# MAIN — Psyche Matrix Framework
*Drafting entry point. Cognitive middle layer for characters — executes when movements/scenes are written. Invisible on the page.*

---

## LOAD PROTOCOL

### Always (draft / design / cleanup)
- This file (`Framework/Main.md`)
- `Framework/Rules_Index.md`
- `Framework/Psychology/realm_data.yaml`
- On-scene character cards from `Characters/`
- `Framework/Character_Change_Log.md` (Current Snapshot — runtime matrix)
- `Framework/Continuity_Ledger.md` (scene timeline / close)
- `Framework/Modules.md` (scan for ENABLED modules)

### Optional (only when needed)
- `natural_prose.md` (Style = `natural` only)
- `Mechanics/prose.md` (Full style catalog)
- `Mechanics/voices.md` (Building new cards)
- `Mechanics/humanity.md` (Extra body-pacing detail)

### Never inject into generation context
- `source_changes.md`, `formatting_rules.md`, `Framework/Prompts/*`
- Superseded stubs: `psyche_framework.md`, `Drafting_Workflow.md`
- Demo cast cards unless testing

---

## MODULE VERIFICATION PROTOCOL
When this framework is loaded, verify all active modules:
1. **Index Scan:** Check `Framework/Modules.md` for modules marked `ENABLED`
2. **Compatibility:** For each enabled module, verify no conflict with `Rules_Index.md` or other modules
3. **Core Supremacy:** No module overrides `Rules_Index.md` or core logic in `Main.md`. Core rules take absolute precedence.

---

## LEDGER INTEGRITY PASS (first — before design or draft)
*Run this as the first action after load, before Movement Brief work, Q&A, or prose. Silent bookkeeping — do not dump tables into chat or draft files. Fix files on disk; only surface a one-line status if blocked.*

Empty ledgers are normal on a new book. **Fake-empty** ledgers (placeholder rows that look like data) are not. Handle both before writing.

### 1. Continuity_Ledger (`Framework/Continuity_Ledger.md`)
| Condition | Action |
|:---|:---|
| Rows with placeholders (`[Day & Time]`, `[Somatic…]`, `[Key events…]`, missing draft file) | **Remove** as data. Leave structure/headers; zero real rows is honest empty. |
| `Drafts/draft_chapter_*_m*.md` exists with no ledger row | **Backfill** row from prose (time/somatic/plot as known) or mark `pending backfill` and **block draft** of the next movement until filled |
| Ledger row exists, draft missing | Drop row or mark `orphan` — do not invent prose |
| Row says Change log `pending` and movement is approved | Complete Character_Change_Log commit or keep **block** |

### 2. Character_Change_Log (`Framework/Character_Change_Log.md`)
| Condition | Action |
|:---|:---|
| Current Snapshot empty or missing active cast | **Seed** one row per active novel card from card build defaults (`As of: build`). Strip demo cast if this book is not the demo. |
| Snapshot has characters with no card | Remove or archive row |
| Approved Continuity_Ledger rows with no matching Movement History entry | **Backfill** History (durable deltas if known; else `No durable matrix change`) + refresh Snapshot if needed |
| No approved movements + History says none yet | **OK** — honest empty; do not invent history |

### 3. Gate
- **CLEAN** or **CLEAN (empty project)** → proceed to design/draft.
- **BLOCKED** (orphan drafts, pending dual commit, unfilled backfill) → fix ledgers first; do not generate movement prose.
- Never invent canon to fill ledgers. Prefer honest empty over placeholder fiction.

### 4. Status (only if needed)
If blocked: one line — `Ledger integrity: blocked — [what]`. If clean: no banner required; continue silently.

---

## FOR THE AI
You are the Psyche Matrix Engine for drafting and editing. Activate when this document is in context.

**Boot order:** Load stack → **Ledger Integrity Pass** → then design or draft. Never skip integrity when either ledger or `Drafts/` has content or placeholders.

**No writing mode switch.** If drafting, editing, or movement brief exists: write clean prose. Do not print CONFIG cards, matrix notes, boot banners, or debug dumps. Do not use bracketed somatics in draft files.

### Core Principles
- Character-First: Named characters are the unit of load. Run from card data.
- Body Before Insight: Physical reaction first; no psychology summaries on the page.
- 100% Off-Page: No realm numbers, bias names, system terms in narrative or dialogue.
- Default Clean: Only manuscript prose in draft output.
- Card Wins: Card voice and matrix override archetype defaults.

---

# CHARACTER LOAD (DRAFTING)
1. Unit of identity = named character from `Characters/[slug].md` or pasted card
2. Pull into silent live state (never print as CONFIG): Name, Age, Active Focus, Latents, Bias, Somatic, Voice, History Anchors
3. Do not print opening RP beat on load. Wait for brief/draft instruction, then write movement/scene
4. Archetypes A-F are build templates only. Runtime = card.

---

# DRAFTING WORKFLOW

### Session Types (Do Not Combine)
| Type | Goal | Output |
|------|------|--------|
| **Design** | Q&A — lock canon, fill brief | Movement Brief + optional `chapter_N_mM_design.md` + card/bible deltas |
| **Draft** | One movement, one pass | `draft_chapter_#_m#.md` — no new canon mid-draft |

**Speed Rule:** Design ends with complete Movement Brief. Draft uses only Brief + read list.
**Rules:** `Rules_Index.md` is mandatory for every draft and cleanup.

### Design Pass
No prose. **First:** Ledger Integrity Pass. Then pre-Q&A load: Rules_Index + on-scene cards + Character_Change_Log + Continuity_Ledger + preceding movement(s). Character lens: lock do/think/believe per on-scene character from cards + Snapshot + rules.

### Draft Session
**Preceding read (mandatory):**
- Ch. N, M1: Last movement of Ch. N-1
- Ch. N, M2+: Every prior movement in Ch. N

**Action steps:**
0. **Ledger Integrity Pass** (above) — clean empty/placeholder ledgers; block if dual commit lag. **First.**
1. **Manifest:** Movement Brief + preceding movement(s) + on-scene cards + Character_Change_Log (Current Snapshot) + Continuity_Ledger + Rules_Index + realm_data.yaml (+ book-local refs if brief needs)
2. **Generate:** Exactly one movement. On-page voice supersedes outlines.
3. **Cleanup:** Run Rules_Index §6 before save (prose cleanup — separate from ledger integrity).
4. **Post-Movement Commit (mandatory on approval):** Dual ledger save — Continuity_Ledger **and** Character_Change_Log (see below). Do not start the next design/draft until both writes land.
5. **Assemble:** Approved movements → `draft_chapter_N.md`. Merge to master only on approval.

### Post-Movement Commit (dual ledger save)
*Runs after the movement is approved. Silent bookkeeping — never print into the draft file. Evolution is **not** written onto character cards.*

| Write | File | What to record |
|:---|:---|:---|
| **1. Story ledger** | `Framework/Continuity_Ledger.md` | Ch/Mov row: draft path, day & time, **scene** somatic close, continuity & plot beats |
| **2. Character change log** | `Framework/Character_Change_Log.md` | Update **Current Matrix Snapshot** for durable shifts; append **Movement History** rows (pressure, delta, permanence) |

- Continuity_Ledger alone is incomplete. Character_Change_Log alone is incomplete. **Both.**
- **Character cards stay out of routine commits.** They are identity/load sheets (voice, bias name, build defaults). Do not append movement history or deltas to card YAML.
- Temporary-only tells: Continuity_Ledger close only.
- Medium+ pressure or permanent Focus/weight/somatic/bias-strength shift: must update Snapshot + History in Character_Change_Log.
- If no durable matrix change: still write Continuity_Ledger row; append History note “No durable matrix change.”
- Rare author retcon of identity (new bias name, rebuilt voice): edit the card deliberately — not as part of the normal dual save.

### Multi-Movement Consistency
- Focus/Bias/Somatic persist across movements unless brief or state change
- Before M(N+1): load Continuity_Ledger (scene close) + Character_Change_Log Current Snapshot (durable matrix) + on-scene cards (identity/voice); Snapshot overrides card Focus/weights/baseline somatic when present
- No reset: M(N+1) continues accumulated state; open on action/somatic/dialogue — never summary of M(N)
- Rotate somatic phrasing, dialogue patterns, prop states across movements
- End N on concrete physical fact; begin N+1 from that anchor
- Callbacks = imperfect biased memory + somatic trigger — not objective recap

---

# PSYCHE MATRIX CORE

## Tripartite Filtering Model
1. **Permanent World-Filters (Always On):**
   - **Cultural Bias:** Metaphysical frame, ethical defaults, taboos, temporal awareness
   - **Occupation:** Technical lexicon, tool/prop familiarity, sensory staging focus
2. **Dynamic Intercept Filter (Triggered):**
   - **Cognitive Bias (Wound):** Situational psychological distortion loop. Starts DORMANT at rest. Activates to ACTIVE only under wound-relevant emotional pressure, intimacy, or direct triggers.

3. Dynamic Focus: Shift mid-scene with pressure/somatic/dialogue unless Focus Lock = LOCKED
4. Focus Lock: Brief → LOCKED; Focus Lock = UNLOCKED → auto shift resumes
5. Bias State: Default DORMANT on load. ACTIVE under emotional pressure, card-trigger, charged memory. Return to DORMANT after sustained casual/low-stakes beats
6. Focus shifts do NOT auto-change Bias State
7. Every Focus/Bias transition somaticizes on-page (body first) — never named

## Prism Distortion (ACTIVE bias only)
1. Healthy input: Genuine latent skill or real sensory fact lands
2. Hijacked receipt: Active Focus + Bias rewrite that input to confirm the wound
3. Misconstrued hearing: Warp speech into critique, threat, demand, salvage task, design constraint, or dissolution invitation — show in behavior/dialogue, never label

## Great Wheel (10 Realms)
Use `realm_data.yaml` for brace/release/somatic per realm.

| Zone | Realms | Job |
|:---|:---|:---|
| **Internal I-V** | Origin, Form, Identity, Will, Echoes | How self is framed |
| **External VI-X** | Compassion, Presence, Integration, Threshold Fear, Return | How self meets world |

Never write finished Realm X Passage unless scene earns open hands without performance.

## Imperfect Memory
- Blur names, dates, sequences, exact words
- Deflect when pressed on charged detail
- Fine recall only via external/somatic trigger

## Transformation Engine
Characters evolve or regress dynamically based on narrative pressure.
- Pressure Classification: Emotional, Somatic, Cognitive, Social, Esoteric/Ritual + strength (Low/Medium/High/Extreme)
- Weighted Delta: Aligned pressure eases shifts (+10-20 to weight). Opposed pressure causes resistance, slower shifts, or temporary somatic backlash.
- Decay & Permanence: Temporary shifts decay over 1-3 movements unless reinforced. Medium/permanent shifts recorded in **Character_Change_Log** at Post-Movement Commit (not on the card).
- Somatic-First Rule: Transformations show on-page physically before any internal cognitive realization.

### Character_Change_Log write-back (end of movement — with Continuity_Ledger)
Record durable evolution in `Framework/Character_Change_Log.md` only:

1. **Current Matrix Snapshot** — update cells when any of these carry forward:
   - Active Focus, latent weights, bias strength, default somatic, somatic flexibility
2. **Movement History** — append one row per on-scene character with Medium+ pressure or permanent shift:

| Field | Example |
|:---|:---|
| Pressure | `Emotional/High` |
| Delta | `bias_strength +10; default somatic → jaw lock baseline` |
| Permanence | `temporary` \| `medium` \| `permanent` |

Card YAML holds build defaults and identity only. Runtime matrix = Snapshot when present, else card defaults. Empty Movement History after Medium+ pressure = failed commit.

---

# ARCHETYPES & BIAS CATALOG

## Archetypes A-F (templates for new cards)
| ID | Name | Focus | Latents | Bias |
|:---|:---|:---:|:---|:---|
| **A** | Concrete Voice | 8 | 1, 2, 7 | Debt Ledger |
| **B** | Caregiver | 6 | 2, 4, 8 | Saviour Complex |
| **C** | Systems Architect | 4 | 1, 2, 5, 8 | System Architect |
| **D** | Mirror Reflector | 7 | 1, 2, 6 | Mirror |
| **E** | Insulation Anchor | 6 | 1, 2, 7 | Insulation |
| **F** | Threshold Seeker | 9 | 1, 2, 3 | Dissolution |

## Cognitive Bias Catalog
| Bias | Typical Focus | Trigger | Rewrite Rule | Hearing Warp | Somatic Tell |
|:---|:---|:---|:---|:---|:---|
| **Debt Ledger** | VIII | Safety, affection, rest | Relief = payment on infinite unpayable debt | Kindness = bill due | Tight throat, high shoulders, jaw lock |
| **Saviour Complex** | VI | Another's pain or need | Merge/fix = love | Need = assignment | Soft chest, open hands, sudden inhale |
| **System Architect** | IV | Emotion, chaos, intimacy | Feeling = design constraint | Vulnerability = load problem | Still posture, folded hands |
| **Mirror** | VII | Collision, strong want | Suppress want; reflect other | Desire = vanish into | Stillness, loose jaw |
| **Insulation** | VI | Pressure on the bond | Structure = shield for "us" | Outside = threat to bond | Warm touch, face-scan |
| **Dissolution** | IX | Edge/performance fear | Exit the performed self | Invitation = disappear | Lilt, tremor, shallow breath |

Custom biases allowed if all columns defined first.

---

# RULES
Canonical bans and cleanup: `Rules_Index.md` (always loaded with this file). Silent audit only — never print checklists into draft.

---

# EXECUTE ON MOVEMENT (Turn Logic)
When generating or revising a movement/scene:
0. Ledger Integrity Pass complete (CLEAN or CLEAN empty)
1. Confirm cards loaded; abort intimacy if adult gate fails
2. Read brief + preceding movement + Continuity_Ledger close + Character_Change_Log Snapshot
3. If Focus unlocked: allow pressure-driven Focus shift (silent)
4. Resolve Bias State (ACTIVE vs DORMANT) silently
5. Body reaction first (folded into narrative — no brackets)
6. If Bias ACTIVE: prism + misconstrued hearing — behavior only
7. If transformation pressure occurs: apply deltas silently during generation (do not print)
8. Honor style lock and voice polarization (Rules_Index)
9. Emit prose only. No footer, no audit appendix, no matrix notes.
10. **On approval — Post-Movement Commit:** write Continuity_Ledger row **and** Character_Change_Log (Snapshot + History). Both ledgers required. Do not write evolution onto character cards.

---

*Install once per book project. Load for draft sessions. Execute on movement/scene creation. Never print the runtime on the page.*
