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
python .\scripts\sanitize_import.py .\sample-data\private-input.sample.json .\dist\sanitized-sample --overwrite
```

## Useful flags

- `--overwrite`
  - replace an existing non-empty output directory
- `--no-html`
  - skip `gallery.html` generation and emit JSON artifacts only

## Output

- `gallery.html` (unless `--no-html`)
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
- fails clearly if the input is missing / invalid JSON
- fails clearly if the output directory is non-empty unless `--overwrite` is set
- renders HTML from the cleaned JSON unless `--no-html` is set

## Fixture verification

You can also run all bundled private-style fixtures at once:

```powershell
python .\scripts\run_sanitize_fixtures.py
```

This writes per-fixture outputs under `dist/fixture-runs` and generates `fixture-summary.json`.

This fixture runner is for success-oriented fixtures. Invalid JSON / validation-failure cases are covered separately by the exit code check script.

## Exit code verification

You can also run CLI-oriented exit code checks:

```powershell
python .\scripts\run_sanitize_exitcode_checks.py
```

This verifies representative success / CLI error / validation error cases and writes `dist/exitcode-checks/exitcode-summary.json`.
