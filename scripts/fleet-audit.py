#!/usr/bin/env python3
"""
fleet-audit.py — Audit every installed skill against the schema + capability contract.

Used by `.fleet audit` command (or direct invocation).

Usage:
  python3 fleet-audit.py              # audit all installed skills
  python3 fleet-audit.py --strict     # fail on any warning
  python3 fleet-audit.py --json       # machine-readable output
"""
import json
import os
import subprocess
import sys
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"
VALIDATOR = Path(__file__).resolve().parent / "validate-skill.py"


def find_skills():
    """List every installed skill (directory with SKILL.md)."""
    if not SKILLS_DIR.exists():
        return []
    skills = []
    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir() and not entry.is_symlink():
            continue
        name = entry.name
        if name.startswith(".") or name.endswith(".zip") or name.endswith(".skill"):
            continue
        skill_md = entry / "SKILL.md"
        if skill_md.exists():
            skills.append((name, entry, skill_md))
    return skills


def audit_skill(name, path, skill_md):
    """Run validator + structural checks. Returns dict with status + issues."""
    issues = []
    warnings = []

    # Run schema validator at v0.2
    try:
        result = subprocess.run(
            ["python3", str(VALIDATOR), "--schema-version", "0.2", str(skill_md)],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0:
            # Parse errors from stderr
            for line in result.stderr.splitlines():
                line = line.strip()
                if line.startswith("-"):
                    issues.append(line.lstrip("- ").strip())
                elif line.startswith("❌"):
                    # header line with count; skip
                    pass
    except Exception as e:
        issues.append(f"validator failed: {e}")

    # Structural check — is this a symlink? (better for drift-avoidance)
    if path.is_symlink():
        install_type = "symlink"
    elif path.is_dir():
        install_type = "copy"
        warnings.append("installed as COPY — edits to source won't propagate (re-install as symlink)")
    else:
        install_type = "unknown"

    # Structural check — does the skill have a data/ folder separate from other skills?
    # (capability-honoring check)
    data_dir = path / "data"
    has_data_dir = data_dir.exists() and data_dir.is_dir()

    status = "pass" if not issues else "fail"
    return {
        "name": name,
        "status": status,
        "install_type": install_type,
        "has_data_dir": has_data_dir,
        "issues": issues,
        "warnings": warnings,
    }


def main():
    strict = "--strict" in sys.argv
    as_json = "--json" in sys.argv

    skills = find_skills()
    if not skills:
        print("🔴 no skills found in", SKILLS_DIR)
        sys.exit(1)

    results = [audit_skill(name, path, md) for name, path, md in skills]

    if as_json:
        print(json.dumps(results, indent=2))
        sys.exit(0 if all(r["status"] == "pass" for r in results) else 1)

    # Human-readable report
    pass_count = sum(1 for r in results if r["status"] == "pass")
    fail_count = len(results) - pass_count
    warn_count = sum(len(r["warnings"]) for r in results)

    print(f"🔍 FLEET AUDIT — {len(results)} skills")
    print("=" * 60)

    for r in results:
        icon = "🟢" if r["status"] == "pass" else "🔴"
        inst = "🔗" if r["install_type"] == "symlink" else "📄"
        print(f"{icon} {inst} {r['name']}")
        for issue in r["issues"]:
            print(f"    ❌ {issue}")
        for warn in r["warnings"]:
            print(f"    ⚠️  {warn}")

    print("=" * 60)
    print(f"Pass: {pass_count}  |  Fail: {fail_count}  |  Warnings: {warn_count}")

    if fail_count > 0:
        sys.exit(1)
    if strict and warn_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
