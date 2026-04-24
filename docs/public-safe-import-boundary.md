# Public-safe Import Boundary

## Purpose

This document defines the boundary between:

- private operational bookmark data
- public distribution bundles

The goal is to make it explicit **what may move into a public pack, what must stay private, and where normalization should happen**.

---

## Core rule

The public repo should receive only artifacts that are:

1. portable
2. explainable
3. safe to redistribute
4. useful to both humans and AI agents

If a field exists only because of a private workflow, local machine setup, or personal operational context, it should not cross the boundary by default.

---

## Recommended pipeline

### Stage 1: private upstream corpus

Private upstream may contain:

- raw exports
- unstable enrichment fields
- local file paths
- personal notes
- machine-specific metadata
- private automation markers
- intermediate classification traces

This stage is allowed to be messy.

### Stage 2: normalized internal model

Before public packaging, normalize into a stable intermediate form.

Recommended normalization responsibilities:

- unify date formats
- normalize author fields
- normalize media arrays
- normalize tag/category shape
- separate translated text from original text
- remove machine-specific or user-specific glue fields

This is the most important boundary layer.

### Stage 3: public-safe bundle

Public output should contain only the cleaned bundle artifacts.

Minimum intended outputs:

- `gallery.html`
- `bookmarks.json`
- `tags.json`
- `translations.json`
- `package-info.json`
- `README.md`

---

## Keep vs remove policy

### Safe to keep in public `bookmarks.json`

Typical safe fields:

- bookmark/post id
- text content that is already part of the exported post
- created timestamp
- normalized author handle / display name
- normalized media descriptors
- source post URL if publicly resolvable

### Usually remove from public `bookmarks.json`

Remove by default:

- local file paths
- browser profile references
- local cache keys
- local screenshot paths
- internal job ids
- personal notes not intended for sharing
- private review annotations
- internal experimental scores without explanation
- machine names / usernames / home-directory paths

### Safe to keep in public `tags.json`

- primary category
- secondary categories
- category list
- classification timestamp

### Usually remove from public `tags.json`

- raw LLM prompts
- full classification reasoning traces
- provider-specific request metadata
- experimental debug fields
- confidence values that are not documented

### Safe to keep in public `translations.json`

- original text when it is already public post text
- normalized translated text
- lightweight author reference

### Usually remove from public `translations.json`

- internal translation prompt history
- provider metadata
- local retry logs
- debug comparison fields that are not part of the product

---

## Normalization boundary recommendations

Normalize before packaging, not during final HTML rendering.

Recommended split:

- import / sanitize stage
  - drop unsafe fields
  - coerce schema
  - prepare public-safe JSON outputs
- render stage
  - consume already-clean JSON
  - build static HTML only

This keeps the public renderer simple and auditable.

---

## Public bundle checklist

Before shipping a public bundle, confirm:

- no absolute local paths remain
- no machine-specific identifiers remain
- no private automation metadata remains
- no personal-only notes remain
- field names are understandable without private context
- JSON files are still useful to agents without the HTML

---

## Recommended next implementation step

The public repo should eventually gain an explicit import/sanitize step that:

1. accepts a broader private-style input
2. emits a narrower public-safe normalized output
3. validates that forbidden fields are not present

That step is the real bridge between the private working repo and the public distribution repo.
