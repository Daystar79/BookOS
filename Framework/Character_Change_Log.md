# Character Change Log
*Matrix evolution ledger — companion to Continuity_Ledger. Separate from character cards.*

**Cards** (`Characters/[slug].md`) stay identity/load sheets: voice, cultural bias, bias *name*, history anchors, build defaults.  
**This file** tracks how the matrix moves over the book: current runtime snapshot + append-only movement deltas.

Do not write `transformation_history` (or movement-by-movement deltas) onto character cards.

---

## Post-Movement Commit (with Continuity_Ledger)

On **every approved movement**, write **both** ledgers:

| Save | File | Owns |
|:---|:---|:---|
| **Story ledger** | `Framework/Continuity_Ledger.md` | Day/time, draft path, **scene** somatic close, plot/continuity beats |
| **Character change log** | This file | Durable Focus/weight/somatic/bias-strength evolution + history of pressure events |

- Continuity_Ledger without this log = incomplete matrix continuity.
- This log without Continuity_Ledger = incomplete scene continuity.
- Character cards are **not** the change log. Optional rare card rewrite only if the author permanently retires an identity field (e.g. renamed bias, rebuilt voice) — not routine post-movement work.
- Temporary tells that will decay: Continuity_Ledger close only. Do not invent permanent rows here.
- Medium / High / Extreme pressure or any permanent shift: **must** update Current Snapshot + append a Movement History row. Missing rows after such pressure = failed commit.

### Load order (next design/draft)
1. On-scene character cards (identity, voice, bias name, build defaults)
2. **Current Matrix Snapshot** below (overrides card Focus / weights / baseline somatic / bias_strength when present)
3. Continuity_Ledger latest row (scene time, props, close body state)

---

## Current Matrix Snapshot
*Overwrite cells when a durable change commits. `As of` = last movement that wrote this character.*

| Character | Active Focus | Latent weights | Bias strength | Default somatic | Flexibility | As of |
| :--- | :--- | :--- | :---: | :--- | :---: | :---: |
| Reed | VIII — Integration | I 10 · II 15 · VII 10 | 75 | Throat tight; shoulders high; jaw lock | 30 | build |
| Helen | VI — Compassion | II 10 · IV 10 · VIII 15 | 70 | Soft chest; open hands | 45 | build |
| Cass | IV — Will | I 10 · II 15 · V 10 · VIII 10 | 70 | Still posture; folded hands | 25 | build |
| Wren | VII — Presence | I 10 · II 10 · VI 15 | 65 | Stillness; loose jaw | 40 | build |
| Nora | VI — Compassion | I 15 · II 10 · VII 10 | 70 | Warm touch; face-scan | 35 | build |
| Lior | IX — Threshold | I 10 · II 10 · III 15 | 70 | Lilt; tremor; shallow breath | 50 | build |

*When adding a novel cast: replace demo rows with book characters. Keep one row per active character.*

---

## Movement History
*Append a section per approved movement. One table row per on-scene character who had pressure or durable change; or a single “No durable matrix change” note.*

### Template (copy per movement)

```markdown
### [Ch] M[#] — [optional title]
| Character | Pressure | Delta | Permanence | Notes |
| :--- | :--- | :--- | :--- | :--- |
| [Name] | Emotional/High | bias_strength +10; default somatic → jaw lock baseline | permanent | [optional] |
| [Name] | — | none | temporary | Close state only → Continuity_Ledger |
```

### Entries

*(none yet — first approved movement appends here)*
