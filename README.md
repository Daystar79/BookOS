# BookOS — AI-Assisted Creative Writing Operating System
*A modular, rule-bounded framework for planning, designing, drafting, and auditing high-concept fiction.*

---

## What is BookOS?

BookOS is a modular pipeline that acts as a cognitive writing companion. It splits the creative process into clear, isolated layers to prevent configuration drift, combat generic AI-writing tropes, and enforce strict stylistic consistency. 

Rather than relying on ad-hoc prompts, BookOS runs on a structured folder database, specific character voice engines, and psychological profiles (the **Psyche Matrix**), keeping all system instructions silent and off-page.

---

## Project Directory Map

```
├── Characters/
│   ├── _template.md         # Template for building character cards
│   ├── Relations.md         # Central index mapping character dynamics & conflict warps
│   └── [character].md       # Slug-named character cards containing the Psyche Matrix
├── Drafts/
│   ├── Completed/           # Assembled chapter drafts
│   ├── master_manuscript.md # The compiled full book text
│   └── draft_chapter_*.md   # Individual scene-level movement draft files
├── Framework/
│   ├── Main.md              # The core cognitive writing instructions
│   ├── Rules_Index.md       # Canonical hard bans, output hygiene, and formatting rules
│   ├── Design_QA_Protocol.md# Rules governing interactive design sessions
│   ├── Drafting_Prompt.md   # Active writing workspace, brief, and fixes queue
│   ├── Prompts/             # Active writing & auditing commands
│   │   ├── MovementDesigner.md  # Interactive Q&A scene builder
│   │   ├── FullBookAudit.md     # Full manuscript timeline & voice analyzer
│   │   └── improvement_pass_prompt.md # Surgical polish and band polish editor
│   ├── Psychology/
│   │   └── realm_index.md   # Psychological profile rules (Realms I-X)
│   └── Setup/               # Archived initialization pipelines (after execution)
└── Sources/                 # Raw research documents, notes, and background references
```

---

## The Creative Pipeline (How to Use)

### Phase 1: Bootstrapping (Run Once)
Setup the project by running these interactive prompts in order. *Note: Upon completion, each prompt automatically archives itself to `Framework/Setup/` to keep your prompts clean.*

1.  **Initialize Novel (`initialize_novel_prompt.md`):** Configures your genre, tone, and high-level plot, writing the output to `Novel_Outline.md`.
2.  **Build Characters (`character_builder_prompt.md`):** Creates your initial cast cards with Voice Engines and Psyche matrices, and creates the reciprocal mappings in `Characters/Relations.md`.
3.  **Build World (`world_builder_prompt.md`):** Automatically scans any research in `Sources/` or `Research/` to build setting geographical bounds, ranks, and rituals, writing `World_Architecture.md` and `Rite_Reference.md`.
4.  **Design Plot (`PlotDesigner.md`):** Translates your high-level milestones into act divisions and chapter targets, generating `Novel_Master_Outline.md`.

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

1.  **Scene Design:** Run **`MovementDesigner.md`** to perform an interactive Q&A. This builds a **Movement Brief** (outlining POV, present characters, location, and must-land beats) and writes it to `Framework/TBD/`.
2.  **Scene Setup:** Paste the generated active brief into **`Framework/Drafting_Prompt.md`**.
3.  **Drafting:** Load the active session files (`Drafting_Prompt.md` + `Main.md` + `Rules_Index.md` + on-scene character cards) and run the **`/draft`** command to write the scene.
4.  **Prose Hygiene:** The drafting engine writes only clean narrative prose to your draft files. The system rules prevent psychological jargon or debug configurations from leaking onto the page.

---

### Phase 3: Auditing & Polish

*   **Manuscript Integrity Audit:** Load **`FullBookAudit.md`** to check chronological timeline drift, formatting compliance, and per-character voice erosion across the entire manuscript.
*   **Surgical Band Polish:** Load **`improvement_pass_prompt.md`** to perform post-draft polish passes on specific chapter bands, focusing on narrative irony, sensory focus, and stylistic cadences.
