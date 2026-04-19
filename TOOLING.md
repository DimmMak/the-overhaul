# 🛠️ Tooling — The Scripts That Enforce The Architecture

**Four Python scripts do all the enforcement work.** No frameworks. No dependencies. Plain stdlib Python. All portable, all readable, all replaceable.

---

## 📋 The full toolkit

```markdown
| 🟣 # | 🟣 Script                       | 🟣 Purpose                               | 🟣 Runtime |
| ---- | ------------------------------- | ---------------------------------------- | ---------- |
| 1    | `validate-skill.py`             | Schema validator (v0.1/v0.2/v0.3)        | ~50ms      |
| 2    | `fleet-audit.py`                | Audit all installed skills               | ~2s        |
| 3    | `cross-skill-audit.py`          | Detect direct skill-to-skill code calls  | ~500ms     |
| 4    | `stress-test.py`                | 12 systematic checks across 3 axes       | ~30s       |
```

All in `scripts/`. All standalone — run any one without the others.

---

## 🛡️ validate-skill.py — the gate

### What it does

Reads a SKILL.md file. Parses YAML frontmatter. Validates against a schema:

```markdown
| 🟣 Schema | 🟣 Required fields                                    |
| --------- | ----------------------------------------------------- |
| v0.1      | name · domain · description (with NOT-for clauses)    |
| v0.2      | v0.1 + capabilities block (reads/writes/calls/cannot) |
| v0.3      | v0.2 + unix_contract block (format/stdin/stdout/compose) |
```

### How it's used

Called by every skill's `install.sh` BEFORE linking:

```bash
VALIDATOR="$HOME/.claude/skills/future-proof/scripts/validate-skill.py"
python3 "$VALIDATOR" --schema-version 0.3 "$SRC/SKILL.md" || {
  echo "❌ SKILL.md failed schema v0.3 validation — install aborted"
  exit 1
}
```

**Non-compliant skills cannot enter the fleet.** That's the bright line.

### Example output (bad skill)

```
❌ /tmp/bad.md: 4 violation(s)
   - missing required field: `domain`
   - missing required `capabilities:` block (v0.2+ requires reads/writes/calls/cannot)
   - description too short (5 chars) — minimum 50
   - missing `NOT for:` collision-fence clauses in description
```

### Example output (good skill)

```
✅ /Users/danny/Desktop/CLAUDE CODE/price-desk/SKILL.md: passes schema v0.3
```

---

## 🔍 fleet-audit.py — the scanner

### What it does

Walks every skill in `~/.claude/skills/`, runs the validator against each, plus checks:
- Is this a symlink (good) or copy (drift risk)?
- Does it have a `data/` folder (honoring capability boundary)?
- Schema v0.3 compliance

### How it's used

Run on demand: `.fleet audit` or `python3 fleet-audit.py`.
Also called by the quarterly cron.

### Example output

```
🔍 FLEET AUDIT — 20 skills
============================================================
🟢 🔗 accuracy-tracker
🟢 🔗 archive
🟢 🔗 cash-out
🟢 🔗 chief-of-staff
🟢 🔗 courserafied
...
============================================================
Pass: 20  |  Fail: 0  |  Warnings: 0
```

(🔗 = symlinked, 📄 = copy.)

---

## 🧬 cross-skill-audit.py — the composition police

### What it does

Scans every installed skill's Python + SKILL.md for hardcoded paths like:
```
~/.claude/skills/OTHER-SKILL/
```

Flags any found. Accepts legitimate CLI calls to data desks as Unix composition (not violations). Flags true import violations.

### How it's used

Run quarterly (or on demand): `python3 cross-skill-audit.py`.

### Example output

```
🔍 CROSS-SKILL-CALL AUDIT
============================================================
🟡 royal-rumble
   → references `price-desk` in SKILL.md
🟡 life-coach
   → references `life-coach-protocol` in SKILL.md
============================================================
🟡 2 direct reference(s) found.
   Review: are they legitimate data reads OR code imports?
```

**Both above are accepted** — royal-rumble calling price-desk's CLI is Unix-style composition (stable CLI + JSON output). Life-coach references its SPAWNED skill (life-coach-protocol), which it creates.

---

## 🧪 stress-test.py — the capstone

### What it does

12 checks across 3 axes:

```
🌳 Tree (4):     domain declared · values valid · symlinked · no orphans
🎮 Plugin (4):   schema v0.3 · capabilities complete · NOT-for clauses · validator rejects bad
🐧 Unix (4):     unix_contract complete · cross-skill audit clean · fund tests 11/11 · rollback tag
```

### How it's used

Multiple invocation patterns all fire the same script via future-proof skill:
- `.future-proof stress-test`
- `stress test the fleet`
- `run all tests`
- `verify the fleet`

Quarterly cron fires it automatically.

### Example output (clean)

```
======================================================================
🧪 FLEET STRESS TEST — 20 skills · 3 axes · 12 checks
======================================================================

🌳 Tree   — WHERE things live
----------------------------------------------------------------------
  🟢 all skills have domain
  🟢 domain values are valid
  🟢 all skills symlinked (no copies)
  🟢 no orphans in .home map
  🌳 Tree axis: 4/4 🟢 clean

🎮 Plugin   — WHAT they can do
----------------------------------------------------------------------
  🟢 schema v0.3 validation
  🟢 capabilities block complete
  🟢 NOT-for collision fences
  🟢 validator rejects bad skill
  🎮 Plugin axis: 4/4 🟢 clean

🐧 Unix   — HOW they compose
----------------------------------------------------------------------
  🟢 unix_contract block complete
  🟢 cross-skill audit clean
  🟢 fund-critical contracts (11/11)
  🟢 rollback tag exists
  🐧 Unix axis: 4/4 🟢 clean

======================================================================
🏆 STRESS TEST SUMMARY: 12/12 passed
🏆 FLEET HEALTHY — locked world-class state holds.
======================================================================
```

### Exit codes

- Exit 0 = all 12 pass → fleet healthy
- Exit 1 = any fail → drift detected, autopsy workflow triggers

---

## 🛡️ How they compose

### Install-time chain

```
User runs install.sh:
  ↓
install.sh calls validate-skill.py
  ↓
if FAIL → reject + abort install
if PASS → create symlink → skill enters fleet
```

### Runtime chain

```
User types "stress test the fleet":
  ↓
future-proof skill fires (auto-match on trigger phrase)
  ↓
future-proof dispatches to stress-test.py
  ↓
stress-test.py internally calls:
  - validate-skill.py (per skill, schema check)
  - fleet-audit.py logic (install-type check)
  - cross-skill-audit.py (composition check)
  - test_fund_critical.py (contract test)
  ↓
Report pass/fail per axis in tier table
```

### Quarterly chain (fully automated)

```
Cron fires (1st of each 3rd month, 9am):
  ↓
scheduled-tasks MCP triggers Claude
  ↓
Claude runs stress-test.py
  ↓
If pass → ROADMAP.md change log entry "audit clean"
If fail → autopsy + notify user
  ↓
Auto-commit + push per memory auto-commit rule
```

---

## 🏛️ Design principles behind the tooling

### 1. Small tools, one job each
Each script does ONE thing. Validator doesn't audit. Audit doesn't stress-test. Stress-test COMPOSES the others via subprocess calls — Unix pattern.

### 2. Plain Python, stdlib only
No frameworks. No pip installs. No virtualenv required. `python3 script.py` just works, now and in 20 years.

### 3. JSON output option
Every script supports `--json` for machine-readable output. Composable with other tools (jq, grep, etc.).

### 4. Exit codes that matter
0 = success. 1 = failure. Predictable. Pipeable. CI-friendly.

### 5. Self-documenting
Every script has a docstring at the top explaining purpose, usage, and exit codes. No README hunt required.

---

## 📂 File locations

All scripts live in:
```
~/Desktop/CLAUDE CODE/future-proof/scripts/
  ├── validate-skill.py
  ├── fleet-audit.py
  ├── cross-skill-audit.py
  └── stress-test.py

~/Desktop/CLAUDE CODE/future-proof/tests/
  └── test_fund_critical.py   (called by stress-test.py)

~/Desktop/CLAUDE CODE/future-proof/data/
  └── skill-md-schema.json     (formal schema, referenced by validator)
```

Copies of each script are in this repo's `scripts/` folder as a snapshot.

---

## 🧬 Replicating in your own project

To port the toolkit to a different skill fleet:

1. Copy all 4 scripts to your `your-project/scripts/`
2. Adjust paths (SKILLS_DIR, etc.) to your repo layout
3. Write `your-project/data/skill-md-schema.json` matching your schema
4. Add validator hook to your install.sh
5. Set up cron via `scheduled-tasks` MCP (or native cron)

Total port effort: **~30 minutes.** The scripts are small + dependency-free.

---

## 🧬 The one-liner

> **Four scripts. No frameworks. Plain Python. They're the immune system — rejecting bad skills at install, detecting drift quarterly, and giving you a one-phrase health check anytime.**

🛠️🃏🛡️
