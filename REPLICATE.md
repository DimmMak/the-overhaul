# 🔨 Replicate — Apply This Pattern To Your Domain

**The three-axis architecture is domain-agnostic.** This repo ships a fund-management fleet as the reference implementation. The structure ports to ANY multi-component decision system.

This file is the blueprint for recreating it elsewhere.

---

## 🎯 Domains this pattern fits

```markdown
| 🟣 Tier | 🟣 # | 🟣 Domain                      | 🟣 Example skills you'd build       |
| ------- | ---- | ------------------------------ | ----------------------------------- |
| T1      | 1    | **Any AI-agent fleet**          | Custom Claude/OpenAI skill library  |
| T1      | 2    | **Legal case tracking**         | case-intake · evidence-index · filing-calendar |
| T1      | 3    | **Medical practice**            | patient-records · referral-tracker · billing-desk |
| T1      | 4    | **VC deal flow**                | company-research · diligence-check · pitch-log |
| T1      | 5    | **Real estate portfolio**       | property-desk · tenant-tracker · maintenance-log |
| T1      | 6    | **Research paper library**      | paper-index · citation-graph · experiment-log |
| T1      | 7    | **Content production pipeline** | brief-intake · draft-engine · fact-check |
| T1      | 8    | **Personal knowledge mgmt**     | notes-capture · review-cycle · connection-finder |
| ━━━━━━━ | ━━━━ | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ |
| T2      | 9    | **Fitness coaching**             | workout-tracker · meal-planner · recovery-metrics |
| T2      | 10   | **Chef / recipe development**    | recipe-lib · supplier-tracker · cost-calculator |
| T2      | 11   | **Music/video production**       | clip-library · project-tracker · export-log |
```

If your domain has:
- 🧩 Multiple skills/tools/agents that need coordination
- 📊 Data flowing between components
- 🎯 Decisions being made based on structured inputs
- 🕰️ A desire to last years, not months

→ this pattern applies.

---

## 🧬 The translation

Every fund-specific piece in the reference implementation has a domain-agnostic equivalent.

```markdown
| 🟣 # | 🟣 Fund concept (ref impl)          | 🟣 Generic concept                    |
| ---- | ----------------------------------- | ------------------------------------- |
| 1    | fund / learning / general (domains) | Your top-level groupings              |
| 2    | `.chief` (fund anchor)              | Your primary workflow anchor          |
| 3    | `.rumble` (deep research)           | Your deep-analysis skill              |
| 4    | `price-desk` (live data source)     | Your real-time data integration       |
| 5    | `accuracy-tracker` (scoring)        | Your performance feedback loop        |
| 6    | `journalist` (formatted output)     | Your publishable-artifact generator   |
| 7    | `.home` (top-level router)          | Your meta-anchor                      |
| 8    | `skill-builder` (meta-skill)        | Stays the same — domain-agnostic      |
| 9    | `future-proof` (preservation coach) | Stays the same — domain-agnostic      |
```

The meta-skills (skill-builder, future-proof) work in ANY domain without modification.

---

## 🏗️ Step-by-step replication recipe

### Phase 0 — Pick your domain + ship a working v0

**Don't start with the architecture.** Build 2-3 crappy skills first. Use them. Notice the pain. THEN apply the overhaul.

Why: you can't architect what you haven't suffered yet. Premature architecture is over-engineering.

### Phase 1 — Port the meta-skills

Copy these as-is from the reference:
- `future-proof/` — the preservation coach
- `skill-builder/` — the meta-skill for creating new skills
- `tier/` — the Risk×Reward matrix

Edit their `domain:` field to `general` in each SKILL.md. Everything else works unchanged.

### Phase 2 — Pin your principles

Copy these memory files from the reference, review, adapt where needed:
- `principle_future_proof_by_default.md` — usually unchanged
- `principle_risk_reward_rating.md` — unchanged
- `principle_earn_your_features.md` — unchanged
- `principle_single_anchor_agent.md` — adjust the anchor hierarchy for your domain
- `principle_real_life_role_naming.md` — unchanged
- `principle_maintenance_discipline.md` — adjust audit cadence if needed
- `principle_50_year_preservation.md` — usually unchanged

Everything in `memory/` is portable. Principles don't have domains.

### Phase 3 — Design your tree

Map your domain into 2-4 top-level branches. Examples:

```
Legal firm:
  cases / billing / compliance / ops

Medical practice:
  patients / scheduling / billing / research

VC fund:
  pipeline / portfolio / investors / ops
```

Three is often the sweet spot. More than four = complexity. Less than two = just use a flat list.

### Phase 4 — Build 5-10 domain-specific skills

Use skill-builder. Phase 1 gates filter out the ones that shouldn't exist.

Every skill you build inherits:
- `domain:` field → auto-routes in your map
- `capabilities:` block → declares its contract
- `unix_contract:` block → declares its I/O shape
- Validator enforcement at install
- NOT-for clauses prevent collision

### Phase 5 — Wire the anchor

Create a domain-anchor skill (like `.chief` for fund). Every domain-specific skill either:
- Dispatches through the anchor, OR
- Is referenced in the anchor's menu

The anchor IS your front door for the domain.

### Phase 6 — Set up preservation

1. Tag every repo with `v-YYYY-MM-DD-v0-shipped`
2. Run `.future-proof` for progress tracking on further builds
3. Set up quarterly cron (via scheduled-tasks MCP) for `.fleet audit`
4. Write your master architecture doc (copy this repo's ARCHITECTURE.md as template)

### Phase 7 — Test

Run `stress-test.py` against your new fleet. Should pass 12/12.
If anything fails, run the autopsy prompt and pin the fix as a rule.

---

## ⏱️ Effort estimates for a new vertical

```markdown
| 🟣 Phase | 🟣 Task                       | 🟣 Time     |
| ------- | ------------------------------ | ----------- |
| 0       | Build crappy v0 (hand-hack it) | Days-weeks  |
| 1       | Port meta-skills               | 30 min      |
| 2       | Pin principles                 | 15 min      |
| 3       | Design tree                    | 30 min      |
| 4       | Build 5-10 domain skills       | 2-4 hours each |
| 5       | Wire anchor                    | 1 hour      |
| 6       | Preservation setup             | 1 hour      |
| 7       | Stress test + fix              | 30 min      |
| **Total (after first domain)** | **~1 day** (after you've done it once) |         |
```

**First domain is slow** because you're learning the pattern. Subsequent domains are much faster — most of the infrastructure (principles, validators, schemas) is reused.

---

## 🚧 Common mistakes replicating

### Mistake 1 — Over-architect on Day 1

Symptom: spending a week designing before shipping anything.

Fix: build crappy v0 first. Suffer for a few weeks. THEN architect.

### Mistake 2 — Skip the `earn-your-features` gate

Symptom: 20 skills on Day 3, half of them unused.

Fix: run skill-builder Phase 1 gates on EVERY new skill. Default SKIP.

### Mistake 3 — Skip the autopsy loop

Symptom: same mistakes recur across sessions.

Fix: treat every fumble as a rule-mining opportunity. Pin the rule. Enforce in validator.

### Mistake 4 — Don't version your schema

Symptom: 6 months in, can't tell which skills are "new style" vs "old."

Fix: validator supports v0.1 / v0.2 / v0.3. Bump when material.

### Mistake 5 — No cold-storage backup

Symptom: GitHub goes down, everything's gone.

Fix: 3-2-1 backup rule (3 copies, 2 media, 1 offsite).

---

## 🛡️ The non-negotiables

If you port this, don't skip these. They're what makes it durable:

```markdown
| 🟣 # | 🟣 Rule                                       |
| ---- | --------------------------------------------- |
| 1    | Plain text only (markdown/JSON/YAML/Python)   |
| 2    | Git-tracked memory folder                     |
| 3    | Validator enforces schema at install time     |
| 4    | Every skill symlinked (not copied)            |
| 5    | Quarterly audit via cron                      |
| 6    | Tag milestones in git                         |
| 7    | Fumbles → autopsy → pinned rule               |
| 8    | Master architecture doc (re-onboard cold)     |
```

These 8 are the skeleton. Skip any one, and the fleet drifts within 1-2 years.

---

## 🎬 What the reference implementation teaches

Beyond the code, the reference implementation demonstrates:

1. **Principles compound** — 14 rules pinned over hours become a philosophy that compounds across sessions
2. **Specialization beats generic** — each skill does one job excellently vs many jobs average
3. **Plain text wins time** — nothing proprietary, everything grep-able
4. **Enforcement must be structural** — memory rules fire ~80%; validators fire 100%
5. **Recursive refinement is real** — every fumble → rule → fewer fumbles next session

---

## 🧬 The one-liner

> **The fund is the shell. The architecture is the substance. Strip the shell, keep the substance, re-shell in your domain. Every part of the skeleton transfers.**

---

## 📬 Contact / fork

If you port this to a domain:
- Fork the repo
- Add a README section documenting your port
- Open an issue / discussion with lessons from your replication

The goal is a growing library of ported architectures so the pattern gets refined across domains.

🔨🏛️🃏
