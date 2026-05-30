#!/usr/bin/env python3
"""List, find, and extract sections from the bundled PWA skill source."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "references" / "PWA.md"
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^\s*```")


@dataclass(frozen=True)
class Heading:
    line: int
    level: int
    title: str


def read_lines() -> list[str]:
    return SOURCE.read_text(encoding="utf-8").splitlines()


def headings(lines: list[str]) -> list[Heading]:
    found: list[Heading] = []
    in_fence = False

    for index, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        match = HEADING_RE.match(line)
        if match:
            found.append(
                Heading(
                    line=index,
                    level=len(match.group(1)),
                    title=match.group(2).strip(),
                )
            )

    return found


def matching_headings(all_headings: list[Heading], query: str) -> list[Heading]:
    query_folded = query.casefold()
    return [item for item in all_headings if query_folded in item.title.casefold()]


def section_bounds(lines: list[str], all_headings: list[Heading], heading: Heading) -> tuple[int, int]:
    start = heading.line
    end = len(lines)

    for candidate in all_headings:
        if candidate.line <= heading.line:
            continue
        if candidate.level <= heading.level:
            end = candidate.line - 1
            break

    return start, end


def print_headings(all_headings: list[Heading]) -> None:
    for item in all_headings:
        indent = "  " * (item.level - 1)
        print(f"{item.line}: {indent}{'#' * item.level} {item.title}")


def print_matches(all_headings: list[Heading], query: str) -> int:
    matches = matching_headings(all_headings, query)
    for item in matches:
        indent = "  " * (item.level - 1)
        print(f"{item.line}: {indent}{'#' * item.level} {item.title}")
    return 0 if matches else 1


def print_section(lines: list[str], all_headings: list[Heading], query: str) -> int:
    matches = matching_headings(all_headings, query)
    if not matches:
        print(f"No heading matched: {query}")
        return 1

    selected = matches[0]
    start, end = section_bounds(lines, all_headings, selected)
    print(f"<!-- Source: references/PWA.md lines {start}-{end} -->")
    print("\n".join(lines[start - 1 : end]))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List markdown headings with source line numbers.")

    find_parser = subparsers.add_parser("find", help="Find headings by case-insensitive text.")
    find_parser.add_argument("query")

    extract_parser = subparsers.add_parser(
        "extract", help="Extract the first section whose heading contains the query."
    )
    extract_parser.add_argument("query")

    args = parser.parse_args()
    lines = read_lines()
    all_headings = headings(lines)

    if args.command == "list":
        print_headings(all_headings)
        return 0
    if args.command == "find":
        return print_matches(all_headings, args.query)
    if args.command == "extract":
        return print_section(lines, all_headings, args.query)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
