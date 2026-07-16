# Cognitive Middleware

**An invisible cognitive matrix for character-driven fiction drafting.**  
Body-first psychology, bias distortion, and realm-aware somatics — all running silently off-page.

---

## What It Is

**CognitiveMiddleware** (formerly PsycheFramework) is a sophisticated runtime engine developed primarily for **"Belief and Love"** (and compatible with related private works such as *A Wanderer’s Guide to the Gates*). It enables consistent, psychologically rich characters through:

- **Body Before Insight** — Physical reactions and somatic tells always precede psychological explanation.
- **Character-First** — Named characters from card files are the single source of truth.
- **Prism Distortion** — Active biases warp how characters receive and interpret the world (shown through behavior, never labeled).
- **100% Off-Page** — The entire matrix stays invisible in the final prose. No realm numbers, bias names, or system terms appear on the page.
- **Great Wheel Integration** — Somatic and bracing/release profiles for all 10 Realms.

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

1. Clone or copy this framework into your book project folder ("Belief and Love" or compatible private repo).
2. Run `deploy_framework.py` (optional but recommended) to set up structure.
3. For every drafting session, load:
   - `Framework/Main.md`
   - `Framework/Rules_Index.md`
   - `Framework/Psychology/realm_index.md`
   - Relevant character cards from `Characters/`

4. Write movements/scenes using the brief + cards. The matrix runs silently.

---

## Key Files

| File | Purpose | Load? |
|------|---------|-------|
| `Framework/Main.md` | Core engine, workflow, commands, and principles | **Always** |
| `Framework/Rules_Index.md` | Hard bans, cleanup protocol, dialogue rules | **Always** |
| `Framework/Psychology/realm_index.md` | Somatic profiles for all 10 Realms | **Always** |
| `Characters/` | Individual character cards (Focus, Latents, Bias, Voice, etc.) | Per scene |
| `Framework/Mechanics/` | Prose styles, sexuality rules, voice templates, humanity details | As needed |
| `Framework/Prompts/` | Supporting prompt templates | Reference only |
| `RolePlaying/RoleplayEngine.md` | Self-contained somatic character RP engine (separate from drafting) | RP only |

**Never load into generation context:**
- `source_changes.md`
- `formatting_rules.md`
- Entire `Prompts/` folder
- Superseded stubs (`psyche_framework.md`, `Drafting_Workflow.md`)

---

## Author Commands (Drafting)

| Command | Effect |
|---------|--------|
| Load character card | Silent state load (name + card) |
| `/create …` | Build minimal new card |
| `/focus N` | Lock active Focus to Realm N |
| `/focus unlock` | Allow dynamic Focus shifts |
| `/bias active` / `dormant` | Force bias state |
| `/style <id>` | Lock prose style |
| `/style unlock` | Allow style change |
| `/18+ on` / `off` | Enable/disable heat (only if Canon Adult = YES) |
| `/reset` | Clear session state |

---

## Character Cards

Cards live in `Characters/`. Each contains:
- Name, Age, Canon Adult flag
- Active Focus + Latents
- Bias (with state)
- Somatic profile
- Voice characteristics
- History anchors

Use the `_template.md` to create new ones. Archetypes A–F in `Main.md` are starting templates only.

---

## Rules Highlights

- **No system language on page** (Realms, Focus, Bias, Prism, etc.)
- **Body first** — never psychological summaries or therapy language
- **Imperfect memory** — blur, deflect, trigger only
- **Asymmetric dialogue** — characters talk past each other
- **Pattern rotation** — fight repetitive AI phrasing across movements
- **Strict cleanup pass** before saving drafts (see Rules_Index §6)

---

## Philosophy in One Line

**The matrix protects the character’s internal logic so the prose can stay honest, embodied, and invisible.**

---

## License & Usage

This framework was built for personal long-form fiction work. Feel free to adapt it for your own projects. Credit appreciated but not required.

---

*Install once. Load for every draft session. Let the matrix run silently. Write clean prose.*
