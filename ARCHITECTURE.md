# 🏛️ Architecture — The Three-Axis Model

**Every system that survives decades obeys three orthogonal axes simultaneously.** The Overhaul applies all three to an AI skill fleet.

---

## 🎯 The core claim

You can score any piece of software on three axes:

```
🌳 Tree axis    = organizational — WHERE does each piece live?
🎮 Plugin axis  = isolation      — WHAT can each piece do?
🐧 Unix axis    = composition    — HOW do pieces combine?
```

A system's **half-life** (how long it survives before drift/decay) is **multiplicative** across all three:

```
P(survive Y years) = tree^Y × plugin^Y × unix^Y
```

The WEAKEST axis dominates. Fix the weakest first — the leverage is highest there.

---

## 🌳 Axis 1 — Tree (WHERE things live)

### The principle

Every piece of the system has **one parent**, one canonical location, one unambiguous path from root. Tree > graph because tree has one clear ownership; graph has distributed responsibility (= nobody's responsibility).

### The fleet implementation

```
.home (top anchor)
 ├── 🏦 fund domain
 │    ├── royal-rumble · price-desk · fundamentals-desk · technicals-desk
 │    ├── accuracy-tracker · journalist · chief-of-staff
 │
 ├── 🎓 learning domain
 │    ├── courserafied · study-buddy
 │
 └── 🧰 general domain
      ├── mewtwo · home · snes-builder · future-proof · tier
      ├── archive · time-machine · cash-out · life-coach
      ├── project-manager · promptlatro
```

Every skill declares its domain in SKILL.md frontmatter:

```yaml
---
name: royal-rumble
domain: fund
---
```

The routing layer (`home.py`) reads `domain:` from each SKILL.md and auto-places the skill in the correct branch. **No hardcoded lookup table.** If a new skill ships without a valid domain, `.home map` yells at you loudly:

```
⚠️  UNROUTED SKILLS (missing or invalid domain: in SKILL.md):
    • ghost-skill  ← add valid domain to SKILL.md frontmatter
```

### Why tree wins long-term

| 🟣 # | 🟣 Alternative    | 🟣 Problem                                        |
| ---- | ----------------- | ------------------------------------------------ |
| 1    | Flat namespace    | Collisions, no organization                      |
| 2    | Graph (multi-parent)| Shared ownership = nobody's responsibility       |
| 3    | Radial (all pull from center)| Multi-parent dependency temptation      |
| 4    | **Tree (one parent)**| 🟢 Clear ownership, reasonable scope, survivable |

Every successful hierarchy in computing — file systems, git commits, DNS, class inheritance, org charts — is a tree.

---

## 🎮 Axis 2 — Plugin (WHAT things can do)

### The principle

Every component declares explicitly:
- What it reads
- What it writes
- What it calls
- What it **cannot** do

The declaration is machine-checkable. The system rejects components that don't declare, or declare invalidly.

### The SNES cartridge metaphor

```
          ┌─────────────────────────────┐
          │      CONSOLE (HOST)         │
          │  ──────────────────────     │
          │  • runs the cartridge       │
          │  • can eject anytime        │
          │  • controls power/memory    │
          │  ▲  reads cart              │
          └──┼──────────────────────────┘
             │
       ┌─────┴──────────────┐
       │   CARTRIDGE        │
       │   ───────────      │
       │  • exposes ROM     │
       │  • CAN'T write     │
       │    to console      │
       │  • plug-and-play   │
       └────────────────────┘
```

SNES lasted 10+ years because:
1. **Fixed contract** — every cart fits every slot
2. **Read-only upward** — bad cart can't brick the console
3. **Host manages cart** — console decides what runs when
4. **No cart-to-cart communication** — isolation guaranteed

The Overhaul applies the same four guarantees to skills.

### The fleet implementation

Every SKILL.md has a `capabilities:` block:

```yaml
capabilities:
  reads:
    - "royal-rumble/data/predictions.json"
    - "price-desk output"
  writes:
    - "accuracy-tracker/data/*.jsonl"
  calls:
    - "price-desk (via .price)"
  cannot:
    - "modify other skills' data"
    - "create new predictions"
    - "write outside own data folder"
```

The `capabilities` block is:
- **Declared** at authoring time
- **Validated** at install time by `validate-skill.py` (schema v0.2+)
- **Audited** periodically by `fleet-audit.py`
- **Documented** in the master architecture doc

### What's enforced vs what's declarative

Honest distinction:

```markdown
| 🟣 Layer                         | 🟣 Enforcement                        |
| -------------------------------- | ------------------------------------- |
| Install-time schema validation   | 🟢 Hard — rejects at install         |
| Runtime capability check         | 🔴 Not built (over-engineering)       |
| Declarative contract in SKILL.md | 🟢 Hard via schema                    |
| Fleet audit (catches drift)      | 🟡 Periodic — weekly/quarterly        |
```

The declaration layer is enough for this system's scale. OS-level sandboxing would be over-engineering.

---

## 🐧 Axis 3 — Unix (HOW things compose)

### The principle

Small tools. One job each. Stable interfaces. Stdin/stdout composition.

```bash
# 55-year-old pattern still works:
cat log.txt | grep ERROR | wc -l
```

Each program knows NOTHING about the others. They compose via text streams.

### The fleet implementation

Every SKILL.md has a `unix_contract:` block:

```yaml
unix_contract:
  data_format: "jsonl"
  schema_version: "0.1.0"
  stdin_support: false
  stdout_format: "json"
  composable_with:
    - "fundamentals-desk"
    - "technicals-desk"
    - "royal-rumble"
```

### Example chain

```
price-desk ───► JSON ───┐
fundamentals-desk ───► JSON ───┼───► chief's watchlist_view.py ───► markdown table
technicals-desk ───► JSON ───┘
```

None of those skills import each other's code. They all speak a stable CLI + JSON output contract. `chief-of-staff` calls `price-desk` via its CLI (`python3 price.py TICKER`) — that's allowed. Reaching into `price-desk/lib/...` would be a violation.

### The cross-skill audit

`cross-skill-audit.py` detects unsanctioned direct skill-to-skill code references. Found 2 in the fleet, both accepted as legitimate CLI composition (not code imports). Zero violations.

---

## 📐 How the three axes compose

Each axis answers a DIFFERENT question. They're orthogonal — a single skill obeys all three simultaneously without conflict:

```yaml
---
name: price-desk              # ← Unix: CLI identity
domain: fund                  # ← Tree: WHERE
capabilities:                 # ← Plugin: WHAT
  reads:  [...]
  writes: [...]
  cannot: [...]
unix_contract:                # ← Unix: HOW composes
  data_format: "jsonl"
  composable_with: [...]
---
```

One file. Three independent declarations. Every axis gets what it needs.

---

## 🧬 Why this specific combination

**Tree without Plugin** = organized chaos. Anything can do anything, just neatly filed.
**Plugin without Tree** = safe chaos. Nothing can break things, but you can't find anything.
**Tree + Plugin without Unix** = safe organized silos. Pieces can't combine.
**All three** = a system that scales, composes, and survives.

Unix has all three. So does macOS. So does Chrome. So does Kubernetes.

The overhaul gives your AI skill fleet the same DNA.

---

## 🛡️ Schema enforcement (the three axes in one contract)

The schema validator (`validate-skill.py`) enforces all three at install time:

```markdown
| 🟣 Level | 🟣 Enforces                         |
| -------- | ----------------------------------- |
| v0.1     | Tree axis (name, domain, description)|
| v0.2     | Plugin axis (capabilities block)     |
| v0.3     | Unix axis (unix_contract block)      |
```

Install an un-declared skill → rejected. That's the bright line.

---

## 📊 Scoring methodology

Each axis is scored 0-100% based on:

**Tree (current fleet: 99%):**
- All skills have declared domain: 100%
- All domains valid (enum check): 100%
- All installed as symlinks (no copies): 100%
- .home map routes without orphans: 100%
- One trivial imperfection = -1%

**Plugin (current fleet: 98%):**
- All skills pass schema v0.3: 100%
- Capabilities block complete: 100%
- NOT-for collision fences declared: 100%
- Install-time validator rejects bad skills: 100%
- No runtime sandbox (-2% honest deduction)

**Unix (current fleet: 98%):**
- unix_contract block complete: 100%
- Cross-skill audit clean: 100%
- Contract test harness passes: 100%
- Pipeable CLI universally supported: ~90% (some scripts don't accept stdin)

Combined: **99 × 98 × 98 ≈ 95% annual retention**.
Half-life: `log(0.5) / log(0.95) ≈ 13.5 years`.

---

## 🏛️ The diagram — one snapshot

```
┌─────────────────────────────────────────────────────────────┐
│                   🏛️ THE FLEET ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   🌳 Tree — where                                           │
│      .home → [fund | learning | general]                    │
│      every skill self-declares domain                       │
│                                                             │
│   🎮 Plugin — what                                          │
│      SKILL.md capabilities: reads/writes/calls/cannot       │
│      validator enforces at install                          │
│      audit catches drift                                    │
│                                                             │
│   🐧 Unix — how                                             │
│      SKILL.md unix_contract: format/stdin/stdout/compose    │
│      files + JSON + CLI composition                         │
│      no direct code imports                                 │
│                                                             │
│   🛡️ Preservation                                           │
│      stress-test (12 checks) + quarterly cron               │
│      git tags at milestones (rollback forever)              │
│      master arch doc + CHANGELOGs (onboarding cold)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Bottom line

The three-axis model isn't novel. Unix (1969) does it. macOS does it. Git does it. Kubernetes does it.

What's novel here is **applying it to an AI skill fleet** with:
- Machine-checkable declarations (schema v0.3)
- Install-time enforcement (validator gate)
- Periodic drift detection (stress-test + cron)
- Cold re-onboarding (master arch doc)
- Decades-durable plain-text everything

That's the architecture. 🏛️🃏
