#!/usr/bin/env python3
"""Validate the web-layout-audit skill package without relying on external state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any

import yaml


EXPECTED_SOURCE_HASH = "F3BBE17E602D8F76097467EF4FD21DCC1C4B3AF7382BA9D6756CF1F14A531973"
MAX_DESCRIPTION_CHARS = 1024
MAX_SKILL_BODY_LINES = 500

REQUIRED_FILES = [
    "SKILL.md",
    "references/PWA.md",
    "references/source-map.md",
    "references/01-foundations-and-quickstart.md",
    "references/02-correction-playbook.md",
    "references/03-native-app-conversion.md",
    "references/04-audit-checklist.md",
    "references/05-code-patterns-library.md",
    "references/06-failure-modes-matrices-references.md",
    "references/07-bottom-nav-pwa-safe-area.md",
    "references/08-online-pwa-symptom-fix-catalog.md",
    "references/09-playwright-pwa-device-simulation.md",
    "scripts/pwa_section.py",
    "scripts/scan_pwa_static.py",
    "scripts/probe_ui_runtime.py",
    "scripts/simulate_pwa_devices.py",
    "scripts/validate_skill_package.py",
    "assets/audit-report-template.md",
    "assets/correction-record-template.md",
    "assets/verification-matrix-template.md",
    "assets/ui-intent-device-audit-template.md",
    "assets/runtime-probe-report-template.md",
    "assets/bottom-nav-pwa-audit-template.md",
    "assets/pwa-symptom-fix-audit-template.md",
    "assets/pwa-device-simulation-report-template.md",
]

SOURCE_SLICES = [
    "references/01-foundations-and-quickstart.md",
    "references/02-correction-playbook.md",
    "references/03-native-app-conversion.md",
    "references/04-audit-checklist.md",
    "references/05-code-patterns-library.md",
    "references/06-failure-modes-matrices-references.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def add(checks: list[dict[str, Any]], ok: bool, name: str, detail: Any = None, severity: str = "critical") -> None:
    checks.append({"ok": ok, "name": name, "severity": severity, "detail": detail})


def validate_skill(root: Path, zip_path: Path | None = None) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    skill_md = root / "SKILL.md"
    add(checks, skill_md.exists(), "SKILL.md exists")

    frontmatter: dict[str, Any] = {}
    body = ""
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---", content, re.S)
        add(checks, bool(match), "frontmatter block exists")
        if match:
            frontmatter = yaml.safe_load(match.group(1)) or {}
            body = content.split("---", 2)[-1]
            add(checks, frontmatter.get("name") == root.name, "frontmatter name matches folder", frontmatter.get("name"))
            description = frontmatter.get("description", "")
            add(checks, isinstance(description, str) and bool(description.strip()), "description exists")
            add(checks, len(description) <= MAX_DESCRIPTION_CHARS, "description under 1024 characters", len(description))
            add(checks, "<" not in description and ">" not in description, "description has no angle brackets")
            add(checks, len(body.splitlines()) <= MAX_SKILL_BODY_LINES, "SKILL.md body under 500 lines", len(body.splitlines()), "warning")
            add(checks, all(ord(char) < 128 for char in content), "SKILL.md is ASCII-only", severity="warning")

    for relative in REQUIRED_FILES:
        add(checks, (root / relative).exists(), f"required file exists: {relative}")

    source = root / "references" / "PWA.md"
    if source.exists():
        source_hash = sha256(source)
        add(checks, source_hash == EXPECTED_SOURCE_HASH, "full PWA source hash matches expected", source_hash)
        source_lines = source.read_text(encoding="utf-8").splitlines()
        combined_lines: list[str] = []
        for relative in SOURCE_SLICES:
            path = root / relative
            if path.exists():
                combined_lines.extend(path.read_text(encoding="utf-8").splitlines())
        add(checks, combined_lines == source_lines, "split references recombine to full source", {"source_lines": len(source_lines), "combined_lines": len(combined_lines)})

    all_files = [path for path in root.rglob("*") if path.is_file()]
    relative_files = [str(path.relative_to(root)).replace("\\", "/") for path in all_files]
    add(checks, not any(Path(name).name.lower().startswith("readme") for name in relative_files), "no README inside skill")
    add(checks, not any("__pycache__" in name or name.endswith(".pyc") for name in relative_files), "no Python cache files inside skill")
    add(checks, not any(name.startswith(".") or "/." in name for name in relative_files), "no hidden files inside skill", severity="warning")

    for relative in [
        "scripts/pwa_section.py",
        "scripts/scan_pwa_static.py",
        "scripts/probe_ui_runtime.py",
        "scripts/simulate_pwa_devices.py",
        "scripts/validate_skill_package.py",
    ]:
        path = root / relative
        if path.exists():
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
                add(checks, True, f"script syntax valid: {relative}")
            except SyntaxError as error:
                add(checks, False, f"script syntax valid: {relative}", str(error))

    if zip_path:
        add(checks, zip_path.exists(), "zip exists", str(zip_path))
        if zip_path.exists():
            with zipfile.ZipFile(zip_path) as archive:
                entries = sorted(item.filename for item in archive.infolist())
            expected_entries = {f"{root.name}/{name}" for name in relative_files}
            add(checks, set(entries) == expected_entries, "zip entries match skill files", {"zip_entries": len(entries), "skill_files": len(relative_files)})
            add(checks, not any("__pycache__" in name or name.endswith(".pyc") for name in entries), "zip has no Python cache files")

    failed = [check for check in checks if not check["ok"] and check["severity"] == "critical"]
    warnings = [check for check in checks if not check["ok"] and check["severity"] == "warning"]
    return {
        "ok": not failed,
        "summary": {
            "checks": len(checks),
            "failed": len(failed),
            "warnings": len(warnings),
            "files": len(relative_files),
        },
        "checks": checks,
    }


def print_text(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print(
        "Skill package validation: "
        f"{'OK' if report['ok'] else 'FAILED'} "
        f"({summary['checks']} checks, {summary['failed']} failed, {summary['warnings']} warnings)"
    )
    for check in report["checks"]:
        prefix = "OK" if check["ok"] else check["severity"].upper()
        detail = "" if check["detail"] is None else f" - {check['detail']}"
        print(f"[{prefix}] {check['name']}{detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", nargs="?", default=".", help="Skill folder to validate.")
    parser.add_argument("--zip", dest="zip_path", help="Optional zip file to verify against the folder.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    report = validate_skill(Path(args.skill_dir).resolve(), Path(args.zip_path).resolve() if args.zip_path else None)
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print_text(report)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
