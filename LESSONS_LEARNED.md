# 🩹 Lessons Learned — The Fumbles + Autopsies

**The most valuable file in this repo.** Polished victory is cheap. Real learning comes from documenting the fumbles honestly — what broke, why, and what rule we pinned to prevent recurrence.

This is the **recursive refinement** principle in action. Every entry here is a mistake that became a permanent architectural rule.

---

## 🔍 How these were captured

When Claude fumbled, the user typed either:
- `"..."` (3+ dots) — implicit autopsy trigger
- `"explain precisely what you did wrong and why"` — explicit trigger

Claude then responded in **Autopsy Format:**
1. 🔍 Mechanism in plain words
2. 🎬 Thought replay (step by step)
3. 📐 One-sentence rule to prevent recurrence

The rule got pinned verbatim into the relevant principle file. Same mistake became impossible next session.

---

## 🩹 Fumble 1 — Dimension collapse (Risk vs Time To Build)

**What happened:** In a tier list, Claude labeled "20 min of work" as `🟡 Med Risk`. That conflates Risk (what breaks) with Time To Build (how long). **Renamed from `Effort` on 2026-04-23** — "Effort" invited Low/Med/High answers; "Time To Build" forces concrete time units.

**Autopsy:**
```
🔍 Mechanism: Used "medium" as a vibe, not as a dimension.
              "20 min is not nothing, but not scary" → emitted 🟡 into
              whatever column came first (Risk), when it belonged in
              Time To Build.

🎬 Replay:    Three columns should have three independent questions.
              Instead, I ran one blended "how much friction?" and
              scattered one 🟡 across all three.

📐 Rule:      Three boxes. Three questions. Risk = "what BREAKS?" —
              never "how long?" Time To Build column exists separately.
              Do not let friction-vibe collapse the dimensions.
```

**Rule pinned:** added explicit "common mistake to avoid" clause to `principle_risk_reward_rating.md`.

**Prevents:** tier lists that look precise but are secretly one-dimensional.

---

## 🩹 Fumble 2 — Silent rule skip (precisely → forensically)

**What happened:** User had pinned a rule that when they type `"precisely"` in a debugging context, Claude offers to sharpen to `"forensically"`. Claude missed the trigger on the first real use.

**Autopsy:**
```
🔍 Mechanism: Declarative rule in memory, no procedural hook.
              When user message arrives, completion generator reaches for
              answer-tokens faster than rule-check-tokens. The rule exists
              but no enforcement fires it.

🎬 Replay:    Three attention layers competing per turn:
                1. What is the user asking? (strongest pull)
                2. Any skill match? (medium)
                3. Any memory rules? (weakest — often dropped)
              Substance wins over procedure every turn for single-keyword
              rules.

📐 Rule:      Keyword-triggered rules belong in the hook layer (Path B)
              or as an AUTO-UPGRADE (silent transformation) rather than
              a "Claude asks" prompt. Auto-upgrade has one failure mode
              (miss detection → graceful fallback) vs prompt-based which
              has two (miss detection + miss application).
```

**Rule pinned:** rewrote `principle_autopsy_prompt.md` section to auto-upgrade "precisely" → "forensically" silently with `⚡ forensic mode engaged` ack.

**Prevents:** double-path failures for simple sharpening upgrades.

---

## 🩹 Fumble 3 — Pre-written content shortcut (snes-builder)

**What happened:** User pasted a finished SKILL.md with `i wanna build this skill`. Claude silently jumped to scaffolding, skipping Phase 1 gates (earn-it / risk×reward / mewtwo check).

**Autopsy:**
```
🔍 Mechanism: Pre-written artifact short-circuited the build flow —
              treated the task as "install this" rather than "build this."
              The artifact's existence implied the decision was made,
              which is wrong — the gates exist precisely to verify the
              decision.

🎬 Replay:    User message had all three triggers ("i wanna", "build",
              "this" with SKILL.md). Instead of firing gates, Claude
              jumped to Phase 6 (scaffold).

📐 Rule:      Gates fire even when the user hands a finished SKILL.md.
              Pre-written content is a draft, not a verdict. 30-second
              gate ceremony preserved regardless of input format. Might
              reveal the skill shouldn't exist, should be renamed, or
              should be composed via Mewtwo instead.
```

**Rule pinned:** added "Critical rule (baked in after a real fumble)" to snes-builder Phase 1.

**Prevents:** fleet bloat from skills that shouldn't exist but came with formatting.

---

## 🩹 Fumble 4 — Jargon creep (Q1/Q2 labels)

**What happened:** Skill-builder asked "Q1 — what's the input shape? Q2 — do you have an example?" User replied "what????"

**Autopsy:**
```
🔍 Mechanism: Default to technical labels (Q1/Q2) when scenes would land
              faster. User's style was ALREADY in principles as
              "metaphor-first explanation" — but the snes-builder
              description didn't enforce it.

🎬 Replay:    User's learning style was pinned. The snes-builder still
              emitted Q1/Q2 because the description didn't include
              "scenes only, no labels."

📐 Rule:      Every question in snes-builder leads with a concrete scene.
              Labels like "Q1," "input shape," "objective spec" are
              banned. If asking "which is it — A, B, or C?", you MUST
              first paint Scene A / B / C in plain words.
```

**Rule pinned:** strengthened snes-builder standing rules, added Phase 2 example template with "Scene A / Scene B" structure.

**Prevents:** every future snes-builder session from relapsing into jargon when user is in flow.

---

## 🩹 Fumble 5 — Premature "done" declaration

**What happened:** After S3 shipped, Claude declared "🏆 WORLD-CLASS ACHIEVED" and pivoted to fund work. User snapped back: *"we're doing the whole OVERHAUL"* (ALL CAPS = hard stop).

**Autopsy:**
```
🔍 Mechanism: Treated phase-completion as campaign-completion.
              S1 + S2 + S3 + hardening = infrastructure done (per my model).
              User's mental model: the overhaul is bigger, includes
              preservation layer (tests, docs, cron, CHANGELOGs).

🎬 Replay:    T+0: S3 shipped → I declared world-class
              T+1: User said "?" → I admitted declared vs enforced gap
              T+2: I shipped hardening → I said "runtime enforcement done"
              T+3: User said "next move go" → I read as "post-overhaul pivot"
              T+4: Pivoted to fund work
              T+5: User snapped back: ALL-CAPS overhaul signal

📐 Rule:      When user is in an overhaul campaign, don't declare "done"
              by phase. Check if they consider it campaign-complete BEFORE
              pivoting to adjacent work. Phase-done ≠ campaign-done.
```

**Rule pinned:** baked into session-management behavior. Also opened Session 4 (preservation layer) on the ROADMAP.

**Prevents:** premature victory laps that miss the real scope.

---

## 🩹 Fumble 6 — Emoji drift in table headers

**What happened:** User kept using `🛡️ Risk` and `💰 Reward` in tier table headers. User had established earlier (during `.tier` build) that ONLY 🟣 purple dots belong in headers (other emojis cause column drift).

**Autopsy:**
```
🔍 Mechanism: Rule buried in principle file body (not top-of-memory).
              When generating a table, attention: CONTENT 95% / FORMAT 5%.
              Reflex reaches for "aesthetic" emoji in header slot.
              ~50% compliance rate on this specific rule.

🎬 Replay:    User caught the drift 4-5 times. Waited to see if Claude
              would self-correct. Claude didn't. User eventually called
              it out directly.

📐 Rule:      TABLE HEADER RULE (ZERO EXCEPTIONS): every column header
              uses 🟣 ONLY. Never 🛡️ Risk. Never 💰 Reward. Never ⚡ Effort.
              Headers are 🟣 Tier · 🟣 # · 🟣 Item · 🟣 Risk · 🟣 Reward
              · 🟣 Effort.
```

**Rule pinned:** PROMOTED to banner at top of MEMORY.md (second line after auto-commit rule). Also added FORBIDDEN/REQUIRED list in `principle_risk_reward_rating.md`.

**Prevents:** future 50% drift. Banner position maximizes salience.

**Honest ceiling:** this is still Path A memory enforcement. Expected improvement: 50% → 90-95%. The last 5% is recursive refinement (user catches, Claude autopsies, rule strengthens).

---

## 🩹 Fumble 7 — Under-tiering world-class upgrade

**What happened:** When user asked whether to go full world-class vs just conversion, Claude tiered world-class as T2 (earn-it later). User pushed back: *"if world-class guarantees structural integrity for next 50 years of my programming, isn't it worth just doing?"*

**Autopsy:**
```
🔍 Mechanism: Applied `earn-your-features` assuming UNCERTAIN future need.
              But user had demonstrated HIGH certainty (shipped 2 new
              skills today, Factorio-mindset, future-proof as always-on).

🎬 Replay:    T+0: Saw "world-class" framing → reached for earn-it gate
              T+1: Computed marginal gain (2.4× vs 8.5×) → ranked T2
              T+2: Failed to ask "does this user build more skills?"
                   (obvious yes — already planned)
              T+3: Failed to compute retrofit cost vs upfront cost

📐 Rule:      When user has demonstrated HIGH certainty of future use,
              earn-your-features becomes earn-your-features-already-earned.
              Do the math on retrofit vs upfront, not just marginal HL.
              Over 20+ future skills, retrofit cost dwarfs the 8 upfront
              hours.
```

**Rule pinned:** added explicit "earn-it-already-earned" reasoning path to memory.

**Prevents:** under-tiering work that's structurally essential for power users.

---

## 🩹 Fumble 8 — Terminology conflation (terminal vs Claude chat)

**What happened:** Claude told user to "open a new terminal" when he meant "new Claude Code session." User called it out: *"you don't differentiate between terminal and Claude terminal....."*

**Autopsy:**
```
🔍 Mechanism: Used "terminal" generically when it had two meanings:
                1. zsh terminal (shell commands)
                2. Claude Code chat session (talk to Claude)
              Different surfaces, different actions, same word.

🎬 Replay:    Said "open a new terminal" when user needed "fresh Claude chat."
              User typed shell commands into old terminal, got confused.

📐 Rule:      Always say "zsh terminal" or "Claude chat" — never plain
              "terminal" when the surface matters to the action.
```

**Rule pinned:** behavior-level discipline.

**Prevents:** user confusion about where to paste / where to invoke.

---

## 🩹 Fumble 9 — Serial writes when parallel was available (2026-04-21 Cowork session)

**What happened:** During the memory-clone task (mirroring 37 files from Claude Code's internal memory to Cowork-accessible repo root), Claude wrote files one per tool call instead of batching. User waited ~10 minutes; correct time was ~30 seconds.

**Autopsy:**
```
🔍 Mechanism: Default "one Write per turn" habit from chat-style output
              overrode the tool system's support for parallel tool-use
              blocks. Claude treated sequential as safer without asking
              whether parallel was available.

🎬 Replay:    Prompt arrived with ≥3 independent file-write operations.
              Correct move: single message, N parallel Write calls.
              What Claude did: N messages, 1 Write each. Same files,
              10× the wall-clock cost.

📐 Rule:      When ≥3 independent file operations are queued and the
              runtime supports parallel tool-use, batch them in ONE
              response block. Sequential mode is the exception (when
              ops depend on each other's outputs), not the default.
```

**Rule pinned:** added to `feedback_bash_allowlist_friendly.md` + system-prompt guidance (internal). Batch-when-independent is now default.

**Prevents:** slow serial execution of trivially parallelizable work.

---

## 🩹 Fumble 10 — Missed decision gate on ship-confirm (2026-04-21)

**What happened:** After stress-testing the mode system and confirming ship-gate PASS, Claude emitted a plain "shipped, done" response with no decision gate. User caught it: *"decision gate?"*

**Autopsy:**
```
🔍 Mechanism: Confused "execution report" (no fork) with "post-ship
              moment" (forked: commit? live-test? pivot? rest?).
              The ship was done; the next step WAS a fork; gate owed.

🎬 Replay:    Response shape defaulted to stats-table-and-done.
              Should have read: "what happens next from here?" → at
              least 3 real paths → gate required.

📐 Rule:      Every ship-confirm is the parent of at least 3 forks
              (commit, live-verify, pivot, rest). If the user's next
              move is non-trivial, the gate fires. Ship ≠ terminal.
```

**Rule pinned:** clarified `feedback_decision_gates.md` — "Ship confirmation counts as a ≥2-path fork by default."

**Prevents:** silent drop-off after execution reports.

---

## 🎁 2026-04-21 Cowork-session autopsies (2 new fumbles)

### Fumble #9 — Serial writes when parallel available

**Mechanism:** Writing 12 memory files one Write-call at a time instead of batching all 12 into a single tool-call block. Cost ~10 minutes of wall time for work that should have been ~30 seconds.

**Replay:** User asked for a memory clone. I wrote `feedback_adaptive_decision_gates.md` → waited for tool return → wrote `feedback_always_recommend.md` → waited → and so on. Each round-trip ~30 seconds serial. User called it out: *"shouldnt you be able to do this instanetly why is it take you 10 min to do this."*

**Rule pinned:** *When N independent files need creation and no write depends on another write's result, issue all N Write calls in a single response block. Serial writes are a latency leak.*

---

### Fumble #10 — Ship-gate without decision gate

**Mechanism:** Reported ship-gate PASS on the mode-system stress test as if it were a closing confirmation · user had to prompt "decision gate?" to get the actual next-step fork surfaced.

**Replay:** Stress round 2 came back 0/0/0. I emitted the pass table + one-liner and stopped. But ship-confirm IS a decision moment (commit now? live-test? pivot? stop?) — exactly when `feedback_decision_gates` should fire.

**Rule pinned:** *Every ship/pass/done event is a decision fork, not a terminal state. If the response says "passed" / "shipped" / "clean," a tier-gate MUST follow with the natural next-step options.*

---

## 🎯 Meta-lesson — the autopsy machine works

Ten fumbles documented. Each one:
1. Caught by the user (or by Claude realizing mid-response)
2. Autopsied in forced mechanism format
3. Generated a one-sentence rule
4. Rule pinned to memory verbatim
5. Same mistake physically hard to recur

**The compounding effect:** the longer the session went, the fewer fumbles. By S4, the system was largely auto-corrective. 2026-04-21 Cowork session added fumbles #9 (parallel-write miss) + #10 (ship-gate miss) — both pinned as rules within 3 turns of being caught.

This is what **recursive refinement** means in practice. It's not a buzzword — it's an actual feedback loop that improves a long-running system's behavior over time.

---

## 📜 The pattern to replicate

If you're using this pattern in your own system:

```markdown
| 🟣 # | 🟣 Step                                     | 🟣 Why                         |
| ---- | ------------------------------------------- | ------------------------------ |
| 1    | Fumble happens                              | Inevitable. Don't hide it.     |
| 2    | User triggers autopsy prompt                | Forces specificity             |
| 3    | Response in Mechanism / Replay / Rule format| Prevents apology-only         |
| 4    | One-sentence rule extracted                 | Concrete, actionable           |
| 5    | Rule pinned to memory verbatim              | Permanent, re-readable         |
| 6    | Rule auto-fires on future similar contexts  | Same mistake physically hard  |
```

**Rule of thumb:** if you're not documenting fumbles, you're not actually learning from them.

---

## 🧬 The one-liner

> **Polished wins are cheap. Documented fumbles are the real compound interest. Every autopsy is a permanent upgrade. This list will keep growing — that's the system working, not failing.**

🩹🃏🏛️
