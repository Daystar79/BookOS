# BookOS — Cognitive Middleware & Writer's OS

**An invisible, token-optimized cognitive matrix for character-driven fiction drafting and somatic roleplay.**  
Body-first psychology, bias distortion, and realm-aware somatics — running silently off-page.

---

## What It Is

**BookOS** is a sophisticated runtime engine developed for character-driven long-form fiction. It enables consistent, psychologically rich characters through:

- **Body Before Insight** — Physical reactions and somatic tells always precede psychological explanation.
- **Character-First** — Named characters from card files are the single source of truth.
- **Tripartite Filtering** — Worldview filters split into background world-filters (Cultural Bias & Occupation) and a dynamic situational filter (Cognitive Bias / Wound) that remains dormant at rest.
- **100% Off-Page** — The entire matrix stays invisible in the final prose. No realm numbers, bias names, or system terms appear on the page.
- **Great Wheel Integration** — Somatic and bracing/release profiles for all 10 Realms.
- **Transformation Engine** — Dynamic evolution or regression of character attributes based on narrative pressure and somatic tells.

The framework is designed to fight common AI writing problems: therapy-speak, perfect recall, symmetric dialogue, pattern repetition, and on-page system leakage.

---

## Core Philosophy

- The matrix is a **tool for the writer**, not content for the reader.
- Characters are not therapists, narrators, or helpful assistants.
- Memory is imperfect and biased. Recall is triggered somatically, not on command.
- Style, focus, and bias state are controllable but never visible in the output.
- Adult/sexual content is strictly gated and never enabled by default.

---

## Quick Start

1. Clone or copy this framework into your book project folder.
2. Run `deploy_framework.py` (optional but recommended) to set up the directories.
3. **Read the sample (optional):** `Drafts/samples/draft_chapter_1_m1.md` — Reed + Helen demo movement with dual ledger commits already filled (`Continuity_Ledger` + `Character_Change_Log`). See `Drafts/samples/README.md`.
4. For every drafting session, load:
   - `Framework/Main.md`
   - `Framework/Rules_Index.md`
   - `Framework/Psychology/realm_data.yaml`
   - Relevant character cards from `Characters/`
   - Both ledgers (after **Ledger Integrity Pass**)
5. Write movements/scenes using the brief + cards. The matrix runs silently.
6. On approval: dual ledger save. Run the linter:
   ```bash
   ./Framework/linter.py Drafts/
   ```

---

## Key Files & Directories

| File/Folder | Purpose | Usage / Load |
|------|---------|--------------|
| `Framework/Main.md` | Core engine, workflow, commands, and principles | **Always load** |
| `Framework/Rules_Index.md` | Hard bans, cleanup protocol, dialogue rules | **Always load** |
| `Framework/Psychology/realm_data.yaml` | Somatic profiles for all 10 Realms (optimized string format) | **Always load** |
| `Framework/linter.py` | Automated prose linter to check for system leaks | Command-line utility |
| `Characters/` | Active character cards and per-character change logs (`_log.yaml`) | Load per scene |
| `Characters/Physical/`, `/Somatic/`, `/Aesthetics/` | Subfolders holding genre-specific physical, somatic, and visual templates | Loaded by Character Builder |
| `Factions/` | Isolated cards for organisations, guilds, and political groups | Load per scene requirements |
| `Templates/` | Global genre blueprints (Sci-Fi, High Fantasy, Dark Romance, etc.) | Loaded by World/Character Builder |
| `Framework/Mechanics/` | Prose styles, voice templates, humanity details | Load as needed |
| `Modules/` | Optional active modules (e.g. `sexuality.yaml` in YAML format) | Load when enabled |
| `Framework/Prompts/` | Interactive novel initializer, world, and character builders | Reference only |
| `RolePlaying/RoleplayEngine.md` | Self-contained somatic character RP engine. **Designed to be dropped directly into a chat window** (e.g., Gemini CLI, Web interface, or Claude session) to start a live interactive roleplay session. | Drop into Chat |

---

## Author Commands (Drafting & RP)

| Command | Effect |
|---------|--------|
| Load character card | Silent state load (name + card) |
| `/create …` | Build minimal new card |
| `/focus N` | Lock active Focus to Realm N |
| `/focus unlock` | Allow dynamic Focus shifts |
| `/bias active` / `dormant` | Force bias state (Active distorts perception, Dormant acts normally) |
| `/style <id>` | Lock prose style |
| `/style unlock` | Allow style change |
| `/18+ on` / `off` | Enable/disable heat (only if Canon Adult = YES) |
| `/transform event: <desc> strength: <level>` | Force a transformation pressure calculation |
| `/reset` | Clear session state |

---

## Tripartite Filter System

1. **Cultural Bias (Background):** Metaphysical frame, ethical defaults, and **temporal awareness** (how they track time/destiny, e.g., cyclic liturgy vs. linear progress).
2. **Occupation & Species (Background):** Technical lexicon, prop/tool familiarity, and somatic/physical defaults (species defaults to `human` but maps to custom configurations like Elves, Dwarves, or aliens).
3. **Cognitive Bias (Triggered):** Wound-based perception warp. Stays **DORMANT** during casual beats, intercepting inputs only when emotional pressure activates it.

---

## Transformation & Evolution

Character cards hold **build defaults** (`transformation_weights`: active_focus dominance, latent anchors, bias_strength, somatic_flexibility).  
**Runtime evolution** is tracked separately in `Framework/Character_Change_Log.md` (Current Matrix Snapshot + Movement History) — not on the card.

**Session boot:** **Ledger Integrity Pass** first (Main.md) — honest empty ledgers are fine; placeholder rows and dual-commit lag are fixed or block drafting.

**Post-Movement Commit (mandatory dual ledger save):** On each approved movement, update:
1. `Framework/Continuity_Ledger.md` — timeline, scene somatic close, plot beats  
2. `Characters/[slug]_log.yaml` — the individual YAML change log for each on-scene character who experienced matrix pressure or durable shifts (for data loading).
3. `Framework/Character_Change_Log.md` — the consolidated, human-readable change log (for quick reference).

Cards stay identity/load sheets. Neither ledger alone is enough.

---

## Historical & Safety Gates (Roleplaying)

- **Safety Gating:** Strict prohibition of Lolicon/Shotacon tropes. Canon verification is required for 18+ Anime/Hentai imports.
- **Historical Figures:** Lifespan/active era must be specified. Character cards prioritize their **own writings/primary documentation**, falling back to the cultural and temporal bias of their era only when documentation is lacking. Modern or post-era concepts are strictly banned from their awareness. Under no circumstances may the AI engine break character or use external search/lookup tools to resolve historical gaps during active roleplay.

---

## Automated Prose Linter (`linter.py`)

Run `Framework/linter.py` on your drafts to scan for:
- **System Leaks:** On-page mentions of Realms, biases, and matrix weights.
- **Therapy-Speak:** Jargon like *wound*, *trauma*, *trigger*, or *reframe*.
- **Dialogue Tags/Fillers:** Banned markers like *whispered*, *Are you okay*, and *said quietly*.
- **Formatting Breaks:** Excessive horizontal rules (`---`) separating real-time actions.

---

*Install once. Load for every session. Let the matrix run silently. Write clean prose.*

---

## License

BookOS uses a hybrid open-source license model:
* Software components (such as [linter.py](file:///mnt/Book/BookOS/Framework/linter.py)) are licensed under the **MIT License**.
* Creative content, manuals, character card formats, and YAML schemas are licensed under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**.

See [LICENSE.md](file:///mnt/Book/BookOS/LICENSE.md) for full license details.
