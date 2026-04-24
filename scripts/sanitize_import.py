from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from build_sample_pack import build_manifest
from render_gallery import build_html

FORBIDDEN_SUBSTRINGS = (
    ':\\',
    '/Users/',
    '/home/',
    'browser_profile',
    'cache_key',
    'local_path',
    'screenshot_path',
    'job_id',
    'llm_prompt',
    'reasoning_trace',
    'provider_metadata',
    'retry_log',
    'machine_name',
)

DEFAULT_CATEGORIES = [
    'frontend', 'backend', 'workflow', 'ai-agent', 'tool-update', 'oss',
    'indie-dev', 'ai-media', 'prompt-eng', 'x-growth', 'career',
    'ai-industry', 'dev-env', 'lifestyle', 'tutorial'
]

ALLOWED_BOOKMARK_KEYS = {'id', 'text', 'created_at', 'author', 'media', 'source_url'}
ALLOWED_AUTHOR_KEYS = {'id', 'username', 'display_name'}
ALLOWED_MEDIA_KEYS = {'type', 'media_url_https', 'expanded_url', 'video_url'}
ALLOWED_TAG_ROOT_KEYS = {'classified_at', 'total', 'categories', 'tags'}
ALLOWED_TAG_KEYS = {'id', 'primary', 'secondary'}
ALLOWED_TRANSLATION_KEYS = {'author', 'original', 'ja'}
ALLOWED_PACKAGE_INFO_KEYS = {
    'name', 'kind', 'generated_from', 'generated_at', 'files', 'stats',
    'viewer_capabilities', 'agent_use', 'sanitized', 'validation'
}


class CliError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Sanitize a broader private-style input into a public-safe knowledge pack.'
    )
    parser.add_argument('input', type=Path, help='Path to private-style input JSON')
    parser.add_argument('output_dir', type=Path, help='Directory for public-safe bundle output')
    parser.add_argument('--title', default='X Bookmark Knowledge Pack', help='HTML title')
    parser.add_argument(
        '--subtitle',
        default='Portable local bookmark bundle for humans and AI agents',
        help='HTML subtitle',
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Remove existing output contents before writing the sanitized bundle.',
    )
    parser.add_argument(
        '--no-html',
        action='store_true',
        help='Skip gallery.html generation and output JSON artifacts only.',
    )
    return parser.parse_args()


def _norm_media(item: dict[str, Any]) -> dict[str, str]:
    media: dict[str, str] = {
        'type': item.get('type') or 'photo',
        'media_url_https': item.get('media_url_https') or item.get('preview_url') or '',
        'expanded_url': item.get('expanded_url') or item.get('url') or '',
    }
    if item.get('video_url'):
        media['video_url'] = item.get('video_url')
    return media


def sanitize_bookmarks(raw: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int]]:
    tweets_out: list[dict[str, Any]] = []
    dropped_metrics = {
        'bookmark_extra_fields_removed': 0,
        'media_extra_fields_removed': 0,
        'author_extra_fields_removed': 0,
    }
    for row in raw.get('tweets') or []:
        author = row.get('author') or {}
        dropped_metrics['bookmark_extra_fields_removed'] += len(set(row.keys()) - (ALLOWED_BOOKMARK_KEYS | {'tweet_url'}))
        dropped_metrics['author_extra_fields_removed'] += len(set(author.keys()) - ALLOWED_AUTHOR_KEYS)
        for media_row in (row.get('media') or []):
            dropped_metrics['media_extra_fields_removed'] += len(set(media_row.keys()) - (ALLOWED_MEDIA_KEYS | {'preview_url', 'url'}))

        public_row = {
            'id': str(row.get('id') or ''),
            'text': row.get('text') or '',
            'created_at': row.get('created_at') or '',
            'author': {
                'id': str(author.get('id') or ''),
                'username': author.get('username') or '',
                'display_name': author.get('display_name') or author.get('username') or '',
            },
            'media': [_norm_media(m) for m in (row.get('media') or [])],
        }
        source_url = row.get('source_url') or row.get('tweet_url')
        if source_url:
            public_row['source_url'] = source_url
        tweets_out.append(public_row)

    return {
        'exported_at': raw.get('exported_at') or raw.get('generated_at') or '',
        'count': len(tweets_out),
        'tweets': tweets_out,
    }, dropped_metrics


def sanitize_tags(raw: dict[str, Any], tweet_ids: set[str]) -> tuple[dict[str, Any], dict[str, int]]:
    categories = raw.get('categories') or DEFAULT_CATEGORIES
    out_rows = []
    dropped_metrics = {
        'tag_extra_fields_removed': 0,
        'tag_rows_skipped_missing_bookmark': 0,
    }
    for row in raw.get('tags') or []:
        tweet_id = str(row.get('id') or '')
        if tweet_id not in tweet_ids:
            dropped_metrics['tag_rows_skipped_missing_bookmark'] += 1
            continue
        dropped_metrics['tag_extra_fields_removed'] += len(set(row.keys()) - ALLOWED_TAG_KEYS)
        primary = row.get('primary') or ''
        secondary = [x for x in (row.get('secondary') or []) if isinstance(x, str)]
        out_rows.append({'id': tweet_id, 'primary': primary, 'secondary': secondary})
    return {
        'classified_at': raw.get('classified_at') or raw.get('generated_at') or '',
        'total': len(out_rows),
        'categories': categories,
        'tags': out_rows,
    }, dropped_metrics


def sanitize_translations(raw: dict[str, Any], bookmarks: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int]]:
    tweet_map = {str(t['id']): t for t in bookmarks.get('tweets') or []}
    out: dict[str, Any] = {}
    dropped_metrics = {
        'translation_extra_fields_removed': 0,
        'translation_rows_skipped_missing_bookmark': 0,
    }
    for tweet_id, value in (raw or {}).items():
        tid = str(tweet_id)
        if tid not in tweet_map:
            dropped_metrics['translation_rows_skipped_missing_bookmark'] += 1
            continue
        dropped_metrics['translation_extra_fields_removed'] += len(set(value.keys()) - ALLOWED_TRANSLATION_KEYS)
        tweet = tweet_map[tid]
        out[tid] = {
            'author': value.get('author') or tweet.get('author', {}).get('username', ''),
            'original': value.get('original') or tweet.get('text', ''),
            'ja': value.get('ja') or value.get('translated') or value.get('original') or tweet.get('text', ''),
        }
    return out, dropped_metrics


def _assert_exact_keys(obj: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = set(obj.keys()) - allowed
    if extra:
        raise ValueError(f'{label} contains unexpected keys after sanitization: {sorted(extra)}')


def validate_public_safe(payloads: list[tuple[str, Any]]) -> list[str]:
    serialized = json.dumps({name: payload for name, payload in payloads}, ensure_ascii=False)
    lower = serialized.lower()
    hits = [needle for needle in FORBIDDEN_SUBSTRINGS if needle.lower() in lower]
    if hits:
        raise ValueError(f'Forbidden private-like markers remained after sanitization: {hits}')
    return ['forbidden-substring-scan:ok']


def validate_schema(bookmarks: dict[str, Any], tags: dict[str, Any], translations: dict[str, Any], package_info: dict[str, Any]) -> list[str]:
    checks: list[str] = []
    _assert_exact_keys(bookmarks, {'exported_at', 'count', 'tweets'}, 'bookmarks root')
    checks.append('bookmarks-root-keys:ok')
    for tweet in bookmarks.get('tweets') or []:
        _assert_exact_keys(tweet, ALLOWED_BOOKMARK_KEYS, f"bookmark {tweet.get('id')}")
        _assert_exact_keys(tweet.get('author') or {}, ALLOWED_AUTHOR_KEYS, f"bookmark {tweet.get('id')} author")
        for media in tweet.get('media') or []:
            _assert_exact_keys(media, ALLOWED_MEDIA_KEYS, f"bookmark {tweet.get('id')} media")
    checks.append('bookmarks-nested-keys:ok')

    _assert_exact_keys(tags, ALLOWED_TAG_ROOT_KEYS, 'tags root')
    for row in tags.get('tags') or []:
        _assert_exact_keys(row, ALLOWED_TAG_KEYS, f"tag {row.get('id')}")
    checks.append('tags-schema:ok')

    for tweet_id, row in translations.items():
        _assert_exact_keys(row, ALLOWED_TRANSLATION_KEYS, f'translation {tweet_id}')
    checks.append('translations-schema:ok')

    _assert_exact_keys(package_info, ALLOWED_PACKAGE_INFO_KEYS, 'package-info root')
    checks.append('package-info-schema:ok')
    return checks


def build_validation_report(
    bookmarks: dict[str, Any],
    tags: dict[str, Any],
    translations: dict[str, Any],
    drop_metrics: dict[str, int],
    checks: list[str],
    source_name: str,
) -> dict[str, Any]:
    return {
        'source': source_name,
        'status': 'ok',
        'checks': checks,
        'allowlists': {
            'bookmark_keys': sorted(ALLOWED_BOOKMARK_KEYS),
            'author_keys': sorted(ALLOWED_AUTHOR_KEYS),
            'media_keys': sorted(ALLOWED_MEDIA_KEYS),
            'tag_root_keys': sorted(ALLOWED_TAG_ROOT_KEYS),
            'tag_keys': sorted(ALLOWED_TAG_KEYS),
            'translation_keys': sorted(ALLOWED_TRANSLATION_KEYS),
        },
        'counts': {
            'bookmarks': bookmarks.get('count', 0),
            'tag_rows': tags.get('total', 0),
            'translation_rows': len(translations),
        },
        'dropped': drop_metrics,
    }


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load_input_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CliError(f'Input file not found: {path}')
    if not path.is_file():
        raise CliError(f'Input path is not a file: {path}')
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise CliError(f'Input is not valid JSON: {path} (line {exc.lineno}, column {exc.colno})') from exc


def prepare_output_dir(path: Path, overwrite: bool) -> None:
    if path.exists() and not path.is_dir():
        raise CliError(f'Output path exists and is not a directory: {path}')
    if path.exists():
        has_contents = any(path.iterdir())
        if has_contents and not overwrite:
            raise CliError(
                f'Output directory already exists and is not empty: {path} ; rerun with --overwrite to replace it.'
            )
        if has_contents and overwrite:
            shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def main() -> int:
    args = parse_args()
    try:
        raw = load_input_json(args.input)
        prepare_output_dir(args.output_dir, overwrite=args.overwrite)

        bookmarks, bookmark_metrics = sanitize_bookmarks(raw.get('bookmarks') or raw)
        tweet_ids = {str(t['id']) for t in bookmarks.get('tweets') or []}
        tags, tag_metrics = sanitize_tags(raw.get('tags') or {}, tweet_ids)
        translations, translation_metrics = sanitize_translations(raw.get('translations') or {}, bookmarks)
        drop_metrics = bookmark_metrics | tag_metrics | translation_metrics

        package_info = build_manifest(bookmarks, tags, translations)
        files = [
            'bookmarks.json',
            'tags.json',
            'translations.json',
            'package-info.json',
            'validation-report.json',
            'README.md',
        ]
        if not args.no_html:
            files.insert(0, 'gallery.html')
        package_info.update({
            'kind': 'public-safe-bundle',
            'generated_from': args.input.name,
            'sanitized': True,
            'files': files,
        })

        checks = []
        checks.extend(validate_public_safe([
            ('bookmarks', bookmarks),
            ('tags', tags),
            ('translations', translations),
            ('package_info', package_info),
        ]))
        checks.extend(validate_schema(bookmarks, tags, translations, package_info))

        validation = build_validation_report(
            bookmarks=bookmarks,
            tags=tags,
            translations=translations,
            drop_metrics=drop_metrics,
            checks=checks,
            source_name=args.input.name,
        )
        package_info['validation'] = {
            'status': validation['status'],
            'checks': validation['checks'],
            'dropped': validation['dropped'],
        }

        write_json(args.output_dir / 'bookmarks.json', bookmarks)
        write_json(args.output_dir / 'tags.json', tags)
        write_json(args.output_dir / 'translations.json', translations)
        write_json(args.output_dir / 'package-info.json', package_info)
        write_json(args.output_dir / 'validation-report.json', validation)
        if not args.no_html:
            html = build_html(bookmarks, title=args.title, subtitle=args.subtitle, tags_data=tags)
            (args.output_dir / 'gallery.html').write_text(html, encoding='utf-8')
        (args.output_dir / 'README.md').write_text(
            '# Public-safe Bundle\n\nGenerated by sanitize_import.py.\n',
            encoding='utf-8',
        )
        print(f'Sanitized bundle written to: {args.output_dir}')
        print(f'Validation report: {args.output_dir / "validation-report.json"}')
        if args.no_html:
            print('HTML generation skipped (--no-html).')
        return 0
    except CliError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f'VALIDATION ERROR: {exc}', file=sys.stderr)
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
