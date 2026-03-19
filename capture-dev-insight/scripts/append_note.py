#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys

DEFAULT_NOTES_DIR = Path('/Users/bytedance/Documents/Personal-record/MyTypst/Dev/daily-dev-notes')
DEFAULT_TIMEZONE = 'Asia/Shanghai'

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None




def current_note_date() -> str:
    if ZoneInfo is None:
        return datetime.now().date().isoformat()
    return datetime.now(ZoneInfo(DEFAULT_TIMEZONE)).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Append a Markdown insight to a daily note.')
    parser.add_argument('--title', required=True, help='Section title to append.')
    parser.add_argument('--body-file', help='Path to a Markdown body file. If omitted, read from stdin.')
    parser.add_argument('--target-file', help='Explicit Markdown file to append to.')
    parser.add_argument('--notes-dir', default=str(DEFAULT_NOTES_DIR), help='Directory for default daily notes.')
    default_date = current_note_date()
    parser.add_argument('--date', default=default_date, help='Date used for the default file name.')
    return parser.parse_args()


def read_body(args: argparse.Namespace) -> str:
    if args.body_file:
        return Path(args.body_file).expanduser().read_text(encoding='utf-8').strip()
    return sys.stdin.read().strip()


def resolve_target(args: argparse.Namespace) -> tuple[Path, bool]:
    if args.target_file:
        return Path(args.target_file).expanduser(), False
    notes_dir = Path(args.notes_dir).expanduser()
    return notes_dir / f'{args.date}.md', True


def build_block(title: str, body: str) -> str:
    clean_title = title.strip()
    clean_body = body.strip()
    if not clean_title:
        raise ValueError('Title must not be empty.')
    if not clean_body:
        raise ValueError('Body must not be empty.')
    return f'## {clean_title}\n\n{clean_body}\n'


def append_block(target: Path, block: str, *, daily_file: bool, note_date: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)

    if not target.exists():
        if daily_file:
            target.write_text(f'# {note_date}\n\n{block}', encoding='utf-8')
        else:
            target.write_text(block, encoding='utf-8')
        return

    existing = target.read_text(encoding='utf-8')
    stripped = existing.strip()

    if not stripped:
        if daily_file:
            target.write_text(f'# {note_date}\n\n{block}', encoding='utf-8')
        else:
            target.write_text(block, encoding='utf-8')
        return

    if daily_file and stripped == f'# {note_date}':
        target.write_text(existing.rstrip() + '\n\n' + block, encoding='utf-8')
        return

    target.write_text(existing.rstrip() + '\n\n---\n\n' + block, encoding='utf-8')


def main() -> int:
    args = parse_args()
    body = read_body(args)
    target, daily_file = resolve_target(args)
    block = build_block(args.title, body)
    append_block(target, block, daily_file=daily_file, note_date=args.date)
    print(target)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
