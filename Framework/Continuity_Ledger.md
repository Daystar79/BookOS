# Chapter & Movement Continuity Ledger
*Canonical continuity map and timeline reference*

This ledger is the source of truth for **narrative timeline, locations, and scene-close somatic anchors** across drafted movements. Review this ledger, linked drafts, character logs, and character cards before any design or drafting session.

**Session boot:** Main.md **Ledger Integrity Pass** runs first — placeholder rows are not data; honest empty is valid.

---

## Post-Movement State Commit

On **every approved movement**, execute the Post-Movement State Commit:
1. Write story continuity.
2. Update canonical per-character runtime state (`Characters/[slug]_log.yaml`).
3. Regenerate or synchronize the consolidated human-readable log (`Framework/Character_Change_Log.md`).

| Save | Where | Owns |
|:---|:---|:---|
| **Story ledger** | This file | Day/time, draft path, **scene** somatic close, continuity & plot beats, open loops |
| **Character log** | `Characters/[slug]_log.yaml` | Durable matrix snapshot + append-only history (primary runtime data) |
| **Consolidated log** | `Framework/Character_Change_Log.md` | Human-readable quick-reference snapshot and history for all characters |

- Scene close lives here; matrix evolution lives in `Characters/[slug]_log.yaml` (summarized in Character_Change_Log).
- Character cards stay identity/load sheets — do not append movement history to card YAML.
- Temporary tells: this ledger only. Medium+ / permanent matrix shifts: update `_log.yaml` (and Character_Change_Log).
- Next session: Ledger Integrity Pass → this ledger (latest real row) + active character logs + on-scene cards.

### Somatic State on Close (column guide)
Per on-scene character, one compact clause — e.g. `Name: jaw locked, high shoulders`. Scene-close body only. If baseline permanently changed, update that character's `_log.yaml` snapshot (not the card).

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

*(no approved movements)*

---

## Act Two

| Ch / Mov | Draft File | Day & Time | Somatic State on Close | Crucial Continuity & Plot Beats |
| :---: | :--- | :--- | :--- | :--- |

*(no approved movements)*
