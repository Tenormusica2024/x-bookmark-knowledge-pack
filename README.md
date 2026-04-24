# x-bookmark-knowledge-pack

Turn X bookmarks into a **portable local knowledge pack** for both humans and AI agents.

This public repo is the distribution track for tooling incubated in the private `x-bookmark-gallery` environment.

## Core idea

This is **not** trying to be a generic bookmark SaaS.
It is trying to make exported X bookmarks:

- local-first
- portable
- human-browsable
- AI-readable
- static and archive-friendly

Think of it as:

**a knowledge-pack generator / viewer for X bookmarks**

not:

**a cloud bookmark manager**

---

## Package shape

Minimum public bundle:

- `gallery.html`
- `bookmarks.json`
- `tags.json`
- `translations.json`
- `package-info.json`
- `README.md`

Optional later:

- `validation-report.json`
- `bookmarks.md`
- `bookmarks.jsonl`

---

## What already works

- local static gallery rendering
- text / author search
- media-type filtering
- tag filtering
- `Tag Match` toggle
- `AND tag` filtering
- sample pack generation
- private-style input -> public-safe bundle sanitizing
- validation report generation

---

## Fast start

### Build the sample pack

```powershell
python .\scripts\build_sample_pack.py
```

Output goes to `dist/sample-pack`.

### Render a gallery directly

```powershell
python .\scripts\render_gallery.py .\sample-data\bookmarks.json .\dist\custom\gallery.html --tags .\sample-data\tags.json
```

### Sanitize a broader private-style input

```powershell
python .\scripts\sanitize_import.py .\sample-data\private-input.sample.json .\dist\sanitized-sample --overwrite
```

---

## Read next

- `docs/quick-reference.md`
- `docs/quickstart.md`
- `docs/sanitize-import-example.md`
- `docs/use-with-agents.md`
- `docs/public-safe-import-boundary.md`

---

## Positioning

This project should try to win on:

- bookmark-to-knowledge-pack transformation
- local shareability
- AI-readable static artifacts
- simple human browsing over structured exports

Not on:

- cloud sync scale
- generic bookmark SaaS breadth
- “AI tagging” alone
