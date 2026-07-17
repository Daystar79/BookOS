# Chapter & Movement Continuity Ledger
*Canonical Continuity Map & Timeline Reference*

This ledger is the source of truth for **narrative timeline, locations, and scene-close somatic anchors** across drafted movements. Review this ledger, linked drafts, **Character_Change_Log**, and character cards before any design or drafting session.

**Session boot:** Main.md **Ledger Integrity Pass** runs first — placeholder rows are not data; honest empty is valid.

---

## Dual ledger save (with Character Logs)

On **every approved movement**, write this story ledger, update the individual character logs, and sync the consolidated visual reference log:

| Save | Where | Owns |
|:---|:---|:---|
| **Story ledger** | This file | Day/time, draft path, **scene** somatic close, continuity & plot beats, open loops |
| **Character change log** | `Characters/[slug]_log.yaml` | Durable matrix snapshot + append-only history (primary data load source) |
| **Consolidated log** | `Framework/Character_Change_Log.md` | Human-readable quick-reference snapshot and history for all characters |

- Scene close lives here; matrix evolution lives in the character's `_log.yaml` and is summarized in `Framework/Character_Change_Log.md`.
- Character cards stay identity/load sheets — do not append movement history to card YAML.
- Temporary tells: this ledger only. Medium+ / permanent matrix shifts: `Characters/[slug]_log.yaml` (and `Framework/Character_Change_Log.md`) required.
- Next session: Ledger Integrity Pass → this ledger (latest real row) + active character logs + on-scene cards.

### Somatic State on Close (column guide)
Per on-scene character, one compact clause — e.g. `Reed: jaw locked, high shoulders; Helen: open hands, soft chest`. Scene-close body only. If baseline permanently changed, update the character's `_log.yaml` snapshot and the consolidated log (not the card).

### Empty vs placeholder
| State | Meaning |
|:---|:---|
| **Honest empty** | Headers only; no movement rows. Correct when no movement is approved yet. |
| **Placeholder (invalid as data)** | Cells like `[Day & Time]` or links to drafts that do not exist. Integrity Pass **deletes** these as rows. |
| **Committed** | Real time, real somatic close, existing draft path, Change log: yes. |

---

## Act One

| Ch / Mov | Draft File | Day & Time | Somatic State on Close | Crucial Continuity & Plot Beats |
| :---: | :--- | :--- | :--- | :--- |
| **1 M1** *(sample)* | [Drafts/samples/draft_chapter_1_m1.md](../Drafts/samples/draft_chapter_1_m1.md) | Day 1 · ~18:40 · forge shop after close | **Reed:** jaw set, scar-rub, keys cutting palm, shoulders still high; tea finished as payment. **Helen:** hand withdrawn, coat on, inventory look unfinished at threshold | Helen brings cold tea + touch-care; Reed reframes as debt (hinge “no charge”); unpaid favor tension persists; second cup left untouched; Helen returns Saturday with food. Demo sample — not novel canon. · Change log: **yes** |

---

## Act Two

| Ch / Mov | Draft File | Day & Time | Somatic State on Close | Crucial Continuity & Plot Beats |
| :---: | :--- | :--- | :--- | :--- |

*(no approved movements)*
