# 📢 Promotion Kit — Copy-paste ready posts

**Goal:** drive eyes to the-overhaul. Three channels, three tones, one message:
*"This is architect-tier thinking applied to an AI fleet. Here's the case study."*

---

## 🥇 Hacker News (Show HN) — the most valuable post

### Where to submit
👉 https://news.ycombinator.com/submit

### Title (under 80 chars)
```
Show HN: The Overhaul – one-evening AI fleet architecture (20x durability gain)
```

### URL field
```
https://github.com/DimmMak/the-overhaul
```

### Text (optional first comment — post this AFTER submission as a reply to your own post)
```
I built 20 Claude Code skills over a few weeks for a personal hedge fund 
stack (Blue Hill Capital). The fleet was quietly drifting — installed 
as copies instead of symlinks, no schema enforcement, hardcoded routing 
tables, ad-hoc composition.

Spent one evening applying three orthogonal architecture axes (tree + 
plugin + unix — same DNA as Unix/macOS/git/k8s) and locking the gains 
with stress-tests + a quarterly audit cron.

Half-life math: ~8 months → ~13.8 years (20x). Schema-validated at 
install, cross-skill-audited, all fleet rules declared in memory/ as 
plain markdown so they outlast the tools.

Full case study with the exact autopsies, scripts, and replicate.md 
blueprint for porting to any domain (legal, medical, VC, research, etc).

Would love feedback on whether runtime capability enforcement (I 
deliberately skipped it as over-engineering) is worth the complexity 
at larger scale. Currently 20 skills feels fine with declarative + 
install-time validation + quarterly audit.
```

### Timing
- 🟢 **Best:** Mon–Thu, 8–10 AM ET (peak traffic)
- 🟡 OK: Weekend afternoons
- 🔴 Worst: Friday late afternoon

### What to expect
- 10-50 upvotes if it lands → top of Show HN for a few hours
- 2-5 thoughtful comments → real engagement
- 1-2 DMs from engineers / recruiters within 48 hrs

---

## 🥈 Twitter / X — thread format

### Thread (copy each tweet as a separate post — 10 tweets total)

**Tweet 1 (hook)**
```
I built 20 AI skills over weeks. The fleet was drifting silently.

One evening of architectural overhaul → half-life went from ~8 months 
to ~13.8 years. 20× durability gain.

How I did it (with math) 🧵
```

**Tweet 2 (the problem)**
```
The fleet had 3 failure modes:

🔴 Hardcoded routing list that went stale on every new skill
🔴 No isolation contracts — any skill could write anywhere
🔴 Ad-hoc composition — skills imported each other's code

Every week it got harder to add a new skill without breaking something.
```

**Tweet 3 (the model)**
```
Three orthogonal axes. Same DNA as Unix, macOS, Git, Kubernetes:

🌳 Tree — WHERE things live (org hierarchy)
🎮 Plugin — WHAT they can do (capability contracts)
🐧 Unix — HOW they compose (pipes + stable CLI)

System survival = tree × plugin × unix. Multiplicative.
```

**Tweet 4 (session 1 — tree)**
```
Session 1 (~1 hr): Tree axis

Every skill declares its domain in SKILL.md frontmatter. Routing layer 
reads `domain:` from filesystem → auto-routes. Kill the hardcoded list.

Tree: 90% → 99%
Half-life: 8mo → 1.1yr
```

**Tweet 5 (session 2 — plugin)**
```
Session 2 (~3 hrs, the big one): Plugin axis

Every skill declares `capabilities: reads/writes/calls/cannot`.
Schema validator rejects non-compliant skills at install time.

SNES cartridge model: plug in, can't break the console.

Plugin: 50% → 98%
Half-life: 1.1yr → 10yr
```

**Tweet 6 (session 3 — unix)**
```
Session 3 (~1 hr): Unix axis

Every skill declares `unix_contract:` — data format, stdin support, 
stdout format, composable_with. Files + JSON + stable CLIs only. 
No direct code imports.

Unix: 80% → 98%
Half-life: 10yr → 13.8yr
```

**Tweet 7 (session 4 — preservation)**
```
Session 4 (~1 hr): Lock the gains

✅ 12-check stress test across all 3 axes
✅ Quarterly audit cron (runs automatically forever)
✅ Git tag at world-class checkpoint for instant rollback
✅ Master architecture doc for cold re-entry 5 years later
```

**Tweet 8 (the math)**
```
Before: 0.90 × 0.50 × 0.80 = 0.36 annual retention → 8 months half-life
After:  0.99 × 0.98 × 0.98 = 0.95 annual retention → 13.5 years

The weakest axis (plugin at 50%) was dominating. Fixing it unlocked 
the compounding.

Attack your bottleneck first.
```

**Tweet 9 (the transferable part)**
```
The fund stack is the shell. The architecture is the substance.

The same three-axis model ports to:
- Legal case tracking
- Medical records  
- VC deal flow
- Research libraries
- Any multi-component decision system

Blueprint in the repo 👇
```

**Tweet 10 (CTA)**
```
Full writeup + scripts + replicate blueprint:

https://github.com/DimmMak/the-overhaul

Writing more at https://dimmmak.github.io

Open to AI fleet architecture consulting. DMs open.
```

### Posting tips
- Post the whole thread in one session (not spread across hours)
- Pin tweet 1 to your profile
- Reply to tweet 10 with: "If you want to port this to your domain, open an issue on the repo or DM me"

---

## 🥉 LinkedIn — professional tone

### Post
```
Spent last night applying durable architecture patterns to my personal 
AI skill fleet.

Result: system half-life went from ~8 months to ~13.8 years using a 
three-axis model (tree + plugin + unix) — the same DNA that makes 
Unix, macOS, Git, and Kubernetes last for decades.

Write-up with the autopsies, scripts, and a blueprint for applying 
it to any domain (legal, medical, VC deal flow, research):

👉 https://github.com/DimmMak/the-overhaul

I'm now exploring AI architecture consulting engagements — happy to 
chat with anyone building internal AI tooling they want to survive 
beyond a single model generation.

#AIEngineering #SystemsArchitecture #VibeCoding #ClaudeCode
```

### Targeting
- 🎯 Engineers at AI-fintech startups
- 🎯 CTOs at hedge funds 
- 🎯 AI product leads at corporates
- 🎯 Fellow AI-native builders

### What to do after posting
1. Update LinkedIn headline: "AI Systems Architect | Durable AI Tool Design"
2. Pin the post to your profile
3. Reply to EVERY comment within 12 hours
4. DM 5 connections who are in your target audience → "hey, thought you'd find this interesting: [link]"

---

## 🎯 The posting order (do in sequence, not parallel)

```markdown
| 🟣 # | 🟣 Where   | 🟣 When                    | 🟣 Why order matters       |
| ---- | ---------- | -------------------------- | -------------------------- |
| 1    | Twitter    | First — right now          | Builds early momentum       |
| 2    | LinkedIn   | +30 min after Twitter      | Pro audience sees activity |
| 3    | Hacker News| Tuesday 8 AM ET            | Peak HN traffic window     |
```

**Why this order:**
Twitter gets you organic likes / reshares first. LinkedIn sees you "active" and amplifies. HN traffic spikes AFTER you already have social proof elsewhere — your HN comments look more credible.

---

## 🎬 After you post — the 48-hour loop

```markdown
| 🟣 Hour | 🟣 Action                              |
| ------- | -------------------------------------- |
| 0       | Post (Twitter first)                   |
| +1h     | Reply to any comments                  |
| +4h     | Check stats, reply again               |
| +24h    | Post to LinkedIn                        |
| +48h    | Submit to HN (Tuesday morning)          |
| +72h    | Post reflection — *"here's what I learned from the feedback"* |
```

Consistency beats bursts. Don't go viral once; show up steadily.

---

## 🚨 What NOT to do

```markdown
| 🟣 Mistake                                           | 🟣 Why it hurts                   |
| ---------------------------------------------------- | --------------------------------- |
| Post identical copy on all three                     | Platforms punish cross-posts       |
| Beg for upvotes                                       | Kills credibility                 |
| Reply defensively to critical comments               | Erodes trust instantly            |
| Abandon the thread after 24 hours                    | Misses the conversation compound   |
| Apologize for the length                              | Undermines the work               |
| Say "I'm just learning" / imposter-syndrome framing  | Loses the consulting positioning  |
```

---

## 🧬 The one-liner

> **One post per channel. One narrative. One link. Iterate your follow-up based on real feedback. The content is already ready — the only thing left is hitting publish.**

🎯🃏📢
