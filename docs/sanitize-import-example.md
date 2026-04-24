# Private-to-Public Import Example

Use this script when you want to convert a broader private-style input into a narrower public-safe bundle.

## Input expectation

The importer currently accepts a JSON file that may contain:

- `bookmarks`
- `tags`
- `translations`
- extra private-only fields

The script keeps only the public-safe subset and emits a clean bundle.

## Example

```powershell
python .\scripts\sanitize_import.py .\sample-data\private-input.sample.json .\dist\sanitized-sample
```

## Output

- `gallery.html`
- `bookmarks.json`
- `tags.json`
- `translations.json`
- `package-info.json`
- `validation-report.json`
- `README.md`

## Current behavior

- strips obvious private-only fields
- normalizes the core JSON shape
- validates that forbidden private-like markers do not remain
- checks sanitized outputs against explicit allowlists
- writes a validation report with dropped-field counts
- renders HTML from the cleaned JSON

## Fixture verification

You can also run all bundled private-style fixtures at once:

```powershell
python .\scripts\run_sanitize_fixtures.py
```

This writes per-fixture outputs under `dist/fixture-runs` and generates `fixture-summary.json`.
