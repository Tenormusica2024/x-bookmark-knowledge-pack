# Package Spec (Draft)

## Intended output bundle

Minimum distribution bundle:

- `gallery.html`
- `bookmarks.json`
- `tags.json`
- `translations.json`
- `README.md`

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

