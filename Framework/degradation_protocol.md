# Context-Budget Degradation Protocol
*Optional active context optimization framework for token-constrained environments.*

This protocol defines the standard degradation hierarchy for compressing the loaded context stack when running in token-constrained LLM environments (such as ChatGPT, Claude projects, or custom 32k/128k context windows).

---

## 1. Context Capacity Tiers

Operate in one of the three tiers depending on the LLM's active context usage warnings or token constraints:

| Tier | Context Window | Mode | Action |
| :---: | :--- | :--- | :--- |
| **Green** | > 100k tokens | **Full Stack** | Load full canonical manifest (no modifications needed). |
| **Yellow** | 30k – 100k tokens | **Compact Stack** | Apply Phase 1 compression (trim prose history & logs). |
| **Red** | < 30k tokens | **Minimal Stack** | Apply Phase 2 compression (trim realms database & outline). |

---

## 2. Phase 1 Compression (Yellow Tier)

Apply these rules when context warnings occur or when approaching 30k–50k tokens:

### A. Prose Compression (Preceding Reads)
- **Standard:** Load all prior drafted movements in the active chapter.
- **Yellow Rule:** Load **only the immediately preceding movement** (Movement $N-1$) in full. Unload all earlier movements in the active chapter.

### B. Character Log Compression
- **Standard:** Load full `Characters/[slug]_log.yaml` including snapshots and entire historical entry lists.
- **Yellow Rule:** Limit the loaded character log `history` array to the **last 3 entries** only. Keep the snapshot intact.

### C. Reference File Unload
- **Standard:** Load `formatting_rules.md`, stubs, and full reference guidelines.
- **Yellow Rule:** Unload `formatting_rules.md`, `load_protocol.md`, and all stubs (`psyche_framework.md`, etc.). Rely exclusively on the concise [Rules_Index.md](Rules_Index.md) for style and cleanup.

---

## 3. Phase 2 Compression (Red Tier)

Apply these rules in extremely tight context environments (<30k tokens):

### A. Somatic / Staging Anchor Only (Prose Strip)
- **Red Rule:** Do **not** load the full text of preceding movements. Instead, load only the **last 5 paragraphs** of the preceding movement to recover the somatic close, props positioning, and environment anchors.

### B. Log Snapshot Only
- **Red Rule:** Completely **strip the `history` array** from all loaded `_log.yaml` character states. Inject only the single `snapshot` block containing active focus, latent weights, default somatic, and bias strength.

### C. Realm Database Pruning
- **Standard:** Load the complete `realm_data.yaml` (somatic behaviors for all 10 Realms).
- **Red Rule:** Unload `realm_data.yaml` entirely. Instead, copy/inject only the YAML profiles for the **specific active and latent realms** of the characters actively on-scene in this session.

### D. Macro Outline Strip
- **Standard:** Load the full `Novel_Outline.md` or `World_Architecture.md`.
- **Red Rule:** Unload outline and world bible files. Instead, load only a **single-paragraph summary** of the active chapter's narrative goal and location.

---

*Load for memory optimization. Maintain somatic integrity at minimal token footprints.*
