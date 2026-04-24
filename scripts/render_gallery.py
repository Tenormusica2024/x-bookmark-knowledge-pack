from __future__ import annotations

import argparse
import html
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a portable local bookmark gallery from bookmarks.json"
    )
    parser.add_argument("input", type=Path, help="Path to bookmarks.json")
    parser.add_argument("output", type=Path, help="Path to output HTML file")
    parser.add_argument(
        "--title",
        default="X Bookmark Knowledge Pack",
        help="HTML title and heading",
    )
    parser.add_argument(
        "--subtitle",
        default="Portable local bookmark bundle for humans and AI agents",
        help="Subtitle shown under the title",
    )
    parser.add_argument(
        "--tags",
        type=Path,
        default=None,
        help="Path to tags.json",
    )
    return parser.parse_args()


def format_date(value: str) -> str:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return value


def tweet_url(tweet: dict) -> str:
    author = tweet.get("author") or {}
    username = author.get("username", "")
    tweet_id = tweet.get("id", "")
    return f"https://x.com/{quote(username)}/status/{tweet_id}"


def classify_media_type(tweet: dict) -> str:
    media_items = tweet.get("media") or []
    if not media_items:
        return "text"
    types = {m.get("type", "") for m in media_items}
    if "video" in types:
        return "video"
    if "animated_gif" in types:
        return "gif"
    if "photo" in types:
        return "photo"
    return "text"


def best_media_href(media: dict) -> str:
    return media.get("expanded_url") or media.get("video_url") or media.get("media_url_https") or "#"


def preview_src(media: dict) -> str:
    return media.get("media_url_https") or ""


def media_badge(media: dict) -> str:
    media_type = media.get("type", "media")
    if media_type == "video":
        return "Video"
    return "Image"


def render_card(tweet: dict, tag_map: dict[str, dict]) -> str:
    media_items = tweet.get("media") or []
    media_type = classify_media_type(tweet)

    author = tweet.get("author") or {}
    text = (tweet.get("text") or "").strip()
    safe_text = html.escape(text)
    is_long = len(text) > 200
    safe_name = html.escape(author.get("display_name") or author.get("username") or "unknown")
    safe_user = html.escape(author.get("username") or "")
    safe_date = html.escape(format_date(tweet.get("created_at", "")))
    safe_tweet_url = html.escape(tweet_url(tweet), quote=True)

    media_html = []
    for idx, media in enumerate(media_items, start=1):
        href = html.escape(best_media_href(media), quote=True)
        src = html.escape(preview_src(media), quote=True)
        label = html.escape(f"{media_badge(media)} {idx}", quote=True)
        alt = html.escape(text[:120] or f"{media_badge(media)} preview", quote=True)
        if media.get("type") == "video":
            media_html.append(
                f"""
                <a class="media-link" href="{href}" target="_blank" rel="noreferrer">
                  <img loading="lazy" src="{src}" alt="{alt}">
                  <span class="media-badge">{label}</span>
                  <span class="media-play">Play on source</span>
                </a>
                """
            )
        else:
            media_html.append(
                f"""
                <a class="media-link" href="{href}" target="_blank" rel="noreferrer">
                  <img loading="lazy" src="{src}" alt="{alt}">
                  <span class="media-badge">{label}</span>
                </a>
                """
            )

    media_count_label = f"{len(media_items)} media" if media_items else "text only"

    tweet_id = str(tweet.get("id", ""))
    tag_info = tag_map.get(tweet_id, {})
    primary_tag = tag_info.get("primary", "")
    secondary_tags = tag_info.get("secondary", [])
    all_tags = [primary_tag] + secondary_tags if primary_tag else []
    data_tags = html.escape(" ".join(all_tags), quote=True)
    data_primary = html.escape(primary_tag, quote=True)

    tag_badges = ""
    if primary_tag:
        tag_badges_html = f'<span class="tag-badge tag-primary">{html.escape(primary_tag)}</span>'
        for st in secondary_tags:
            tag_badges_html += f'<span class="tag-badge">{html.escape(st)}</span>'
        tag_badges = f'<div class="tag-row">{tag_badges_html}</div>'

    return f"""
    <article class="card" data-author="{safe_user.lower()}" data-text="{html.escape(text.lower(), quote=True)}" data-media-type="{media_type}" data-tags="{data_tags}" data-primary-tag="{data_primary}">
      <div class="card-top">
        <div>
          <a class="author" href="https://x.com/{safe_user}" target="_blank" rel="noreferrer">{safe_name}</a>
          <span class="handle">@{safe_user}</span>
        </div>
        <a class="post-link" href="{safe_tweet_url}" target="_blank" rel="noreferrer">Open post</a>
      </div>
      <div class="meta">{safe_date} · {media_count_label}</div>
      {tag_badges}
      <p class="text{' text-long' if is_long else ''}">{safe_text}</p>
      {f'<button class="expand-btn" type="button">Show more</button>' if is_long else ''}
      {f'<div class="media-grid">{chr(10).join(media_html)}</div>' if media_html else ''}
    </article>
    """


def build_html(
    data: dict,
    title: str,
    subtitle: str,
    tags_data: dict | None = None,
) -> str:
    tweets = data.get("tweets") or []
    tag_map: dict[str, dict] = {}
    if tags_data:
        for tag in tags_data.get("tags", []):
            tag_map[str(tag["id"])] = tag

    cards = [render_card(tweet, tag_map) for tweet in tweets]
    media_count = sum(len(tweet.get("media") or []) for tweet in tweets)
    card_count = len(tweets)
    text_only_count = sum(1 for t in tweets if not t.get("media"))
    video_count = sum(1 for t in tweets if classify_media_type(t) == "video")
    photo_count = sum(1 for t in tweets if classify_media_type(t) == "photo")
    gif_count = sum(1 for t in tweets if classify_media_type(t) == "gif")

    tag_categories = tags_data.get("categories", []) if tags_data else []
    tag_counts: dict[str, int] = {cat: 0 for cat in tag_categories}
    for tweet in tweets:
        info = tag_map.get(str(tweet.get("id", "")), {})
        primary = info.get("primary", "")
        if primary:
            tag_counts[primary] = tag_counts.get(primary, 0) + 1

    generated_at = html.escape(str(data.get("exported_at", "")))
    title_safe = html.escape(title)
    subtitle_safe = html.escape(subtitle)
    summary = f"{card_count} posts · {media_count} linked media · exported {generated_at}"

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title_safe}</title>
  <style>
    :root {{
      --bg: #f4f1ea;
      --panel: #fffdf8;
      --ink: #1f1f1a;
      --muted: #6d6a62;
      --line: #ddd4c8;
      --accent: #0f766e;
      --shadow: 0 18px 40px rgba(46, 37, 24, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      background:
        radial-gradient(circle at top right, rgba(15,118,110,0.10), transparent 24%),
        linear-gradient(180deg, #f7f2e9 0%, #f1ebe0 100%);
      color: var(--ink);
    }}
    main {{ max-width: 1320px; margin: 0 auto; padding: 32px 20px 56px; }}
    .hero {{
      margin-bottom: 28px;
      padding: 28px;
      border: 1px solid var(--line);
      background: rgba(255,253,248,0.88);
      box-shadow: var(--shadow);
    }}
    h1 {{ margin: 0 0 8px; font-size: clamp(32px, 5vw, 56px); line-height: 0.95; }}
    .subtitle {{ margin: 0 0 10px; color: var(--ink); font-size: 16px; }}
    .summary {{ color: var(--muted); font-size: 16px; }}
    .toolbar, .filter-bar, .and-filter-wrap {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 12px;
      align-items: center;
    }}
    .toolbar input, .and-filter-select {{
      padding: 10px 12px;
      border: 1px solid var(--line);
      background: var(--panel);
      color: var(--ink);
      font-size: 14px;
      min-width: 220px;
    }}
    .toggle-group {{
      display: inline-flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
      padding: 8px;
      border: 1px solid var(--line);
      background: var(--panel);
    }}
    .toggle-label, .and-filter-label {{
      color: var(--muted);
      font-size: 12px;
      margin-right: 4px;
    }}
    .toggle-btn, .filter-btn {{
      padding: 8px 12px;
      border: 1px solid var(--line);
      background: var(--panel);
      color: var(--muted);
      font-family: inherit;
      font-size: 12px;
      cursor: pointer;
    }}
    .toggle-btn.active, .filter-btn.active {{
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }}
    .results {{ margin: 14px 0 22px; color: var(--muted); font-size: 14px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 18px;
    }}
    .card {{
      border: 1px solid var(--line);
      background: var(--panel);
      box-shadow: var(--shadow);
      padding: 16px;
    }}
    .card-top {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
    }}
    .author {{
      color: var(--ink);
      text-decoration: none;
      font-weight: 700;
      font-size: 18px;
    }}
    .handle, .meta {{ color: var(--muted); font-size: 13px; }}
    .post-link {{ color: var(--accent); text-decoration: none; font-size: 13px; white-space: nowrap; }}
    .text {{
      margin: 12px 0 14px;
      font-size: 14px;
      line-height: 1.55;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .text-long {{
      display: -webkit-box;
      -webkit-line-clamp: 5;
      -webkit-box-orient: vertical;
      overflow: hidden;
      white-space: normal;
    }}
    .text-long.expanded {{
      display: block;
      -webkit-line-clamp: unset;
      overflow: visible;
      white-space: pre-wrap;
    }}
    .expand-btn {{
      background: none;
      border: none;
      color: var(--accent);
      font-family: inherit;
      font-size: 13px;
      cursor: pointer;
      padding: 0;
      margin: -8px 0 8px;
    }}
    .media-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}
    .media-link {{
      position: relative;
      display: block;
      border: 1px solid var(--line);
      overflow: hidden;
      background: #ece5d8;
      aspect-ratio: 1 / 1;
    }}
    .media-link img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .media-badge, .media-play {{
      position: absolute;
      bottom: 8px;
      font-size: 11px;
      padding: 4px 6px;
    }}
    .media-badge {{
      right: 8px;
      background: rgba(31,31,26,0.78);
      color: #fff;
    }}
    .media-play {{
      left: 8px;
      background: rgba(255,253,248,0.92);
      color: var(--ink);
    }}
    .tag-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin: 6px 0 0;
    }}
    .tag-badge {{
      display: inline-block;
      padding: 2px 8px;
      font-size: 11px;
      border: 1px solid var(--line);
      color: var(--muted);
      background: var(--bg);
    }}
    .tag-badge.tag-primary {{
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }}
    @media (max-width: 640px) {{
      main {{ padding: 18px 12px 40px; }}
      .hero {{ padding: 18px; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>{title_safe}</h1>
      <div class="subtitle">{subtitle_safe}</div>
      <div class="summary">{summary}</div>
      <div class="toolbar">
        <input id="searchInput" type="search" placeholder="Search text or @author">
        <div class="toggle-group" id="tagScopeToggle">
          <span class="toggle-label">Tag Match</span>
          <button class="toggle-btn active" type="button" data-tag-scope="all">All tags</button>
          <button class="toggle-btn" type="button" data-tag-scope="primary">Primary only</button>
        </div>
      </div>
      <div class="filter-bar" id="filterBar">
        <button class="filter-btn active" data-filter="all">All ({card_count})</button>
        <button class="filter-btn" data-filter="video">Video ({video_count})</button>
        <button class="filter-btn" data-filter="photo">Photo ({photo_count})</button>
        <button class="filter-btn" data-filter="gif">GIF ({gif_count})</button>
        <button class="filter-btn" data-filter="text">Text ({text_only_count})</button>
      </div>
      {"" if not tag_categories else '<div class="filter-bar tag-filter-bar" id="tagFilterBar"><button class="filter-btn active" data-tag="all">All Tags</button>' + "".join(f'<button class="filter-btn" data-tag="{html.escape(cat, quote=True)}">{html.escape(cat)} ({tag_counts.get(cat, 0)})</button>' for cat in tag_categories) + '</div>'}
      {"" if not tag_categories else '<div class="and-filter-wrap"><span class="and-filter-label">AND tag</span><select id="andTagSelect" class="and-filter-select"><option value="all">None</option>' + "".join(f'<option value="{html.escape(cat, quote=True)}">{html.escape(cat)}</option>' for cat in tag_categories) + '</select></div>'}
      <div id="results" class="results"></div>
    </section>
    <section class="grid">
      {''.join(cards)}
    </section>
  </main>
  <script>
    const cards = Array.from(document.querySelectorAll('.card'));
    const searchInput = document.getElementById('searchInput');
    const results = document.getElementById('results');
    const mediaFilterButtons = document.querySelectorAll('#filterBar .filter-btn');
    const tagFilterButtons = document.querySelectorAll('#tagFilterBar .filter-btn');
    const tagScopeButtons = document.querySelectorAll('#tagScopeToggle .toggle-btn');
    const andTagSelect = document.getElementById('andTagSelect');
    let activeFilter = 'all';
    let activeTag = 'all';
    let tagScope = 'all';
    let andTag = 'all';

    mediaFilterButtons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        mediaFilterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeFilter = btn.dataset.filter;
        applyFilters();
      }});
    }});

    tagFilterButtons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        tagFilterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeTag = btn.dataset.tag;
        applyFilters();
      }});
    }});

    tagScopeButtons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        tagScopeButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        tagScope = btn.dataset.tagScope || 'all';
        applyFilters();
      }});
    }});

    if (andTagSelect) {{
      andTagSelect.addEventListener('change', () => {{
        andTag = andTagSelect.value || 'all';
        applyFilters();
      }});
    }}

    function applyFilters() {{
      const query = (searchInput.value || '').trim().toLowerCase();
      let visible = 0;

      for (const card of cards) {{
        const author = card.dataset.author || '';
        const text = card.dataset.text || '';
        const mediaType = card.dataset.mediaType || 'text';
        const tags = (card.dataset.tags || '').split(' ');
        const primaryTag = card.dataset.primaryTag || '';
        const matchesQuery = !query || author.includes(query.replace(/^@/, '')) || text.includes(query);
        const matchesType = activeFilter === 'all' || mediaType === activeFilter;
        const matchesTag = activeTag === 'all' || (tagScope === 'primary' ? primaryTag === activeTag : tags.includes(activeTag));
        const matchesAndTag = andTag === 'all' || (tagScope === 'primary' ? primaryTag === andTag : tags.includes(andTag));
        const distinctAndSatisfied = activeTag === 'all' || andTag === 'all' || activeTag !== andTag;
        const show = matchesQuery && matchesType && matchesTag && matchesAndTag && distinctAndSatisfied;
        card.style.display = show ? '' : 'none';
        if (show) visible += 1;
      }}

      const tagModeText = tagScope === 'primary' ? 'primary only' : 'all tags';
      const andModeText = andTag === 'all' ? 'none' : andTag;
      results.textContent = `${{visible}} / ${{cards.length}} cards · tag match: ${{tagModeText}} · and tag: ${{andModeText}}`;
    }}

    searchInput.addEventListener('input', applyFilters);
    applyFilters();

    for (const btn of document.querySelectorAll('.expand-btn')) {{
      btn.addEventListener('click', () => {{
        const text = btn.previousElementSibling;
        if (!text) return;
        const expanded = text.classList.toggle('expanded');
        btn.textContent = expanded ? 'Show less' : 'Show more';
      }});
    }}
  </script>
</body>
</html>
"""


def main() -> None:
    args = parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    tags_data = None
    tags_path = args.tags
    if tags_path is None:
        auto_tags = args.input.parent / "tags.json"
        if auto_tags.exists():
            tags_path = auto_tags
    if tags_path and tags_path.exists():
        tags_data = json.loads(tags_path.read_text(encoding="utf-8"))

    output = build_html(
        data=data,
        title=args.title,
        subtitle=args.subtitle,
        tags_data=tags_data,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
