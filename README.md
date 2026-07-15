# BookOS — AI-Assisted Creative Writing Operating System
*A modular, rule-bounded framework for planning, designing, drafting, and auditing high-concept fiction.*

---

## What is BookOS?

BookOS is a modular pipeline that acts as a cognitive writing companion. It splits the creative process into clear, isolated layers to prevent configuration drift, combat generic AI-writing tropes, and enforce strict stylistic consistency.

Rather than relying on ad-hoc prompts, BookOS runs on a structured folder database, character voice engines, and psychological profiles (the **Psyche Matrix**), keeping all system instructions silent and off-page.

---

## Current state of this repo

| Layer | Status |
|:---|:---|
| **Core runtime** (`Main.md`, `Rules_Index.md`, `realm_index.md`) | Ready — load for every draft |
| **Design / audit prompts** | Ready — load lists aligned to core |
| **Optional modules** (`Modules/`) | Registry only — no module files shipped yet |
| **Book-local files** (outline, world, rites, drafts) | Empty until you run bootstrap |
| **Demo cast** (`Characters/reed` … `lior`) | Playground tests only — not required for novels |

---

## Project Directory Map

```
├── Characters/
│   ├── _template.md           # Template for new character cards
│   ├── Relations.md           # Central dynamics index
│   ├── README.md
│   └── [slug].md              # Demo cards (optional) or your cast
├── Drafts/                    # Movement drafts, Completed/, master manuscript
├── Framework/
│   ├── Main.md                # Psyche Matrix runtime + draft workflow
│   ├── Rules_Index.md         # Hard bans, dialogue, cleanup
│   ├── Modules.md             # Optional module registry (all DISABLED)
│   ├── Design_QA_Protocol.md  # Interactive design session rules
│   ├── Drafting_Prompt.md     # Active brief + session position
│   ├── Continuity_Ledger.md   # Timeline / somatic close map
│   ├── Mechanics/             # Optional: voices, humanity, prose
│   ├── Psychology/
│   │   └── realm_index.md     # Realms I–X brace / release / somatic
│   ├── Prompts/               # Bootstrap, design, audit, polish prompts
│   ├── TBD/                   # Movement design archives
│   ├── Setup/                 # Archive completed bootstrap prompts here
│   └── Corrections/           # Pending correction notes
├── Modules/                   # Future optional packs (empty until shipped)
├── Sources/                   # Research notes for world-builder
├── Audits/                    # Audit reports (gitignored by default)
├── Build/ · Releases/ · Images/
└── README.md
```

---

## Honest load stack (draft session)

Always:

1. `Framework/Main.md`
2. `Framework/Rules_Index.md`
3. `Framework/Psychology/realm_index.md`
4. On-scene cards from `Characters/`
5. Active Movement Brief in `Drafting_Prompt.md`
6. `Framework/Modules.md` (scan for ENABLED — usually none)

Optional: `natural_prose.md`, Mechanics supplements, book-local outline/world/rites **if present**.

Never for generation: `psyche_framework.md`, `Drafting_Workflow.md` (superseded stubs).

---

## The Creative Pipeline (How to Use)

### Phase 1: Bootstrapping (Run Once)

Run these interactive prompts in order. They **create** book-local files under `Framework/` (they are not shipped empty on purpose).

After you finish a bootstrap prompt, **move it yourself** into `Framework/Setup/` so `Prompts/` stays clean (this is not automatic).

1. **Initialize Novel** (`Prompts/initialize_novel_prompt.md`) → writes `Framework/Novel_Outline.md`
2. **Build Characters** (`Prompts/character_builder_prompt.md`) → `Characters/[slug].md` + `Relations.md`
3. **Build World** (`Prompts/world_builder_prompt.md`) → `World_Architecture.md` (+ `Rite_Reference.md` if needed)
4. **Design Plot** (`Prompts/PlotDesigner.md`) → `Novel_Master_Outline.md`

Until those files exist, design/draft sessions should treat them as **optional / if present**.

---

### Phase 2: Recurring Writing Loop

For every individual scene (movement):

```mermaid
graph LR
    A[MovementDesigner.md] -->|1. Run Q&A| B(Design Brief)
    B -->|2. Save to TBD/| C[TBD/chapter_N_mM_design.md]
    C -->|3. Paste Active Brief| D[Drafting_Prompt.md]
    D -->|4. Run /draft| E(Prose Generation)
    E -->|5. Write Draft| F[Drafts/draft_chapter_N_mM.md]
```

1. **Scene Design:** Run **`Prompts/MovementDesigner.md`** (follow `Design_QA_Protocol.md`). Builds a **Movement Brief**; save full QA to `Framework/TBD/`.
2. **Scene Setup:** Paste the active brief into **`Framework/Drafting_Prompt.md`**.
3. **Drafting:** Load the honest stack above + brief; run **`/draft`**. Prefer the **lean draft preceding-read** in Main §2 (not the heavier design load).
4. **Prose Hygiene:** Only narrative prose goes to draft files. Matrix jargon stays off-page.

**Tool roles (not vendor-locked):** use a long-context agent for design/audit when the whole manuscript must fit; use a prose-focused agent for drafting. Gemini CLI is a common long-context choice; Cursor/Grok are common for craft — either role can use any capable model.

---

### Phase 3: Auditing & Polish

* **Manuscript Integrity Audit:** `Prompts/FullBookAudit.md` — timeline, voice protocol, file sync, release readiness.
* **Surgical Band Polish:** `Prompts/improvement_pass_prompt.md` — scoped irony / sensory / cadence fixes after the band is closed.

---

## Bias State (quick)

Default **DORMANT** (normal conversation). Becomes **ACTIVE** under pressure, card triggers, or `/bias active` — then Prism + misconstrued hearing apply. See Main §3b and Rules_Index §7.
