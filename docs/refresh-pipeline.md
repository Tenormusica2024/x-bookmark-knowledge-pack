# Refresh Pipeline

This document describes the smallest practical automation layer for keeping the HTML/UI bundle updated.

## What it does

`refresh_bundle.py` is a thin wrapper around `sanitize_import.py`.

It exists so you can point a scheduler at **one command** instead of manually chaining steps.

The refresh flow is:

1. read the upstream input JSON
2. rerun sanitize
3. rewrite the output bundle in place
4. optionally mirror the refreshed bundle to a publish directory
5. write `refresh-report.json`

---

## Recommended command

```powershell
python .\scripts\refresh_bundle.py <input.json> <output-dir>
```

Example:

```powershell
python .\scripts\refresh_bundle.py .\sample-data\private-input.sample.json .\dist\live-bundle
```

---

## Useful options

### `--publish-dir`

Mirror the refreshed output to a second location after a successful refresh.

Example:

```powershell
python .\scripts\refresh_bundle.py .\sample-data\private-input.sample.json .\dist\live-bundle --publish-dir .\docs\live-bundle
```

This is useful when:

- one folder is your working output
- another folder is your static hosting or publish target

### `--no-html`

Refresh JSON artifacts only.

---

## Output

The refresh output contains the normal sanitized bundle plus:

- `refresh-report.json`

This report records:

- refresh time
- input path
- output path
- publish mirror path if used
- subprocess exit code
- stdout/stderr from the sanitize step

---

## Why this matters

The repo already had sanitize / render / validation building blocks.

This script adds the missing orchestration glue so that:

- Windows Task Scheduler
- cron
- GitHub Actions

can all run the same stable command.
