from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SANITIZE_SCRIPT = ROOT / 'scripts' / 'sanitize_import.py'


class RefreshError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Refresh a public-safe bundle by rerunning the sanitize pipeline into a stable output directory.'
    )
    parser.add_argument('input', type=Path, help='Path to private-style input JSON or extracted bookmark DB export')
    parser.add_argument('output_dir', type=Path, help='Stable output directory to refresh in place')
    parser.add_argument('--title', default='X Bookmark Knowledge Pack', help='HTML title passed to sanitize_import.py')
    parser.add_argument(
        '--subtitle',
        default='Portable local bookmark bundle for humans and AI agents',
        help='HTML subtitle passed to sanitize_import.py',
    )
    parser.add_argument('--no-html', action='store_true', help='Refresh JSON artifacts only')
    parser.add_argument(
        '--publish-dir',
        type=Path,
        default=None,
        help='Optional secondary directory to mirror after a successful refresh (useful for docs/hosting targets).',
    )
    return parser.parse_args()


def run_sanitize(args: argparse.Namespace) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(SANITIZE_SCRIPT),
        str(args.input),
        str(args.output_dir),
        '--overwrite',
        '--title',
        args.title,
        '--subtitle',
        args.subtitle,
    ]
    if args.no_html:
        cmd.append('--no-html')
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def mirror_publish(output_dir: Path, publish_dir: Path) -> None:
    if publish_dir.exists():
        shutil.rmtree(publish_dir)
    shutil.copytree(output_dir, publish_dir)


def write_refresh_report(output_dir: Path, args: argparse.Namespace, result: subprocess.CompletedProcess[str]) -> None:
    report = {
        'refreshed_at': datetime.now(timezone.utc).isoformat(),
        'input': str(args.input),
        'output_dir': str(args.output_dir),
        'publish_dir': str(args.publish_dir) if args.publish_dir else None,
        'no_html': bool(args.no_html),
        'exit_code': result.returncode,
        'stdout': result.stdout.strip(),
        'stderr': result.stderr.strip(),
    }
    (output_dir / 'refresh-report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )


def main() -> int:
    args = parse_args()
    result = run_sanitize(args)
    if result.returncode != 0:
        print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, file=sys.stderr, end='' if result.stderr.endswith('\n') else '\n')
        raise SystemExit(result.returncode)

    if args.publish_dir:
        mirror_publish(args.output_dir, args.publish_dir)

    write_refresh_report(args.output_dir, args, result)
    print(f'Refreshed bundle: {args.output_dir}')
    if args.publish_dir:
        print(f'Published mirror: {args.publish_dir}')
    print(f'Refresh report: {args.output_dir / "refresh-report.json"}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
