# Cognitive Middleware

**An invisible cognitive matrix for character-driven fiction drafting and somatic roleplay.**  
Body-first psychology, bias distortion, and realm-aware somatics — running silently off-page.

---

## What It Is

**CognitiveMiddleware** is a sophisticated runtime engine developed for character-driven long-form fiction. It enables consistent, psychologically rich characters through:

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
3. For every drafting session, load:
   - `Framework/Main.md`
   - `Framework/Rules_Index.md`
   - `Framework/Psychology/realm_data.yaml`
   - Relevant character cards from `Characters/`
4. Write movements/scenes using the brief + cards. The matrix runs silently.
5. Run the linter to ensure no engine terms or banned fillers leaked:
   ```bash
   ./Framework/linter.py Drafts/
   ```

---

## Key Files

| File | Purpose | Usage / Load |
|------|---------|--------------|
| `Framework/Main.md` | Core engine, workflow, commands, and principles | **Always load** |
| `Framework/Rules_Index.md` | Hard bans, cleanup protocol, dialogue rules | **Always load** |
| `Framework/Psychology/realm_data.yaml` | Somatic profiles for all 10 Realms | **Always load** |
| `Framework/linter.py` | Automated prose linter to check for system leaks | Command-line utility |
| `Characters/` | Individual character cards (Focus, Latents, Bias, Voice, etc.) | Load per scene |
| `Framework/Mechanics/` | Prose styles, sexuality rules, voice templates, humanity details | Load as needed |
| `Framework/Prompts/` | Interactive character builder and improvement prompts | Reference only |
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
2. **Occupation (Background):** Technical lexicon, prop/tool familiarity, and immediate staging focus.
3. **Cognitive Bias (Triggered):** Wound-based perception warp. Stays **DORMANT** during casual beats, intercepting inputs only when emotional pressure activates it.

---

## Transformation & Evolution

Character cards support `transformation_weights` tracking:
- `active_focus` dominance and `latent_anchors` weights.
- `bias_strength` and `somatic_flexibility` (rate of physical tell adaptation).
- `transformation_history` tracking permanence of past events.

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
