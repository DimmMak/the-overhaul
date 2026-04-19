#!/usr/bin/env python3
"""
stress-test.py — comprehensive fleet health check across all 3 axes.

Runs systematic tests organized by the world-class architecture:
  🌳 Tree     — WHERE things live (organizational integrity)
  🎮 Plugin   — WHAT they can do (capability contracts)
  🐧 Unix     — HOW they compose (pipe + contract compatibility)

Output: tier-list format per Danny's preferences.
Exit 0 on all-pass, 1 on any fail.

Used by:
  - User on demand (`.future-proof stress-test`)
  - Quarterly cron (via scheduled-tasks)
"""
import json
import re
import subprocess
import sys
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"
DESKTOP = Path.home() / "Desktop" / "CLAUDE CODE"
FUTURE_PROOF = Path(__file__).resolve().parent.parent
VALIDATOR = FUTURE_PROOF / "scripts" / "validate-skill.py"
FLEET_AUDIT = FUTURE_PROOF / "scripts" / "fleet-audit.py"
CROSS_AUDIT = FUTURE_PROOF / "scripts" / "cross-skill-audit.py"
CONTRACT_TESTS = FUTURE_PROOF / "tests" / "test_fund_critical.py"
VALID_DOMAINS = {"fund", "learning", "general"}
WORLD_CLASS_TAG = "v-2026-04-18-world-class"


def installed_skills():
    """Return list of (name, install_path, real_path) for every installed skill."""
    skills = []
    if not SKILLS_DIR.exists():
        return skills
    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir() and not entry.is_symlink():
            continue
        name = entry.name
        if name.startswith(".") or name.endswith((".zip", ".skill")):
            continue
        if not (entry / "SKILL.md").exists():
            continue
        skills.append((name, entry, entry.resolve()))
    return skills


def parse_frontmatter(skill_md):
    """Return raw frontmatter text between first pair of --- markers."""
    text = skill_md.read_text()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    return m.group(1) if m else None


def extract_field(fm_text, key):
    """Extract simple top-level scalar field from frontmatter."""
    if not fm_text:
        return None
    for line in fm_text.splitlines():
        m = re.match(rf"^{key}:\s*(.+?)\s*$", line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return None


# ═════════════════════════════════════════════════════════════════
# 🌳 TREE AXIS — WHERE things live
# ═════════════════════════════════════════════════════════════════

def test_tree_all_have_domain(skills):
    """Every skill's SKILL.md declares a domain."""
    missing = []
    for name, _, real in skills:
        fm = parse_frontmatter(real / "SKILL.md")
        dom = extract_field(fm, "domain")
        if not dom:
            missing.append(name)
    assert not missing, f"{len(missing)} skills missing domain: {missing}"


def test_tree_valid_domain_values(skills):
    """Every domain is one of fund/learning/general."""
    bad = []
    for name, _, real in skills:
        fm = parse_frontmatter(real / "SKILL.md")
        dom = extract_field(fm, "domain")
        if dom and dom not in VALID_DOMAINS:
            bad.append((name, dom))
    assert not bad, f"invalid domain values: {bad}"


def test_tree_all_symlinked(skills):
    """Every installed skill is a symlink to Desktop (no copies)."""
    copies = []
    for name, install, _ in skills:
        if not install.is_symlink():
            copies.append(name)
    assert not copies, f"{len(copies)} skills installed as COPY (drift risk): {copies}"


def test_tree_no_orphans():
    """Every installed skill routes to a domain via .home map logic."""
    home_py = Path.home() / ".claude" / "skills" / "home" / "scripts" / "home.py"
    if not home_py.exists():
        raise AssertionError("home.py not found — .home map can't route")
    result = subprocess.run(["python3", str(home_py), "map"], capture_output=True, text=True, timeout=10)
    assert "UNROUTED" not in result.stdout, f".home map has orphans:\n{result.stdout[-500:]}"


# ═════════════════════════════════════════════════════════════════
# 🎮 PLUGIN AXIS — WHAT they can do
# ═════════════════════════════════════════════════════════════════

def test_plugin_schema_v3_all_pass(skills):
    """Every skill passes schema v0.3 validation."""
    failed = []
    for name, _, real in skills:
        r = subprocess.run(
            ["python3", str(VALIDATOR), "--schema-version", "0.3", str(real / "SKILL.md")],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode != 0:
            failed.append(name)
    assert not failed, f"{len(failed)} skills fail v0.3: {failed}"


def test_plugin_capabilities_complete(skills):
    """Every SKILL.md has capabilities block with all 4 sub-keys."""
    issues = []
    for name, _, real in skills:
        text = (real / "SKILL.md").read_text()
        if "capabilities:" not in text:
            issues.append((name, "no capabilities block"))
            continue
        for sub in ("reads:", "writes:", "calls:", "cannot:"):
            if sub not in text:
                issues.append((name, f"missing {sub}"))
    assert not issues, f"capability issues: {issues[:5]}..." if len(issues) > 5 else f"capability issues: {issues}"


def test_plugin_not_for_clauses(skills):
    """Every description has NOT-for collision-fence clauses."""
    missing = []
    for name, _, real in skills:
        fm = parse_frontmatter(real / "SKILL.md")
        if not fm or "NOT for:" not in fm:
            missing.append(name)
    assert not missing, f"{len(missing)} skills missing NOT-for clauses: {missing}"


def test_plugin_validator_rejects_bad_skill():
    """Schema validator correctly rejects a known-bad SKILL.md."""
    import tempfile
    bad = tempfile.NamedTemporaryFile(mode="w", suffix="_SKILL.md", delete=False)
    bad.write("---\nname: bad\ndescription: too short\n---\n")
    bad.close()
    r = subprocess.run(
        ["python3", str(VALIDATOR), "--schema-version", "0.3", bad.name],
        capture_output=True, text=True,
    )
    Path(bad.name).unlink()
    assert r.returncode != 0, "validator FAILED to reject known-bad skill"


# ═════════════════════════════════════════════════════════════════
# 🐧 UNIX AXIS — HOW they compose
# ═════════════════════════════════════════════════════════════════

def test_unix_contract_complete(skills):
    """Every SKILL.md has unix_contract block with all required sub-keys."""
    issues = []
    for name, _, real in skills:
        text = (real / "SKILL.md").read_text()
        if "unix_contract:" not in text:
            issues.append((name, "no unix_contract block"))
            continue
        for sub in ("data_format:", "schema_version:", "stdin_support:", "stdout_format:", "composable_with:"):
            if sub not in text:
                issues.append((name, f"missing {sub}"))
    assert not issues, f"unix_contract issues: {issues[:5]}"


def test_unix_cross_skill_audit_clean():
    """Cross-skill-audit finds only accepted architectural deps."""
    r = subprocess.run(["python3", str(CROSS_AUDIT)], capture_output=True, text=True, timeout=15)
    # Known-accepted references per our audit
    accepted = {"price-desk", "life-coach-protocol"}
    unexpected = []
    for line in r.stdout.splitlines():
        m = re.search(r"references `([\w-]+)`", line)
        if m and m.group(1) not in accepted:
            unexpected.append(line.strip())
    assert not unexpected, f"unexpected cross-skill refs: {unexpected[:3]}"


def test_unix_fund_critical_contracts():
    """Fund-critical test harness passes (11/11)."""
    r = subprocess.run(["python3", str(CONTRACT_TESTS)], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, f"fund-critical tests failed:\n{r.stdout[-800:]}"


def test_unix_rollback_tag_exists():
    """World-class git tag exists in at least the core future-proof repo (rollback discipline)."""
    r = subprocess.run(
        ["git", "-C", str(DESKTOP / "future-proof"), "tag", "-l", WORLD_CLASS_TAG],
        capture_output=True, text=True,
    )
    assert WORLD_CLASS_TAG in r.stdout, f"rollback tag `{WORLD_CLASS_TAG}` missing from future-proof repo"


# ═════════════════════════════════════════════════════════════════
# RUNNER
# ═════════════════════════════════════════════════════════════════

AXES = [
    ("🌳 Tree", "WHERE things live", [
        ("all skills have domain",          test_tree_all_have_domain),
        ("domain values are valid",         test_tree_valid_domain_values),
        ("all skills symlinked (no copies)", test_tree_all_symlinked),
        ("no orphans in .home map",         test_tree_no_orphans),
    ]),
    ("🎮 Plugin", "WHAT they can do", [
        ("schema v0.3 validation",          test_plugin_schema_v3_all_pass),
        ("capabilities block complete",     test_plugin_capabilities_complete),
        ("NOT-for collision fences",        test_plugin_not_for_clauses),
        ("validator rejects bad skill",     test_plugin_validator_rejects_bad_skill),
    ]),
    ("🐧 Unix", "HOW they compose", [
        ("unix_contract block complete",    test_unix_contract_complete),
        ("cross-skill audit clean",         test_unix_cross_skill_audit_clean),
        ("fund-critical contracts (11/11)", test_unix_fund_critical_contracts),
        ("rollback tag exists",             test_unix_rollback_tag_exists),
    ]),
]


def main():
    skills = installed_skills()
    assert skills, "no installed skills found"

    print("=" * 70)
    print(f"🧪 FLEET STRESS TEST — {len(skills)} skills · 3 axes · 12 checks")
    print("=" * 70)

    results = []

    for axis_name, axis_desc, tests in AXES:
        print(f"\n{axis_name}   — {axis_desc}")
        print("-" * 70)
        axis_pass = 0
        axis_fail = 0
        for check_name, fn in tests:
            try:
                # Some tests need skills arg, others don't
                import inspect
                sig = inspect.signature(fn)
                if len(sig.parameters) > 0:
                    fn(skills)
                else:
                    fn()
                print(f"  🟢 {check_name}")
                axis_pass += 1
            except AssertionError as e:
                print(f"  🔴 {check_name}")
                print(f"     → {e}")
                axis_fail += 1
                results.append((axis_name, check_name, str(e)))
            except Exception as e:
                print(f"  🔴 {check_name} (exception)")
                print(f"     → {type(e).__name__}: {e}")
                axis_fail += 1
                results.append((axis_name, check_name, f"{type(e).__name__}: {e}"))
        total_axis = axis_pass + axis_fail
        verdict = "🟢 clean" if axis_fail == 0 else f"🔴 {axis_fail} failed"
        print(f"  {axis_name} axis: {axis_pass}/{total_axis} {verdict}")

    total_pass = sum(len(t[2]) for t in AXES) - len(results)
    total = sum(len(t[2]) for t in AXES)

    print()
    print("=" * 70)
    print("🏆 STRESS TEST SUMMARY")
    print("=" * 70)
    print()
    print("> 🟢 pass · 🔴 fail · 🟡 partial")
    print()
    print("| 🟣 Axis    | 🟣 Checks | 🟣 Result       |")
    print("| ---------- | --------- | --------------- |")
    for axis_name, _, tests in AXES:
        axis_failures = [r for r in results if r[0] == axis_name]
        p = len(tests) - len(axis_failures)
        icon = "🟢" if not axis_failures else "🔴"
        print(f"| {axis_name:<10} | {p}/{len(tests):<7} | {icon} {'clean' if not axis_failures else f'{len(axis_failures)} failed'}       |")
    print()
    print(f"Total: {total_pass}/{total} checks passed")

    if not results:
        print()
        print("🏆 FLEET HEALTHY — locked world-class state holds.")
        sys.exit(0)
    else:
        print()
        print("🔴 Failures:")
        for axis, check, err in results:
            print(f"  {axis} · {check}")
            print(f"     → {err[:150]}")
        print()
        print("Drift detected. Run autopsy prompt on each failure to find root cause.")
        sys.exit(1)


if __name__ == "__main__":
    main()
