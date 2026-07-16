# Character Card: [Full Name]
*Location: `Characters/[slug].md` — load with [Main.md](../Framework/Main.md) for drafting*

---

## Identity

| Field | Value |
|:---|:---|
| **Name** | [Full name / preferred call-name] |
| **Aliases** | [Optional] |
| **Age (canon)** | [Integer years] |
| **Physical (no ethnic labels)** | [Coloration, features, bone structure, movement — show, never category-label] |
| **Voice archetype base** | A / B / C / D / E / F (or custom hybrid) |

---

## Psyche Matrix

| Field | Value |
|:---|:---|
| **Active Focus** | Realm [N] — [Name] |
| **Latent Anchors** | Realm [a], [b], [c] |
| **Cognitive Bias** | [Bias name] — [one-line rewrite rule] |
| **Default Somatic Alignment** | [throat, breath, jaw, posture, hands…] |

---

## Transformation & Knowledge (NEW)

| Field | Value |
|:---|:---|
| **Transformation Weights** | See transformation_weights YAML below |
| **Depth of Knowledge** | See depth_of_knowledge YAML below |

---

## YAML Frontmatter (for fast LLM parsing — add at top of card)

```yaml
---
name: "[Full Name]"
call_name: "[preferred call-name or null]"
age: [Integer years]
canon_adult: true
physical: "[concise description]"
voice_archetype: "[A-F or hybrid]"
active_focus: "Realm [N] — [Name]"
latent_anchors: ["Realm [a]", "Realm [b]", "Realm [c]"]
cognitive_bias: "[Bias Name] — [one-line rewrite rule]"
default_somatic_alignment: "[body parts / tells]"

# NEW: Transformation
transformation_weights:
  active_focus: 70
  latent_anchors:
    Realm_II: 15
    Realm_VIII: 15
  bias_strength: 60
  somatic_flexibility: 40
  transformation_history: []

# NEW: Depth of Knowledge
depth_of_knowledge:
  general: "[broad understanding]"
  esoteric: "[ritual/occult knowledge level]"
  personal: "[memory clarity vs. blanks]"
---
```

## Voice Engine

- **Baseline:** [register summary]
- **Syntactical engine:** [sentence shape, vocabulary]
- **Hard bans:** [what this character never says]
- **Signature tics:** [optional repeated words/gestures]

---

## History Anchors (imperfect recall)

List only coarse, scene-useful facts. Memories stay vague unless triggered.

- [Anchor 1 — generalized]
- [Anchor 2]
- [Anchor 3]

---

## Relationships (optional)

| Other | Dynamic | Notes |
|:---|:---|:---|
| [Name] | [bond type] | [how Focus/Bias warps them] |

---

## Scene Seeds (optional)

- [Place + pressure + object]
- [Alternate seed]

---

## Load Protocol

When this character is on-scene for drafting ([Main.md](../Framework/Main.md)):

1. **Fast Load:** Read the YAML frontmatter first for structured data (name, age, focus, bias, transformation_weights, depth_of_knowledge).
2. Copy matrix, voice, somatic, and adult-gate fields into **silent** live state (do not print CONFIG).
3. Set **18+ Sexuality** to **OFF**. Enable only if brief/user requests **and** Canon Adult is **YES**.
4. Run Focus brace/release from [realm_index.md](../Framework/Psychology/realm_index.md).
5. Never name realms, biases, or "trauma" in character speech.
