# Character Change Log
*Matrix evolution ledger — companion to Continuity_Ledger. Separate from character cards.*

**Cards** (`Characters/[slug].md`) stay identity/load sheets: voice, cultural bias, bias *name*, history anchors, build defaults.  
**This file** tracks how the matrix moves over the book: current runtime snapshot + append-only movement deltas.

Do not write `transformation_history` (or movement-by-movement deltas) onto character cards.

**Session boot:** Main.md **Ledger Integrity Pass** runs first. Honest empty History is valid; empty Snapshot is not (seed from cards). Placeholder Continuity rows must not leave History “pending.”

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
0. **Ledger Integrity Pass** (Main.md) — clean empty/placeholder ledgers first
1. On-scene character cards (identity, voice, bias name, build defaults)
2. **Current Matrix Snapshot** below (overrides card Focus / weights / baseline somatic / bias_strength when present)
3. Continuity_Ledger latest **real** row (scene time, props, close body state)

### Integrity notes for this file
| Condition | Handle |
|:---|:---|
| Snapshot empty | Seed from active cards (`As of: build`) |
| History empty, no Continuity rows | OK — do not invent entries |
| Continuity has committed rows, History missing those movements | Backfill or block draft |
| Demo Snapshot on a non-demo book | Replace with novel cast |

---

## Current Matrix Snapshot
*Overwrite cells when a durable change commits. `As of` = last movement that wrote this character.*

| Character | Active Focus | Latent weights | Bias strength | Default somatic | Flexibility | As of |
| :--- | :--- | :--- | :---: | :--- | :---: | :---: |
| Reed | VIII — Integration | I 10 · II 15 · VII 10 | 80 | Throat tight; shoulders high; jaw lock; scar-rub under debt pressure | 30 | sample 1 M1 |
| Helen | VI — Compassion | II 10 · IV 10 · VIII 10 | 80 | Soft chest; open hands; proximity lean; hand withdraws when blocked | 50 | sample 1 M1 |
| Cass | IV — Will | I 10 · II 15 · V 10 · VIII 10 | 70 | Still posture; folded hands | 25 | build |
| Wren | VII — Presence | I 10 · II 10 · VI 15 | 65 | Stillness; loose jaw | 40 | build |
| Nora | VI — Compassion | I 15 · II 10 · VII 10 | 70 | Warm touch; face-scan | 35 | build |
| Lior | IX — Threshold | I 10 · II 10 · III 15 | 70 | Lilt; tremor; shallow breath | 50 | build |

*Demo cast Snapshot. Replace with novel cast when starting a real book. Keep one row per active character.*

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

### 1 M1 — Cold Tea *(sample — demo cast)*
| Character | Pressure | Delta | Permanence | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Reed | Emotional/Social · Medium | bias_strength 75→80; default somatic + scar-rub under debt pressure; kindness received as bill due | medium | Offered hinge “no charge” to square; did not put weight down |
| Helen | Emotional/Social · Medium | Snapshot note: hand-withdraw when care blocked; bias still care-as-assignment (Saturday food) | temporary→carry intent | No weight shift; Saturday return open loop |
