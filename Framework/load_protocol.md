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

## Optional Modules (Load as Needed)
- `Framework/Mechanics/humanity.md` — Extra body-pacing detail
- `Framework/Mechanics/prose.md` — Full style catalog
- `Framework/Mechanics/voices.md` — Building new cards
- `Framework/natural_prose.md` — Style = `natural` only

## Never Load for Generation
- `Framework/Archives/*` (historical artifacts)
- `Framework/source_changes.md` (archived)
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

*Use this file as a reference. Do not load it as a runtime file.*
