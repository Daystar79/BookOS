---
module_name: "Transformation Engine"
version: "0.1"
enabled: false
compatibility:
  - "requires: realm_index.md and character cards with transformation_weights"
requires:
  - "Character cards must have transformation_weights section"
  - "Events must be described with pressure type and strength"
---
# Transformation Engine — BookOS Optional Module

*Weighted, event-driven character transformation system. Characters evolve (or regress) based on story pressure rather than sudden insight.*

## Core Principles
- Transformation is **weighted and gradual**.
- Changes are **somatic-first** — body and behavior shift before any internal realization.
- Use the **Great Wheel** and Bias Prism to determine *how* pressure is received.
- **Depth of Knowledge** (separate filter) determines what the character can even perceive about the event.

## YAML Structure (add to character cards)
```yaml
transformation_weights:
  active_focus: 70          # Current dominance of Active Focus Realm (0-100)
  latent_anchors:
    Realm_II: 15
    Realm_VIII: 15
  bias_strength: 60         # How strongly the current Bias distorts perception
  somatic_flexibility: 40   # How easily somatic tells can shift (higher = more fluid)
  transformation_history:   # Log of significant shifts
    - event: "First Gate exposure"
      chapter: 3
      delta:
        active_focus: +8
        latent_anchors:
          Realm_X: +12
      permanence: "medium"   # temporary | medium | permanent
      somatic_note: "fingers tremble longer after the event"
```

## Event Pressure Rules
When a significant event occurs:
1. **Classify pressure**:
   - Type: Emotional | Somatic | Cognitive | Social | Esoteric/Ritual
   - Strength: Low | Medium | High | Extreme
   - Alignment with current Focus/Bias (aligned = easier shift; opposed = resistance or backlash)

2. **Apply weighted delta**:
   - High pressure on aligned realm → +10–20 to weight
   - Opposed pressure → smaller shift or temporary backlash
   - Somatic_flexibility affects how quickly tells change

3. **Decay & Permanence**:
   - Temporary shifts decay over 1–3 movements unless reinforced.
   - Medium/Permanent shifts stay in YAML and affect future loads.

4. **Somatic Manifestation** (always on-page):
   - Never "I feel different now."
   - Instead: "His shoulders stayed tight long after the others had relaxed."

## Integration with Core
- Load this module **after** realm_index and on-scene cards.
- When generating a movement, check recent transformation_history for active deltas.
- Update YAML silently at end of approved movement if shift occurred.

## Commands / Usage
- Author can manually trigger: `/transform event: [description] strength: high`
- Or let the system propose shifts during design pass.

*This module makes arcs feel earned through accumulated story pressure rather than author fiat.*