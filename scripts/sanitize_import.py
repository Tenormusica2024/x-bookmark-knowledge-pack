from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_sample_pack import build_manifest
from render_gallery import build_html

FORBIDDEN_SUBSTRINGS = (
    ':\\',
    '/Users/',
    '/home/',
    'browser_profile',
    'cache_key',
    'local_path',
    'screenshot_path',
    'job_id',
    'llm_prompt',
    'reasoning_trace',
    'provider_metadata',
    'retry_log',
    'machine_name',
)

DEFAULT_CATEGORIES = [
    'frontend', 'backend', 'workflow', 'ai-agent', 'tool-update', 'oss',
    'indie-dev', 'ai-media', 'prompt-eng', 'x-growth', 'career',
    'ai-industry', 'dev-env', 'lifestyle', 'tutorial'
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Sanitize a broader private-style input into a public-safe knowledge pack.'
    )
    parser.add_argument('input', type=Path, help='Path to private-style input JSON')
    parser.add_argument('output_dir', type=Path, help='Directory for public-safe bundle output')
    parser.add_argument('--title', default='X Bookmark Knowledge Pack', help='HTML title')
    parser.add_argument(
        '--subtitle',
        default='Portable local bookmark bundle for humans and AI agents',
        help='HTML subtitle',
    )
    return parser.parse_args()


def _norm_media(item: dict[str, Any]) -> dict[str, str]:
    return {
        'type': item.get('type') or 'photo',
        'media_url_https': item.get('media_url_https') or item.get('preview_url') or '',
        'expanded_url': item.get('expanded_url') or item.get('url') or '',
        **({'video_url': item.get('video_url')} if item.get('video_url') else {}),
    }


def sanitize_bookmarks(raw: dict[str, Any]) -> dict[str, Any]:
    tweets_out: list[dict[str, Any]] = []
    for row in raw.get('tweets') or []:
        author = row.get('author') or {}
        public_row = {
            'id': str(row.get('id') or ''),
            'text': row.get('text') or '',
            'created_at': row.get('created_at') or '',
            'author': {
                'id': str(author.get('id') or ''),
                'username': author.get('username') or '',
                'display_name': author.get('display_name') or author.get('username') or '',
            },
            'media': [_norm_media(m) for m in (row.get('media') or [])],
        }
        source_url = row.get('source_url') or row.get('tweet_url')
        if source_url:
            public_row['source_url'] = source_url
        tweets_out.append(public_row)

    return {
        'exported_at': raw.get('exported_at') or raw.get('generated_at') or '',
        'count': len(tweets_out),
        'tweets': tweets_out,
    }


def sanitize_tags(raw: dict[str, Any], tweet_ids: set[str]) -> dict[str, Any]:
    categories = raw.get('categories') or DEFAULT_CATEGORIES
    out_rows = []
    for row in raw.get('tags') or []:
        tweet_id = str(row.get('id') or '')
        if tweet_id not in tweet_ids:
            continue
        primary = row.get('primary') or ''
        secondary = [x for x in (row.get('secondary') or []) if isinstance(x, str)]
        out_rows.append({'id': tweet_id, 'primary': primary, 'secondary': secondary})
    return {
        'classified_at': raw.get('classified_at') or raw.get('generated_at') or '',
        'total': len(out_rows),
        'categories': categories,
        'tags': out_rows,
    }


def sanitize_translations(raw: dict[str, Any], bookmarks: dict[str, Any]) -> dict[str, Any]:
    tweet_map = {str(t['id']): t for t in bookmarks.get('tweets') or []}
    out: dict[str, Any] = {}
    for tweet_id, value in (raw or {}).items():
        tid = str(tweet_id)
        if tid not in tweet_map:
            continue
        tweet = tweet_map[tid]
        out[tid] = {
            'author': value.get('author') or tweet.get('author', {}).get('username', ''),
            'original': value.get('original') or tweet.get('text', ''),
            'ja': value.get('ja') or value.get('translated') or value.get('original') or tweet.get('text', ''),
        }
    return out


def validate_public_safe(payloads: list[tuple[str, Any]]) -> None:
    serialized = json.dumps({name: payload for name, payload in payloads}, ensure_ascii=False)
    lower = serialized.lower()
    hits = [needle for needle in FORBIDDEN_SUBSTRINGS if needle.lower() in lower]
    if hits:
        raise ValueError(f'Forbidden private-like markers remained after sanitization: {hits}')


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main() -> None:
    args = parse_args()
    raw = json.loads(args.input.read_text(encoding='utf-8'))

    bookmarks = sanitize_bookmarks(raw.get('bookmarks') or raw)
    tweet_ids = {str(t['id']) for t in bookmarks.get('tweets') or []}
    tags = sanitize_tags(raw.get('tags') or {}, tweet_ids)
    translations = sanitize_translations(raw.get('translations') or {}, bookmarks)
    package_info = build_manifest(bookmarks, tags, translations)
    package_info.update({
        'kind': 'public-safe-bundle',
        'generated_from': args.input.name,
        'sanitized': True,
    })

    validate_public_safe([
        ('bookmarks', bookmarks),
        ('tags', tags),
        ('translations', translations),
        ('package_info', package_info),
    ])

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / 'bookmarks.json', bookmarks)
    write_json(args.output_dir / 'tags.json', tags)
    write_json(args.output_dir / 'translations.json', translations)
    write_json(args.output_dir / 'package-info.json', package_info)
    html = build_html(bookmarks, title=args.title, subtitle=args.subtitle, tags_data=tags)
    (args.output_dir / 'gallery.html').write_text(html, encoding='utf-8')
    (args.output_dir / 'README.md').write_text(
        '# Public-safe Bundle\n\nGenerated by sanitize_import.py.\n',
        encoding='utf-8',
    )
    print(f'Sanitized bundle written to: {args.output_dir}')


if __name__ == '__main__':
    main()
