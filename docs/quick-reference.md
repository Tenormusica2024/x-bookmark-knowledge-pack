# Quick Reference

## Main commands

### 1. Build the sample pack

```powershell
python .\scripts\build_sample_pack.py
```

Output:
- `dist/sample-pack/gallery.html`
- `dist/sample-pack/bookmarks.json`
- `dist/sample-pack/tags.json`
- `dist/sample-pack/translations.json`
- `dist/sample-pack/package-info.json`
- `dist/sample-pack/README.md`

### 2. Render gallery from existing JSON

```powershell
python .\scripts\render_gallery.py <input-bookmarks.json> <output-gallery.html> --tags <tags.json>
```

### 3. Sanitize private-style input into public-safe bundle

```powershell
python .\scripts\sanitize_import.py <input.json> <output-dir> --overwrite
```

Useful flags:
- `--overwrite`
- `--no-html`

Typical output:
- `gallery.html` unless `--no-html`
- `bookmarks.json`
- `tags.json`
- `translations.json`
- `package-info.json`
- `validation-report.json`
- `README.md`

Sanitized bundle note:
- `validation-report.json` is standard for sanitize output

### 4. Refresh a stable bundle output

```powershell
python .\scripts\refresh_bundle.py <input.json> <output-dir>
```

OS wrappers:
- Windows: `pwsh -File .\scripts\refresh_bundle.ps1 <input.json> <output-dir>`
- macOS / Linux: `./scripts/refresh_bundle.sh <input.json> <output-dir>`

Useful flags:
- `--publish-dir <dir>`
- `--no-html`

Output:
- refreshed sanitized bundle
- `refresh-report.json`

### 5. Run bundled sanitize fixtures

```powershell
python .\scripts\run_sanitize_fixtures.py
```

Output:
- `dist/fixture-runs/*`
- `dist/fixture-runs/fixture-summary.json`

### 6. Run exit code checks

```powershell
python .\scripts\run_sanitize_exitcode_checks.py
```

Output:
- `dist/exitcode-checks/exitcode-summary.json`

---

## Exit code meaning

- `0`: success
- `2`: CLI/input/output usage error
- `3`: validation failure

---

## Suggested reading order

1. `README.md`
2. `docs/quickstart.md`
3. `docs/sanitize-import-example.md`
4. `docs/use-with-agents.md`
