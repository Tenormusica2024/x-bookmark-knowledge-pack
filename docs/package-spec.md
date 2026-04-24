# Package Spec (Draft)

## Intended output bundle

Minimum distribution bundle:

- `gallery.html`
- `bookmarks.json`
- `tags.json`
- `translations.json`
- `package-info.json`
- `README.md`

Sanitized bundle standard additions:

- `validation-report.json`

Optional:

- `bookmarks.md`
- `bookmarks.jsonl`
- screenshots / sample assets

---

## Role of each file

### `gallery.html`

- primary human-facing artifact
- works as a local static viewer
- no backend dependency

### `bookmarks.json`

- raw or lightly normalized bookmark corpus
- canonical machine-readable source

### `tags.json`

- classification output
- filter/category layer

### `translations.json`

- multilingual support layer
- preserve translated text separately from raw source where possible

### `package-info.json`

- lightweight manifest for pack metadata
- summary stats for humans and agents
- quick capability discovery without parsing the full corpus

### `validation-report.json`

- standard validation artifact for sanitized bundles
- explains schema checks and dropped-field counts
- optional for manually assembled or sample-only bundles

### `bookmarks.md`

- optional AI / PKM-friendly text export

### `bookmarks.jsonl`

- optional agent / pipeline-friendly streaming format

---

## Packaging goals

- portable
- static
- inspectable
- archive-friendly
- easy for AI agents to consume
- understandable without private-environment assumptions
