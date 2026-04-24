from __future__ import annotations

import json
import shutil
from pathlib import Path

from render_gallery import build_html


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "sample-data"
DIST_DIR = ROOT / "dist" / "sample-pack"


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

    readme = """# Sample Pack

This folder is a generated sample output bundle.

Files:

- gallery.html
- bookmarks.json
- tags.json
- translations.json

Open `gallery.html` in a browser for the human-facing view.
Use the JSON files as structured input for AI agents or downstream tooling.
"""
    (DIST_DIR / "README.md").write_text(readme, encoding="utf-8")
    print(f"Built sample pack at: {DIST_DIR}")


if __name__ == "__main__":
    main()
