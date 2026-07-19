# Sample movement (ships with Midlayer)

Worked example of the full drafting loop using the **demo cast** (Reed + Helen).

| Step | Artifact |
|:---|:---|
| Prose | [`draft_chapter_1_m1.md`](./draft_chapter_1_m1.md) |
| Story ledger | `Framework/Continuity_Ledger.md` (1 M1 row) |
| Matrix ledger | `Framework/Character_Change_Log.md` (Snapshot + History) |

**Not novel canon.** Strip or replace when you start a real book. Demo cards in `Characters/` are optional tests only.

How to produce the next sample (agent pattern):
1. `python3 scripts/run.py midlayer status` (must not be BLOCKED)
2. `python3 scripts/run.py midlayer pack --slugs reed,helen --brief "…"`
3. Draft one movement, prose only; `python3 scripts/run.py lint Drafts/samples/`
4. On approval: `python3 scripts/run.py midlayer commit --movement "1 M1" --draft Drafts/samples/… --slugs reed,helen --day "…" --somatic "…" --beats "…"`

Note: shipped demo logs may still show sample history while Continuity_Ledger is honest-empty until you commit (status WARN, not BLOCK).
