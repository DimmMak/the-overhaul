#!/usr/bin/env python3
"""
cross-skill-audit.py — detect direct cross-skill calls (Unix philosophy violations).

Scans every installed skill's scripts/ and SKILL.md for hardcoded paths into
OTHER skills' internals. Anchor-routed calls (via .home/.chief/mewtwo) are fine.
Direct `~/.claude/skills/X/scripts/Y.py` from skill Z is a violation.

Usage:
  python3 cross-skill-audit.py
  python3 cross-skill-audit.py --json
"""
import json
import re
import sys
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"

# Anchor skills — legitimate cross-domain routers. Calling these is OK.
ANCHORS = {"home", "chief-of-staff", "mewtwo", "future-proof"}


def find_skill_references(skill_name, skill_path):
    """Return set of OTHER skills this skill references directly (via filesystem paths)."""
    refs = set()
    # Patterns to detect: `~/.claude/skills/X/` or `$HOME/.claude/skills/X/`
    pat = re.compile(r"(?:~|\$HOME|/Users/\w+)/\.claude/skills/([a-z][\w-]*)")
    for py_file in skill_path.rglob("*.py"):
        try:
            text = py_file.read_text(errors="ignore")
        except Exception:
            continue
        for m in pat.finditer(text):
            other = m.group(1)
            if other != skill_name and other not in ANCHORS:
                refs.add((other, py_file.relative_to(skill_path).as_posix()))
    # Also check SKILL.md body
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        text = skill_md.read_text()
        for m in pat.finditer(text):
            other = m.group(1)
            if other != skill_name and other not in ANCHORS:
                refs.add((other, "SKILL.md"))
    return refs


def main():
    as_json = "--json" in sys.argv
    results = []

    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir() and not entry.is_symlink():
            continue
        name = entry.name
        if name.startswith(".") or name.endswith((".zip", ".skill")):
            continue
        if not (entry / "SKILL.md").exists():
            continue
        # Resolve symlinks for true content
        real = entry.resolve()
        refs = find_skill_references(name, real)
        results.append({"skill": name, "violations": sorted(list(refs))})

    if as_json:
        print(json.dumps(results, indent=2))
        sys.exit(0)

    total = 0
    print("🔍 CROSS-SKILL-CALL AUDIT")
    print("=" * 60)
    for r in results:
        if r["violations"]:
            total += len(r["violations"])
            print(f"🟡 {r['skill']}")
            for other, where in r["violations"]:
                print(f"   → references `{other}` in {where}")
        else:
            pass  # clean — don't clutter
    print("=" * 60)

    if total == 0:
        print("🟢 ZERO direct cross-skill calls — anchor-only routing holds.")
        sys.exit(0)
    else:
        print(f"🟡 {total} direct reference(s) found.")
        print("   Review: are they legitimate data reads OR code imports?")
        print("   Code imports from non-anchor skills should route through .home/.chief/mewtwo.")
        sys.exit(0)  # exit 0 because some data-path references are expected/OK


if __name__ == "__main__":
    main()
