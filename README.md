# x-bookmark-knowledge-pack

Turn X bookmarks into a **portable local knowledge pack** that both humans and AI agents can read.

This repository is the public distribution track for bookmark tooling that is currently incubated in the private `x-bookmark-gallery` environment.

The goal is **not** to win as a generic bookmark SaaS.
The goal is to make exported X bookmarks:

- easy to browse for humans
- easy to consume for AI agents
- local-first
- portable
- static and archive-friendly

---

## What this is

Think of this project as:

**a knowledge-pack generator / viewer for X bookmarks**

not:

**a cloud bookmark manager**

That means the core value is the package itself:

- `gallery.html` for human browsing
- `bookmarks.json` as canonical machine-readable data
- `tags.json` for classification / filtering
- `translations.json` for multilingual support
- optional downstream exports such as Markdown or JSONL

Open the HTML in a browser.
Give the structured files to AI agents, scripts, or PKM pipelines.

---

## Why this exists

The generic bookmark-manager space is already crowded.

A public version is more defensible if it focuses on:

1. local-first portability
2. static artifact quality
3. AI-agent-readable outputs
4. human-friendly filtering on top of structured data
5. turning bookmarks into reusable knowledge packs

So the product direction is intentionally biased toward:

- no server requirement
- no account requirement
- zip-friendly distribution
- inspectable local files
- long-term archive value

---

## Current package shape

Minimum bundle:

- `gallery.html`
- `bookmarks.json`
- `tags.json`
- `translations.json`
- `README.md`

Optional later additions:

- `bookmarks.md`
- `bookmarks.jsonl`
- sample screenshots
- importer / validator helpers

---

## What already works

Current public-safe minimum:

- render a local static gallery from `bookmarks.json`
- automatically use `tags.json` when available
- search by text / author
- media-type filtering
- tag filtering
- `Tag Match` toggle (`All tags` / `Primary only`)
- `AND tag` filtering
- sample pack generation for distribution testing

---

## Quick start

### 1. Build the sample pack

```powershell
python .\scripts\build_sample_pack.py
```

This generates:

- `dist/sample-pack/gallery.html`
- `dist/sample-pack/bookmarks.json`
- `dist/sample-pack/tags.json`
- `dist/sample-pack/translations.json`
- `dist/sample-pack/README.md`

Then open `dist/sample-pack/gallery.html` in your browser.

### 2. Render your own gallery

```powershell
python .\scripts\render_gallery.py .\sample-data\bookmarks.json .\dist\custom\gallery.html --tags .\sample-data\tags.json
```

If `tags.json` exists next to the input file, it is also auto-detected.

---

## Recommended repo split

### Private repo

Use the private repo for:

- real bookmark data
- experimental classification logic
- operational automation
- environment-specific workflows
- pre-release iteration

### Public repo

Use this repo for:

- generalized packaging
- sample data
- safe defaults
- distribution-oriented docs
- public-friendly renderer / builder UX

---

## Core docs

- `docs/public-distribution-strategy.md`
- `docs/package-spec.md`
- `docs/private-to-public-split.md`
- `docs/bootstrap-plan.md`
- `docs/quickstart.md`
- `docs/use-with-agents.md`

---

## Near-term direction

The next refactoring focus for the public track should be:

1. package UX polish
2. sample quality improvement
3. clearer import / normalization boundary
4. better AI-facing companion outputs
5. release-ready distribution flow

---

## Differentiation thesis

This project should try to win on:

- bookmark-to-knowledge-pack transformation
- local shareability
- AI-readable static artifacts
- simple human browsing over structured exports

It should **not** try to win mainly on:

- biggest bookmark database
- cloud sync/network effects
- SaaS-style workspace breadth
- generic AI tagging alone
