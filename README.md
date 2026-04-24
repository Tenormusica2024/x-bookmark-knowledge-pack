# x-bookmark-viewer

Portable local X bookmark knowledge pack viewer.

This repository is the public-facing distribution track for the bookmark tooling
that is currently incubated in the private `x-bookmark-gallery` repo.

The goal is **not** to compete head-on as a generic cloud bookmark manager.
The goal is to make X bookmarks:

- human-readable
- AI-agent-readable
- local-first
- portable
- easy to archive and share as static artifacts

---

## Positioning

This project is best understood as:

**a local knowledge pack generator / viewer for X bookmarks**

instead of:

**a general-purpose bookmark SaaS**

That means the product direction prioritizes:

- static HTML output
- JSON / Markdown companion artifacts
- local-first workflows
- portability
- AI-friendly structured data

---

## Planned package shape

The intended distribution shape is a portable bundle such as:

- `gallery.html`
- `bookmarks.json`
- `tags.json`
- `translations.json`
- optional `bookmarks.md`
- optional `bookmarks.jsonl`
- `README.md`

Human users open the HTML.

AI agents read the structured files.

---

## Current repo role

This public repo is the distribution-facing track.

The private repo remains the experimentation / operations track.

Recommended division:

- private repo
  - real operations
  - real bookmark data
  - experimental classification logic
  - pre-release improvements

- public repo
  - generalized packaging
  - sample data
  - documentation
  - safe defaults
  - public distribution quality

---

## Initial public roadmap

### Phase 1

- establish public repo skeleton
- define package structure
- define what should be public vs private
- add distribution-oriented README/docs

### Phase 2

- generalize paths and configuration
- remove private-environment assumptions
- prepare sample dataset
- stabilize HTML artifact format

### Phase 3

- make AI-readable companion artifacts first-class
- improve output consistency
- refine distribution UX

---

## Differentiation thesis

This project should win on:

1. local-first portability
2. static artifact quality
3. AI-agent-readable outputs
4. human-friendly filtering and browsing
5. bookmark-to-knowledge-pack transformation

Not on:

- being the biggest bookmark SaaS
- having the strongest cloud search
- generic AI tagging alone

---

## Near-term next step

The next recommended step is:

**define the public distribution package spec**

See:

- `docs/public-distribution-strategy.md`
- `docs/package-spec.md`
- `docs/private-to-public-split.md`

