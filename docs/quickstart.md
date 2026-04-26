# Quickstart

This document is for first-time users of the public distribution repo.

## Goal

Generate a small local bundle that can be:

- opened by a human in a browser
- inspected by an AI agent as structured files
- archived or shared as static artifacts

---

## Prerequisites

- Python 3.10 / 3.11 / 3.12
- local clone of this repository

No server is required.
No database is required.
No X login is required for the sample pack.

---

## Fastest path

Run:

```powershell
python .\scripts\build_sample_pack.py
```

This creates a sample bundle under `dist/sample-pack`.

Main output:

- `gallery.html`
- `bookmarks.json`
- `tags.json`
- `translations.json`
- `package-info.json`
- `README.md`

Open `gallery.html` locally in your browser.

If you want a stronger local validation pass before using your own data, run:

```powershell
python .\scripts\run_sanitize_fixtures.py
python .\scripts\run_sanitize_exitcode_checks.py
```

Then rebuild the sample pack once.

---

## Rendering your own data

Basic form:

```powershell
python .\scripts\render_gallery.py <input-bookmarks.json> <output-gallery.html> --tags <tags.json>
```

Example:

```powershell
python .\scripts\render_gallery.py .\sample-data\bookmarks.json .\dist\custom\gallery.html --tags .\sample-data\tags.json
```

If `tags.json` exists in the same folder as the input bookmarks file, the renderer will try to use it automatically.

---

## What the HTML already supports

- keyword search
- author search
- media-type filtering
- category/tag filtering
- `Tag Match` mode switch
  - `All tags`
  - `Primary only`
- `AND tag` filtering

---

## Intended workflow

1. prepare normalized bookmark data
2. prepare classification / tag data
3. render `gallery.html`
4. bundle the HTML and JSON files together
5. share or archive the pack as a static folder or zip

---

## Next likely improvements

- input validation
- stronger package metadata
- optional Markdown / JSONL companion exports
- clearer importer path from private operational data to public-safe bundles

---

## Related docs

- `docs/quick-reference.md`
- `docs/sanitize-import-example.md`
- `docs/refresh-pipeline.md`
- `docs/scheduler-setup.md`
- `docs/recommended-upstream-input.md`
- `docs/use-with-agents.md`
