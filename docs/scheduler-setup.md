# Scheduler Setup

This document is for users who want periodic refresh without relying on an AI agent to manually rerun commands.

## Important point

You do **not** need an AI agent for the recurring part.

You only need to configure the scheduler once.

After that, the machine can rerun the refresh command automatically.

---

## Recommended base command

```powershell
python .\scripts\refresh_bundle.py <input.json> <output-dir>
```

Example:

```powershell
python .\scripts\refresh_bundle.py .\sample-data\private-input.sample.json .\dist\live-bundle
```

---

## Windows Task Scheduler

Recommended when the user runs this on Windows.

### Basic setup

- Program/script:
  - `python`
- Add arguments:
  - `.\scripts\refresh_bundle.py .\sample-data\private-input.sample.json .\dist\live-bundle`
- Start in:
  - repo root directory

### Suggested trigger

- daily
- or every few hours, depending on how often the upstream bookmark DB updates

### Notes

- keep the repo on a stable local path
- use absolute paths if Task Scheduler has trouble with relative paths
- test the command manually once before scheduling it

---

## cron (Linux / macOS)

Example:

```bash
0 */6 * * * cd /path/to/x-bookmark-knowledge-pack && python ./scripts/refresh_bundle.py ./sample-data/private-input.sample.json ./dist/live-bundle
```

---

## GitHub Actions

Use when:

- the upstream input can be produced inside GitHub
- or the sanitized bundle is versioned/published through the repo itself

This repo does not yet include an Actions workflow template, but the refresh command is designed to be scheduler-friendly.

---

## Recommended operational pattern

1. keep one stable upstream JSON location
2. keep one stable output directory
3. point the scheduler at `refresh_bundle.py`
4. inspect `refresh-report.json` and `validation-report.json` when something goes wrong

---

## Failure handling

If refresh fails:

- check scheduler logs first
- then check stderr from the failed command
- then inspect the upstream JSON and the sanitize validation rules

The CLI exit codes remain:

- `0` success
- `2` CLI/input/output usage error
- `3` validation failure
