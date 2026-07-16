---
title: "Prose Protocol"
description: "Optional detail pack governing session-level prose styles and selection/lock states."
type: "supplementary_protocol"
role: "Prose style catalog and selection lock state machine"
load_protocol: "Load when styling overrides or catalog auditing are needed"
---

# Prose Protocol
*Optional detail pack. Session defaults and lock-on-select also live in [Main.md](../Main.md) §3a. Load this file only when you need the full catalog/state machine.*

> [!IMPORTANT]
> **Prose style is user-selected.** Do not force the house "Natural / asymmetric" pack (Anthony/Barker lane) unless chosen.  
> **Default = `llm`** (model fluent prose), status **unlocked** until the writer makes an explicit style choice.  
> **Once the writer selects a style, it LOCKS** for the rest of the session (or until explicit unlock / full reset).

Psychology (matrix, voice, somatics) stays in force regardless of style. Style only changes **how the narrative is written**, not who the character is.

---

## Related

- **Drafting entry:** [Main.md](../Main.md)
- **Natural / asymmetric pack (optional):** [natural_prose.md](../natural_prose.md)
- **Card-building voices:** [voices.md](./voices.md)
- **Hard bans:** [Rules_Index.md](../Rules_Index.md)

---

## 1. Why lock (design intent)

LLMs drift. Mid-scene they "improve" cadence, slide toward house texture, or flatten hardboiled into generic literary. A **locked prose style** is a session contract:

- One narrative register per continuous draft / RP run
- Character switches do **not** change style (style is session-level, not card-level)
- Audits compare prose against the locked ID, not a moving target

Unlock remains available so the writer stays in control — but unlock is never silent or accidental.

---

## 2. Selection + lock state machine

Live fields:

| Field | Values | Meaning |
|:---|:---|:---|
| **Prose Style** | catalog ID (`llm`, `natural`, …) | Active register |
| **Style Lock** | `UNLOCKED` \| `LOCKED` | Whether the style may change freely |

### Rules

1. **Session start:** `Prose Style = llm`, `Style Lock = UNLOCKED` (unless the movement brief / first message already names a style — then apply that style and set **LOCKED** immediately).
2. **Explicit selection locks:**
   - `/style <id>`
   - `/style custom: …`
   - Clear natural language: "use hardboiled," "write in natural prose," "anthony/barker," "lock style to cinematic"
   - Drafting brief line: `Prose Style: natural` (or any ID)
3. On explicit selection: set the style, set **`Style Lock = LOCKED`**, confirm in a one-line system note: `Style locked: <id>`.
4. **While LOCKED:**
   - Ignore casual or implied style drift ("make it prettier," "more literary," model self-rewrite urges).
   - Refuse style changes with a short note: `Style is locked (<id>). Use /style unlock then /style <new>, or /style force <id>.`
   - Do **not** quietly migrate toward `natural` or any other pack.
5. **Unlock (explicit only):**
   - `/style unlock` → `Style Lock = UNLOCKED`; style ID unchanged until next select
   - `/style force <id>` → set new style and keep **LOCKED** (intentional replace without two steps)
   - `/reset` → `llm` + **UNLOCKED**
6. **While UNLOCKED:**
   - The LLM **must not** drift toward any specific style pack characteristics (natural, literary, etc.).
   - Maintain current style's register until explicit selection.
   - UNLOCKED means "user can change freely," not "LLM can migrate freely."
7. **Auto-lock after first response:** If Style Lock = UNLOCKED after first character response and no explicit style was set, **automatically set Style Lock = LOCKED** with current style (`llm`). Print confirmation: `Style auto-locked to llm. Use /style to change.`
8. If style is **`llm`**: do **not** load `natural_prose.md`. If **`natural`**: load it fully.
9. Character **dialogue voice** still follows the character card. Style ≠ character voice.
10. Hard gates never change with style: Canon Adult / 18+, never-name-the-system, no speaking for the user (playground), imperfect recall when humanity is loaded.

---

## 3. Style catalog

| ID | Name | When to use | Engine notes |
|:---|:---|:---|:---|
| **`llm`** / **`default`** | Model default | Ordinary LLM fluency | No house-style constraints. Clear, competent narrative. Still honor character voice + matrix. |
| **`natural`** | Natural / asymmetric (house) | Anti-AI texture: jagged rhythm, drift, fumble, anti-synthesis | **Load full** [natural_prose.md](../natural_prose.md). Anthony/Barker-adjacent — optional, not automatic. |
| **`clean`** | Clean commercial | Genre readability | Short–medium sentences, clear beats, light sensory, minimal figurative density. |
| **`literary`** | Literary lyrical | Interior, image-led | Longer cadence allowed; image and motif; still no therapy summary endings unless user asks. |
| **`hardboiled`** | Hardboiled / lean | Crime, noir pressure | Spare verbs, concrete nouns, dry understatement, minimal adverb. |
| **`cinematic`** | Cinematic | Scene-as-shot | Visual framing, cut-friendly paragraphs, external action over interior essay. |
| **`minimal`** | Minimal | Extreme restraint | Short lines, white space, almost no figurative language. |
| **`romantic`** | Warm romantic | Soft heat, non-explicit by default | Gesture and timing; avoid purple metaphor stacks. |
| **`custom`** | User-defined | User pastes a style brief | Follow their brief only; do not re-impose `natural` rules. |

Aliases:

- `default`, `normal`, `standard`, `model` → **`llm`**
- `house`, `asymmetric`, `anthony`, `barker`, `anthony/barker`, `anti-ai` → **`natural`**
- `noir`, `lean` → **`hardboiled`**
- `film`, `screen` → **`cinematic`**
- `sparse` → **`minimal`**

---

## 4. What always stays on (style-invariant)

| Layer | Stays on? |
|:---|:---|
| Character card / Focus / Bias / Prism | Yes |
| Character dialogue voice (A–F / card) | Yes |
| Canon Adult / 18+ gate | Yes |
| Never name realm/bias/trauma in character | Yes |
| Humanity: imperfect recall, biased hearing (if protocol loaded) | Yes |
| `natural_prose.md` jagged / fumble / anti-synthesis rules | **Only if style = `natural`** |
| Style lock once set | Yes, until unlock / force / reset |

---

## 5. Drafting vs chat RP (style)

| Context | Style control |
|:---|:---|
| **Drafting** ([Main.md](../Main.md)) | Brief or `/style` sets style → **LOCKED** for the pass |

### Output (drafting vs chat RP)

| Context | Somatics | Debug / matrix |
|:---|:---|:---|
| **Drafting** ([Main.md](../Main.md)) | Fold into narrative. **No brackets.** | **Never** print CONFIG, matrix notes, audit tables, or engine labels |

**Hard ban:** Do not dump turn-loop state, Focus/Bias labels, "Prism intercept", remnant/passage jargon, or post-scene matrix footnotes into draft files.

---

## 6. Commands / brief lines

```
/style llm              → set llm, LOCK
/style natural          → set natural, LOCK
/style hardboiled       → set hardboiled, LOCK
/style custom: …        → set custom brief, LOCK
/style unlock           → UNLOCK (style ID unchanged)
/style force cinematic  → set cinematic, stay LOCKED
/style                  → report current style + lock state
```

Drafting brief:

```
Prose Style: natural
Style Lock: LOCKED
```

---

## 7. Audit

1. What style is active, and is it **LOCKED**?
2. If LOCKED, refuse silent restyle; require unlock or force.
3. If `llm` → do **not** rewrite toward natural/asymmetric or any other style pack.
4. If `natural` → apply [natural_prose.md](../natural_prose.md) fully.
5. If UNLOCKED → maintain current style's characteristics; no drift toward any style pack.
6. After first character response with UNLOCKED style → verify auto-lock occurred.
7. Character voice fidelity is audited separately from prose style.
