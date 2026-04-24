# Use with AI Agents

This project is designed so the same bookmark corpus can be used by both humans and AI agents.

## Human-facing artifact

`gallery.html` is the human-facing viewer.

Use it when you want:

- visual browsing
- quick manual filtering
- lightweight local inspection

---

## Agent-facing artifacts

The AI-facing side should primarily use:

- `bookmarks.json`
- `tags.json`
- `translations.json`

These files are easier for agents to inspect, summarize, cluster, or transform than raw HTML.

---

## Recommended agent usage pattern

### `bookmarks.json`

Use as the canonical corpus for:

- retrieval
- summarization
- deduplication
- transformation to other formats
- downstream indexing

### `tags.json`

Use for:

- primary/secondary category lookup
- filtering logic
- evaluating classification quality
- building composite views or presets

### `translations.json`

Use for:

- multilingual normalization
- translating bookmark text before classification
- generating cross-language summaries

---

## Why this matters

Many bookmark tools stop at UI convenience.

This project is trying to make the output package itself reusable as a small local knowledge asset.

That means the static bundle should remain:

- inspectable
- portable
- scriptable
- archive-friendly
- easy to hand to another model or workflow

---

## Good agent tasks on top of the pack

Examples:

- cluster bookmarks into themes
- compare primary vs secondary tagging drift
- produce a Markdown digest
- extract tool mentions
- detect repeated concepts or near-duplicates
- generate a study queue from saved posts

---

## Design rule for future public refactors

When adding features, prefer improvements that make the bundle more useful to both:

1. a human opening `gallery.html`
2. an agent reading structured companion files

If a feature only helps the UI but weakens portability or inspectability, it is probably the wrong priority for this public track.
