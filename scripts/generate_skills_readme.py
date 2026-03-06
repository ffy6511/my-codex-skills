#!/usr/bin/env python3
"""Generate a README skills section from agents/openai.yaml files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

START_MARKER = "<!-- skills:start -->"
END_MARKER = "<!-- skills:end -->"


def find_openai_yaml_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for path in root.rglob("openai.yaml"):
        if ".git" in path.parts or ".system" in path.parts:
            continue
        files.append(path)
    return sorted(files)


def _try_parse_with_pyyaml(text: str) -> Dict[str, str]:
    try:
        import yaml  # type: ignore
    except Exception:
        return {}

    try:
        data = yaml.safe_load(text) or {}
    except Exception:
        return {}

    interface = data.get("interface") if isinstance(data, dict) else {}
    if not isinstance(interface, dict):
        return {}

    return {
        "display_name": str(interface.get("display_name") or "").strip(),
        "short_description": str(interface.get("short_description") or "").strip(),
        "default_prompt": str(interface.get("default_prompt") or "").strip(),
    }


def _strip_wrapping_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_interface_fallback(text: str) -> Dict[str, str]:
    lines = text.splitlines()
    in_interface = False
    interface_indent = 0
    parsed: Dict[str, str] = {
        "display_name": "",
        "short_description": "",
        "default_prompt": "",
    }

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        if not in_interface:
            if re.match(r"^\s*interface\s*:\s*$", line):
                in_interface = True
                interface_indent = indent
            idx += 1
            continue

        if stripped and indent <= interface_indent and not stripped.startswith("#"):
            break

        key_match = re.match(r"^\s*([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
        if not key_match:
            idx += 1
            continue

        key, raw_value = key_match.group(1), key_match.group(2)
        if key not in parsed:
            idx += 1
            continue

        raw_value = raw_value.rstrip()
        if raw_value in {"|", ">"}:
            block_indent = None
            block_lines: List[str] = []
            idx += 1
            while idx < len(lines):
                block_line = lines[idx]
                block_stripped = block_line.strip()
                block_current_indent = len(block_line) - len(block_line.lstrip(" "))

                if block_stripped == "":
                    block_lines.append("")
                    idx += 1
                    continue

                if block_indent is None:
                    block_indent = block_current_indent
                if block_current_indent < (block_indent or 0):
                    break

                block_lines.append(block_line[(block_indent or 0) :])
                idx += 1

            parsed[key] = "\n".join(block_lines).strip()
            continue

        parsed[key] = _strip_wrapping_quotes(raw_value)
        idx += 1

    return parsed


def parse_openai_yaml(path: Path) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8")
    parsed = _try_parse_with_pyyaml(text)
    if parsed and any(parsed.values()):
        return parsed
    return _parse_interface_fallback(text)


def build_entries(paths: Iterable[Path]) -> List[Tuple[str, str, str]]:
    entries: List[Tuple[str, str, str]] = []
    for path in paths:
        parsed = parse_openai_yaml(path)
        skill_name = path.parent.parent.name
        display_name = parsed["display_name"] or skill_name
        short_description = parsed["short_description"] or "N/A"
        default_prompt = parsed["default_prompt"] or "N/A"
        entries.append((display_name, short_description, default_prompt))

    entries.sort(key=lambda item: item[0].casefold())
    return entries


def render_entries(entries: Iterable[Tuple[str, str, str]]) -> str:
    chunks: List[str] = []
    for display_name, short_description, default_prompt in entries:
        chunks.append(f"### {display_name}\n")
        chunks.append(f"{short_description}\n")
        chunks.append("<details>")
        chunks.append("<summary>default_prompt</summary>\n")
        chunks.append("````text")
        chunks.append(default_prompt)
        chunks.append("````\n")
        chunks.append("</details>\n")

    return "\n".join(chunks).strip() + "\n"


def update_readme(readme_path: Path, generated: str) -> bool:
    existing = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    if START_MARKER in existing and END_MARKER in existing:
        start_idx = existing.index(START_MARKER)
        end_idx = existing.index(END_MARKER)
        if end_idx < start_idx:
            raise ValueError("README marker order is invalid")

        before = existing[:start_idx].rstrip()
        after = existing[end_idx + len(END_MARKER) :].lstrip("\n")
        new_text = (
            f"{before}\n\n{START_MARKER}\n"
            f"{generated}"
            f"{END_MARKER}\n"
            f"{after}"
        )
        readme_path.write_text(new_text.rstrip() + "\n", encoding="utf-8")
        return True

    prefix = existing.rstrip()
    section = (
        "## Skills\n\n"
        f"{START_MARKER}\n"
        f"{generated}"
        f"{END_MARKER}\n"
    )

    if prefix:
        new_text = f"{prefix}\n\n{section}"
    else:
        new_text = section

    readme_path.write_text(new_text, encoding="utf-8")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Scan openai.yaml files and refresh the README skills section between markers."
        )
    )
    parser.add_argument("--root", default=".", help="Repository root to scan")
    parser.add_argument("--readme", default="README.md", help="README file path")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated section only and do not write files",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    readme_path = Path(args.readme).resolve()

    files = find_openai_yaml_files(root)
    entries = build_entries(files)
    generated = render_entries(entries)

    if args.dry_run:
        print(generated, end="")
        return 0

    had_markers = update_readme(readme_path, generated)
    action = "updated existing marker block" if had_markers else "created marker block"
    print(f"Processed {len(files)} openai.yaml files; {action} in {readme_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
