# Recommended Upstream Input

## Recommendation

For real use, the recommended upstream source is **an extracted bookmark DB / export JSON that already exists outside the viewer UI**.

In other words:

- do not make the HTML viewer itself responsible for collecting bookmarks
- make the viewer consume a separate upstream extraction result

This is the same direction as the current private workflow.

---

## Why this is recommended

A separate extracted bookmark DB is better because it keeps concerns clean.

### Upstream layer

Responsible for:

- collecting bookmark data
- syncing with X/export sources
- storing richer private operational fields
- keeping intermediate or unstable metadata

### Public-safe bundle layer

Responsible for:

- sanitizing that upstream data
- generating a reusable local bundle
- regenerating HTML / JSON outputs
- producing artifacts for humans and AI agents

---

## What users need to know

If you distribute this tool, users will need guidance on:

1. where their upstream bookmark JSON comes from
2. what shape is recommended
3. how often it updates
4. how it connects to the refresh pipeline

Without that, users can understand the viewer but still not know how to keep it current.

---

## Recommended product message

The practical recommendation is:

- use your preferred extraction DB/export process upstream
- treat this repo as the sanitize + bundle + viewer layer

That makes this project easier to explain and easier to automate.

---

## Suggested default framing

If no better source is available, describe the expected input as:

**private-style extracted bookmark DB export JSON**

That wording is broad enough for real users, while still matching the current design of `sanitize_import.py` and `refresh_bundle.py`.
