from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / 'dist' / 'exitcode-checks'
SCRIPT = ROOT / 'scripts' / 'sanitize_import.py'
SAMPLE_DIR = ROOT / 'sample-data'


def run_case(name: str, args: list[str], expected_exit: int) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return {
        'case': name,
        'expected_exit': expected_exit,
        'actual_exit': result.returncode,
        'ok': result.returncode == expected_exit,
        'stdout': result.stdout.strip(),
        'stderr': result.stderr.strip(),
    }


def main() -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    success_out = DIST_DIR / 'success'
    occupied_out = DIST_DIR / 'occupied'
    occupied_out.mkdir(parents=True, exist_ok=True)
    (occupied_out / 'existing.txt').write_text('occupied\n', encoding='utf-8')

    cases = [
        run_case(
            'success-overwrite-no-html',
            [str(SAMPLE_DIR / 'private-input.sample.json'), str(success_out), '--overwrite', '--no-html'],
            0,
        ),
        run_case(
            'missing-input',
            [str(SAMPLE_DIR / 'does-not-exist.json'), str(DIST_DIR / 'missing-input-out')],
            2,
        ),
        run_case(
            'invalid-json',
            [str(SAMPLE_DIR / 'private-input.invalid.json'), str(DIST_DIR / 'invalid-json-out')],
            2,
        ),
        run_case(
            'nonempty-output-without-overwrite',
            [str(SAMPLE_DIR / 'private-input.sample.json'), str(occupied_out)],
            2,
        ),
        run_case(
            'validation-failure-forbidden-source-url',
            [str(SAMPLE_DIR / 'private-input.validation-fail.json'), str(DIST_DIR / 'validation-fail-out')],
            3,
        ),
    ]

    summary_path = DIST_DIR / 'exitcode-summary.json'
    summary_path.write_text(json.dumps(cases, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    failed = [case for case in cases if not case['ok']]
    print(f'Exit code checks completed: {len(cases)} cases')
    print(f'Summary: {summary_path}')
    if failed:
        print(f'Failures: {len(failed)}')
        raise SystemExit(1)


if __name__ == '__main__':
    main()
