from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / 'sample-data'
DIST_DIR = ROOT / 'dist' / 'fixture-runs'
SCRIPT = ROOT / 'scripts' / 'sanitize_import.py'


def main() -> None:
    fixtures = sorted(SAMPLE_DIR.glob('private-input*.json'))
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    summary = []
    for fixture in fixtures:
        out_dir = DIST_DIR / fixture.stem
        if out_dir.exists():
            shutil.rmtree(out_dir)
        subprocess.run(
            [sys.executable, str(SCRIPT), str(fixture), str(out_dir)],
            check=True,
            cwd=ROOT,
        )
        validation = json.loads((out_dir / 'validation-report.json').read_text(encoding='utf-8'))
        summary.append({
            'fixture': fixture.name,
            'status': validation['status'],
            'checks': validation['checks'],
            'dropped': validation['dropped'],
            'counts': validation['counts'],
        })

    summary_path = DIST_DIR / 'fixture-summary.json'
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Fixture sanitize runs completed: {len(summary)} fixtures')
    print(f'Summary: {summary_path}')


if __name__ == '__main__':
    main()
