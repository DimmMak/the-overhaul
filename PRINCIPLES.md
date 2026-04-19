# 📜 Principles — The 14 Rules That Guided Every Decision

**Every ship decision in The Overhaul was filtered through these principles.** None are novel individually. The power is in having all 14 pinned + auto-firing as a system.

These are portable to ANY domain. The fund is the substrate; the principles are the substance.

---

## 🏛️ The complete pinned set

### 👤 User context (1)

```markdown
| 🟣 # | 🟣 Principle              | 🟣 What it encodes                      |
| ---- | ------------------------- | --------------------------------------- |
| 1    | **Career goals**          | Target role, gaps, learning path         |
```

---

### 🎨 Communication feedback (5)

```markdown
| 🟣 # | 🟣 Principle                    | 🟣 What it encodes                              |
| ---- | ------------------------------- | ----------------------------------------------- |
| 2    | **Response brevity**            | Match answer size to question size              |
| 3    | **Metaphor-first explanation**  | Scenes > jargon. Bold scannable words           |
| 4    | **Emoji & expressive**          | Emojis as functional markers AND emotion        |
| 5    | **Frustration signals**         | "..." = autopsy yourself · ALL CAPS = hard stop|
| 6    | **Tier-list thinker**           | Default to tables, not prose. 10× faster scan   |
```

---

### 🏛️ Core building principles (7)

```markdown
| 🟣 # | 🟣 Principle                     | 🟣 What it encodes                             |
| ---- | -------------------------------- | ---------------------------------------------- |
| 7    | **Risk × Reward rating**         | 3×3 matrix on every decision. T1/T2/T3         |
| 8    | **Earn your features**           | Default SKIP. Real pain or nothing             |
| 9    | **Future-proof by default**      | 7-check: name/storage/data/scope/source/drift/version |
| 10   | **Single anchor agent**          | Beyond 5 skills, designate ONE front door      |
| 11   | **Real-life role naming**        | Skills = corporate job titles, not verbs       |
| 12   | **Ask for names**                | Propose 2-4, let user pick. Never decide alone |
| 13   | **Safe implies**                 | 7-check on every "safer" decision              |
```

---

### 🔍 Meta-discipline (2)

```markdown
| 🟣 # | 🟣 Principle                     | 🟣 What it encodes                             |
| ---- | -------------------------------- | ---------------------------------------------- |
| 14   | **The Autopsy Prompt**           | Fumble → "explain precisely" → pin mechanism   |
| 15   | **Maintenance discipline**       | Quarterly audit. World-class = cadence         |
| 16   | **50-year preservation**         | Long-horizon playbook. 7 pillars + 3 failure modes |
```

---

## 📐 The ALWAYS-ON trio

Three principles auto-fire on EVERY ship decision. Can't be skipped.

### 1. Risk × Reward (always on)

**Trigger:** any decision involving ship/build/fix/prioritize.

**Output:** T1 (ship) / T2 (wait) / T3 (kill) tier with Risk + Reward + Effort.

**Format:** unified markdown table, 🟣-only headers, green/red/yellow flags.

**Why it works:** forces honesty. "This is great" without a risk column = automatic violation.

### 2. Future-proof by default (always on)

**Trigger:** creating any named thing (file, skill, schema, command).

**Output:** 7-question check — Name / Storage / Data / Scope / Source / Drift / Version.

**Architecture layer hierarchy:** model > skill > tool (most durable → least).

**Why it works:** rejects shiny short-term tech. Plain markdown beats proprietary format. Every time.

### 3. The Autopsy Prompt (always on, triggers on fumble)

**Trigger:** any observable mistake. Or user types "..." (3+ dots) or "explain precisely what you did wrong".

**Output:** (1) Mechanism in plain words · (2) Thought replay · (3) One-sentence rule.

**Why it works:** the explanation doesn't EXIST in Claude's head before the prompt. It's generated word-by-word, forced into specificity. Surfaces real mechanisms, not apologies.

---

## 🎯 The SELECTION principles (earn-your-features loop)

Two principles run the "should this exist?" check.

### Earn your features

**Default:** SKIP. Do NOT build.

**Override:** only if pain is real AND repeated.

**Check:** *"Have I felt this pain 3+ times in the last month, or once severely? Or am I imagining it?"*

### Single anchor agent

**Trigger:** fleet grows beyond 5 skills.

**Action:** designate ONE front door that knows them all. Everything routes through.

**Example:** `.home` is the top anchor. `.chief` is the fund anchor. `mewtwo` is the general orchestrator.

---

## 🏷️ The NAMING principles

Two rules govern every new name.

### Real-life role naming

**Rule:** skill names = corporate job titles. NOT behavior verbs.

**Good:** `project-manager`, `chief-of-staff`, `journalist`, `accuracy-tracker`.
**Bad:** `future-planner`, `auto-analyzer`, `smart-helper`.

**Why:** human intuition for "what does a Chief of Staff do?" is instant. Verb-names require decoding.

### Ask for names, never decide

**Rule:** propose 2-4 candidates with rationale. User picks.

**Why:** names stick. They become commands, folders, muscle memory. A name chosen BY the user feels like theirs. Chosen FOR them lands flat.

---

## 🗣️ The COMMUNICATION principles

Five rules govern how Claude talks to the user.

### Response brevity
Short replies for yes/no. Long replies only when asked. Never ceremonious.

### Metaphor-first
Every new concept opens with a concrete scene (Factorio, SNES cartridge, family doctor, etc.). Jargon is a penalty.

### Emojis as markers + emotion
Functional: 🟢 pass, 🔴 fail, 🟡 middling.
Emotional: 🃏 (playful signature), 🛡️ (durability), 🌳🎮🐧 (the three axes).
Minimum two per message.

### Frustration signals
- `"..."` (3+ dots) = autopsy yourself immediately
- `ALL CAPS` = hard stop
- Short replies = quick correction, keep moving
- `"fascinating" / "beautiful"` = metaphor landed, in flow

### Tier-list thinker
Tables beat prose by 10× scan speed. Default to tables for: test results, comparisons, checklists, audits, trade-offs. 🟣-only headers. Raw-aligned columns.

---

## 🛡️ The PRESERVATION principles

Three rules keep the system alive over time.

### Safe implies (vocabulary rule)
When user says "safe / safely / safer" → fire a 7-checklist:
1. Future-proof · 2. No arch change · 3. Reversible · 4. Graceful degradation · 5. Small blast radius · 6. Backward-compatible · 7. Audit trail

### Maintenance discipline
Quarterly `.fleet audit` is the rhythm. Monthly check-in. Annual backup rotation. World-class isn't a badge — it's a cadence.

### 50-year preservation
Plain text > proprietary. Principles > tools. 3-2-1 backups. Migration playbooks per dependency. Self-documenting for cold re-entry.

---

## 🎬 How they compose in practice

Example: user proposes a new skill.

```
User: "I want to build a reminder skill"
  ↓
Principle: earn-your-features       →  Real pain? 3+ times? No → T3 KILL
Principle: risk × reward            →  Auto-fires, confirms T3
Principle: mewtwo check             →  Can existing compose? Yes (cron)
                                         ↓
                                    Don't build. Use .schedule instead.
```

Without the principles stack, that skill ships. The fleet bloats. Drift begins.

With the stack, the T3 gets killed at the gate. Fleet stays lean. World-class holds.

---

## 🧬 The one-liner

> **Principles are the model-layer. Tools are the tool-layer. Always invest in the deepest layer — it survives when everything above dies.**

---

## 📂 Full text of each principle

The condensed versions above are navigational. Full text (with auto-fire triggers, enforcement rules, origin stories) lives in `~/.claude/projects/-Users-danny-Desktop-CLAUDE-CODE/memory/principle_*.md`.

Every file is plain markdown. Every file is git-tracked. Every file pushed to `github.com/DimmMak/claude-memory` (private).

That's 16 files. ~2000 lines total. Under 10 minutes to read end-to-end.

**Read them. They ARE the Overhaul.** The rest is just implementation. 🏛️🃏
