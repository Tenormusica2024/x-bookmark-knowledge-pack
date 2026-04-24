from __future__ import annotations

import json
import shutil
from pathlib import Path

from render_gallery import build_html, classify_media_type


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "sample-data"
DIST_DIR = ROOT / "dist" / "sample-pack"


def build_manifest(bookmarks: dict, tags: dict, translations: dict) -> dict:
    tweets = bookmarks.get("tweets") or []
    tag_rows = tags.get("tags") or []
    primary_counts: dict[str, int] = {}
    for row in tag_rows:
        primary = row.get("primary")
        if primary:
            primary_counts[primary] = primary_counts.get(primary, 0) + 1

    media_summary = {
        "text": 0,
        "photo": 0,
        "video": 0,
        "gif": 0,
    }
    for tweet in tweets:
        media_summary[classify_media_type(tweet)] += 1

    return {
        "name": "X Bookmark Knowledge Pack (Sample)",
        "kind": "sample-pack",
        "generated_from": "sample-data",
        "generated_at": bookmarks.get("exported_at"),
        "files": [
            "gallery.html",
            "bookmarks.json",
            "tags.json",
            "translations.json",
            "package-info.json",
            "README.md",
        ],
        "stats": {
            "bookmarks": len(tweets),
            "translated_rows": len(translations),
            "primary_categories_used": sorted(primary_counts.keys()),
            "primary_category_counts": primary_counts,
            "media_summary": media_summary,
        },
        "viewer_capabilities": [
            "search",
            "media-type-filter",
            "tag-filter",
            "tag-match-scope",
            "and-tag-filter",
        ],
        "agent_use": {
            "canonical_corpus": "bookmarks.json",
            "classification_layer": "tags.json",
            "translation_layer": "translations.json",
        },
    }


def main() -> None:
    bookmarks_path = SAMPLE_DIR / "bookmarks.json"
    tags_path = SAMPLE_DIR / "tags.json"
    translations_path = SAMPLE_DIR / "translations.json"

    bookmarks = json.loads(bookmarks_path.read_text(encoding="utf-8"))
    tags = json.loads(tags_path.read_text(encoding="utf-8"))
    translations = json.loads(translations_path.read_text(encoding="utf-8"))

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    html = build_html(
        data=bookmarks,
        title="X Bookmark Knowledge Pack (Sample)",
        subtitle="Portable local sample bundle for humans and AI agents",
        tags_data=tags,
    )
    (DIST_DIR / "gallery.html").write_text(html, encoding="utf-8")
    shutil.copy2(bookmarks_path, DIST_DIR / "bookmarks.json")
    shutil.copy2(tags_path, DIST_DIR / "tags.json")
    shutil.copy2(translations_path, DIST_DIR / "translations.json")

    manifest = build_manifest(bookmarks, tags, translations)
    (DIST_DIR / "package-info.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readme = """# Sample Pack

This folder is a generated sample output bundle for distribution testing.

Included files:

- gallery.html
- bookmarks.json
- tags.json
- translations.json
- package-info.json

Suggested usage:

- Open `gallery.html` in a browser for the human-facing view.
- Read `bookmarks.json`, `tags.json`, and `translations.json` from AI agents or scripts.
- Use `package-info.json` as a lightweight manifest for pack metadata and available capabilities.
"""
    (DIST_DIR / "README.md").write_text(readme, encoding="utf-8")
    print(f"Built sample pack at: {DIST_DIR}")


if __name__ == "__main__":
    main()
