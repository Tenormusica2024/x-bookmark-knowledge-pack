# End-to-End Example

This is the simplest mental model for how the tool is intended to be used.

## Flow

1. your upstream bookmark extractor / DB produces a private-style JSON export
2. `refresh_bundle.py` reads that export
3. `sanitize_import.py` converts it into a public-safe bundle
4. `gallery.html` and companion JSON files are regenerated
5. a scheduler reruns the same refresh command later

---

## Example command

```powershell
python .\scripts\refresh_bundle.py .\sample-data\private-input.sample.json .\dist\live-bundle --publish-dir .\dist\live-bundle-published
```

---

## What the user experiences

- the upstream source can stay richer and more operational
- the distributed/viewed bundle stays smaller and safer
- the HTML view updates when the refresh command runs again
- AI agents can read the JSON outputs directly

---

## Why this matters

This makes the product easier to understand:

- upstream extraction is one concern
- sanitize / bundle generation is another
- HTML browsing is the human-facing output
- scheduled refresh is an operations layer on top

That split is part of the product value, not just an implementation detail.
