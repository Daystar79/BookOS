---
title: Standard Framework Load Protocol
type: reference
description: Common load order and file references for all Psyche Matrix operations
load_priority: 0
---

# Standard Load Protocol
*Reference for all prompts and workflows. Always load in this order unless specified otherwise.*

---

## Core Framework (Always Load)
1. `Framework/Main.md` — Core engine, workflow, and principles
2. `Framework/Rules_Index.md` — Hard bans, cleanup protocol, dialogue rules
3. `Framework/Psychology/realm_data.yaml` — Somatic profiles for all 10 Realms

## Character Data
4. On-scene character cards from `Characters/` directory
5. `Characters/[slug]_log.yaml` — individual character logs for on-scene characters (overrides card Focus/weights/baseline somatic when present)
6. `Framework/Continuity_Ledger.md` — latest scene close / timeline (design & draft)

## First action after load
7. **Ledger Integrity Pass** (`Main.md`) — clean empty/placeholder ledgers before design or draft

## Optional Modules (Load as Needed)
- `Framework/Mechanics/humanity.md` — Extra body-pacing detail
- `Framework/Mechanics/prose.md` — Full style catalog
- `Framework/Mechanics/voices.md` — Building new cards
- `Framework/natural_prose.md` — Style = `natural` only

## Never Load for Generation
- `CHANGELOG.md` (product history — agents update on maintenance; not runtime)
- `AGENTS.md` (agent contract — maintenance only)
- `Framework/Archives/*` (historical artifacts)
- `Framework/source_changes.md` (session/design locks — not runtime)
- `Framework/Drafting_Workflow.md` (stub, archived)
- `Framework/psyche_framework.md` (stub, archived)
- `Framework/Prompts/*` (reference only, not runtime)

---

## Character Card Load Instruction
*Standard load comment for all character cards:*

```
*Load: See _template.md*
```

---

# Reference: Continuity Ledger Protocol

### Dual Ledger Save
On **every approved movement**, write the story ledger, update the individual character logs, and sync the consolidated visual reference log:
*   **Story Ledger (`Framework/Continuity_Ledger.md`):** Owns day/time, draft path, scene somatic close, continuity & plot beats, open loops.
*   **Character Change Log (`Characters/[slug]_log.yaml`):** Owns durable matrix snapshot + append-only history (primary data load source).
*   **Consolidated Log (`Framework/Character_Change_Log.md`):** Human-readable quick-reference snapshot and history for all characters.

### Somatic State on Close Guidelines
Per on-scene character, write one compact clause representing their close-of-scene bodily state — e.g. `Reed: jaw locked, high shoulders; Helen: open hands, soft chest`. Scene-close body only. If baseline permanently changed, update the character's `_log.yaml` snapshot and the consolidated log (not the card).

### Empty vs Placeholder States
*   **Honest Empty:** Headers only; no movement rows. Correct when no movement is approved yet.
*   **Placeholder (invalid as data):** Cells like `[Day & Time]` or links to drafts that do not exist. Integrity Pass deletes these as rows.
*   **Committed:** Real time, real somatic close, existing draft path, Change log: yes.

---

# Reference: Character Change Log Protocol

### Load Order (Next Design/Draft)
1. On-scene character cards (identity, voice, bias name, build defaults)
2. **Canonical mutable runtime state:** per-slug `_log.yaml` snapshot (overrides card Focus / weights / baseline somatic / bias_strength when present)
3. `Framework/Continuity_Ledger.md` latest real row (scene time, props, close body state)

### Integrity Mapping
*   **Snapshot Empty:** Seed from active cards (`As of: build`)
*   **History Empty (no Continuity rows):** OK — do not invent entries.
*   **Continuity has committed rows, History missing those movements:** Backfill or block draft.

---

*Use this file as a reference. Do not load it as a runtime file.*
