# 📜 Master SKILL.md Example — fully annotated

**This is what a schema v0.3 compliant SKILL.md frontmatter looks like.** Every skill in the fleet follows this shape. The validator rejects anything that doesn't.

---

## The template

```yaml
---
name: example-skill               # Required. Kebab-case. Lowercase only. No spaces/underscores.
domain: general                   # Required. Must be: fund / learning / general.
version: 0.2.0                    # Semver. Bump on every material change.
role: "The Example"               # Human-readable job title (per principle_real_life_role_naming).

description: >                    # Must be 50-2000 chars. Must include NOT-for clauses.
  Brief statement of what the skill does + trigger phrases that fire it.
  Example trigger: "run the example", "do the example thing".
  NOT for: trivial one-off scripts (use bash directly).
  NOT for: functions inside another skill (use that skill's API).
  NOT for: general orchestration (use mewtwo).

capabilities:                     # Required in v0.2+. The plugin contract.
  reads:                          # What files/APIs the skill may READ.
    - "example/data/config.json"
    - "memory/principle_future_proof_by_default.md"
  writes:                         # What files the skill may WRITE (own data folder only).
    - "example/data/example-log.jsonl"
  calls:                          # Other skills this skill may invoke.
    - "price-desk (via .price)"
  cannot:                         # Explicit prohibitions. The SAFETY BOUNDARY.
    - "modify other skills' data"
    - "write outside own data folder"
    - "bypass anchor routing"

unix_contract:                    # Required in v0.3. The composition contract.
  data_format: "json"             # What shape this skill emits.
  schema_version: "0.2.0"         # Version of the data format.
  stdin_support: false            # Can be piped INTO via stdin?
  stdout_format: "json"           # What comes out of stdout (json / markdown / text).
  composable_with:                # Siblings this skill naturally pipes with.
    - "other-skill-1"
    - "other-skill-2"
---

# Example Skill

[Body of the SKILL.md — instructions, workflow, guardrails — below the frontmatter.]
```

---

## What the validator enforces

### Schema v0.1 (always)
- ✅ `name` exists + is kebab-case
- ✅ `domain` exists + is one of (fund | learning | general)
- ✅ `description` exists + is 50-2000 chars
- ✅ `description` contains `NOT for:` (collision-fence rule)

### Schema v0.2 (adds)
- ✅ `capabilities:` block exists
- ✅ All 4 sub-keys present: reads, writes, calls, cannot

### Schema v0.3 (adds)
- ✅ `unix_contract:` block exists
- ✅ All 5 sub-keys present: data_format, schema_version, stdin_support, stdout_format, composable_with

---

## Common mistakes the validator catches

```markdown
| 🟣 # | 🟣 Mistake                             | 🟣 Validator message                              |
| ---- | -------------------------------------- | ------------------------------------------------- |
| 1    | Forgot `domain:`                       | missing required field: domain                    |
| 2    | Wrong domain value                     | invalid domain `fin` — must be: fund, learning, general |
| 3    | Description too short                  | description too short (15 chars) — minimum 50      |
| 4    | No NOT-for clauses                     | missing `NOT for:` collision-fence clauses         |
| 5    | Missing capabilities (v0.2+)           | missing required `capabilities:` block             |
| 6    | Missing cannot sub-key                 | capabilities block missing `cannot:` sub-field     |
| 7    | Missing unix_contract (v0.3)           | missing required `unix_contract:` block            |
```

---

## Real-world example — price-desk

```yaml
---
name: price-desk
domain: fund
version: 0.2.0
role: Market Data Officer

description: >
  The live-price single source of truth for Blue Hill Capital.
  Wraps yfinance (Yahoo Finance) into a price-verification layer.
  No trade decision without a live price check.
  Commands: .price | .price TICKER | .price watchlist
  NOT for: fundamentals (use fundamentals-desk).
  NOT for: technicals (use technicals-desk).
  NOT for: final trade decisions (use .rumble or .tier).

capabilities:
  reads:
    - "yfinance API (network)"
  writes:
    - "price-desk/data/price-log.jsonl"
  calls: []
  cannot:
    - "write outside own data folder"
    - "modify other skills"
    - "return stale cached data without timestamp"

unix_contract:
  data_format: "jsonl"
  schema_version: "0.1.2"
  stdin_support: false
  stdout_format: "json"
  composable_with:
    - "fundamentals-desk"
    - "technicals-desk"
    - "royal-rumble"
    - "tier"
    - "accuracy-tracker"
---
```

**This passes schema v0.3.** 20/20 skills in the fleet match this shape.

🏛️🃏
