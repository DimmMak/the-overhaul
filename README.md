# 🏛️ The Overhaul

**How I architected a 20-skill AI fleet from spaghetti to world-class — in one evening.**

Half-life of the system went from **~8 months** to **~13.8 years** — a **20× durability gain** — using three orthogonal design axes, schema-enforced contracts, and a preservation cron that maintains the system with zero ongoing effort.

---

## 🎯 The elevator pitch

Most "AI skill libraries" rot within months. Descriptions blur, data drifts, dependencies die, and the system degrades silently. The Overhaul is the record of how I applied durable software architecture patterns to a personal AI fleet so that it survives decades of tool churn — provably, testably, and automatically.

```markdown
| 🟣 # | 🟣 What                                 | 🟣 Result                       |
| ---- | --------------------------------------- | ------------------------------- |
| 1    | 20 skills built ad-hoc over weeks       | Half-life ~8 months             |
| 2    | One evening of structural overhaul       | Half-life ~13.8 years           |
| 3    | Automated quarterly audit preserves it   | Decay blocked by design         |
| 4    | Pattern replicable to any domain         | Portable architecture           |
```

---

## 📚 How to read this repo

```markdown
| 🟣 If you want...                          | 🟣 Read                         |
| ------------------------------------------ | ------------------------------- |
| The full story of the evening              | [STORY.md](STORY.md)            |
| The architecture in depth                  | [ARCHITECTURE.md](ARCHITECTURE.md) |
| The rules that guided every decision       | [PRINCIPLES.md](PRINCIPLES.md)  |
| The numbers (before/after, half-life math) | [BEFORE_AND_AFTER.md](BEFORE_AND_AFTER.md) |
| What went wrong + how I fixed it           | [LESSONS_LEARNED.md](LESSONS_LEARNED.md) |
| The scripts that enforce the architecture  | [TOOLING.md](TOOLING.md)        |
| How to apply this to YOUR domain           | [REPLICATE.md](REPLICATE.md)    |
```

---

## 🏆 The three-axis model

Every system that survives decades — Unix, SQL, Git, the Web — obeys three orthogonal axes simultaneously:

```
🌳 Tree     = WHERE things live        (organizational hierarchy)
🎮 Plugin   = WHAT they can do         (capability contracts)
🐧 Unix     = HOW they compose         (pipes + stable CLI)
```

The Overhaul applies all three to an AI skill fleet. The result is a system that:

- ✅ Self-routes new skills via `domain:` frontmatter (Tree)
- ✅ Validates every skill against a schema at install time (Plugin)
- ✅ Composes via files + JSON + standardized CLI (Unix)
- ✅ Stress-tests itself in 12 checks across all three axes
- ✅ Auto-audits quarterly via cron with zero ongoing effort

---

## 📊 The numbers

```markdown
| 🟣 Metric                              | 🟣 Before | 🟣 After |
| -------------------------------------- | --------- | -------- |
| Tree axis score                        | 90%       | 99%      |
| Plugin axis score                      | 50%       | 98%      |
| Unix axis score                        | 80%       | 98%      |
| Combined half-life (years)             | ~0.67     | ~13.8    |
| Stress test checks passing             | N/A       | 12/12    |
| Fleet audit warnings                   | 3         | 0        |
| Ship time                              | n/a       | ~5 hrs   |
```

---

## 🎬 Who this is for

- 🧑‍💻 **Engineers** building agent systems who want durable architecture
- 🎓 **Architects** looking for applied case studies
- 🏢 **Teams** needing a blueprint for long-lived AI tooling
- 🤖 **Future AI operators** who inherit this kind of system cold

---

## 🔨 Tools built during the overhaul

```markdown
| 🟣 Tool              | 🟣 Purpose                                         |
| -------------------- | -------------------------------------------------- |
| `validate-skill.py`  | Schema validator (v0.1 / v0.2 / v0.3 levels)      |
| `fleet-audit.py`     | Audit all skills against schema + install pattern |
| `cross-skill-audit.py`| Detect unsanctioned direct skill-to-skill calls  |
| `stress-test.py`     | 12-check fleet stress test (tree/plugin/unix)     |
```

All in `scripts/`. All tool-independent (plain Python).

---

## 🏛️ Framing

This is not a tutorial on Claude Code or any specific AI platform. This is a **case study in durable architecture applied to AI-augmented tooling**. The principles port to any agent framework, any domain, any language runtime.

The specific skills built here manage a personal hedge fund (Blue Hill Capital). The architecture would work equally for legal case tracking, medical records, research libraries, supply chains, or any multi-component decision system.

**The domain is the shell. The structure is the substance.**

---

## 📜 License

MIT. Learn from it, remix it, ship your own version.

---

## 🙏 Credit

- **Ras Mic** — for the recursive refinement + progressive disclosure patterns that inspired snes-builder
- **Unix philosophy** (1969 Bell Labs) — the composition model is theirs, 55+ years proven
- **Built via Claude Code** (Opus 4.7, 1M context) in a single 5-hour session with the author

🏛️🃏🛡️🌳
