# Characters Directory

Named fictional people are the **unit of load**. Archetypes A–F are voice/matrix templates only ([Main.md](../Framework/Main.md) §5, [voices.md](../Framework/Mechanics/voices.md)).

## Card format

Character cards are **pure YAML** (`.md` extension for tooling compatibility):

- Entire card is a single YAML document between `---` fences
- Structured fields: identity, psyche matrix, `transformation_weights` (**build defaults**), `depth_of_knowledge`, `voice`, `history_anchors`, `scene_seeds`
- One-line load protocol after the closing `---`
- No movement history on the card — evolution lives in [Character_Change_Log.md](../Framework/Character_Change_Log.md)
- No duplicate markdown tables — the YAML is the identity source of truth

## Drafting flow

1. Author names on-scene characters.
2. System loads `Characters/[slug].md` (or a pasted card).
3. Overlay [Character_Change_Log.md](../Framework/Character_Change_Log.md) Current Snapshot when present (Focus, weights, baseline somatic, bias_strength).
4. Silent live state: Focus, Latents, Bias, Somatic, and Voice.
5. [Main.md](../Framework/Main.md) + [Rules_Index.md](../Framework/Rules_Index.md) + [realm_data.yaml](../Framework/Psychology/realm_data.yaml) execute on movement/scene — no bare archetype letter.
6. On approval: update Continuity_Ledger + Character_Change_Log (not the card).

## Files

- [`_template.md`](./_template.md) — copy for new characters
- Demo cards (`reed`, `helen`, `cass`, `wren`, `nora`, `lior`) — optional tests only; not required for novels
- [`Relations.md`](./Relations.md) — central relationship dynamics index
- Evolution ledger: [`../Framework/Character_Change_Log.md`](../Framework/Character_Change_Log.md)

## Adding a novel character

1. Copy `_template.md` → `Characters/[slug].md` (or run [character_builder_prompt.md](../Framework/Prompts/character_builder_prompt.md))
2. Fill YAML fields: **age**, **canon_adult**, physical, cultural_bias
3. Fill psyche matrix from Main + realm_data.yaml
4. Voice: nearest A–F base under `voice:`, then override with idiolect on the card
5. Drafting: load Main + Rules_Index + realm_data.yaml + this card
