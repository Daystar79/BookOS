# Claims contract — Midlayer runtime

Product claims are only as true as the **mechanism + verification** below.
Update this table when the runtime gains or loses enforcement.

| Claim | Mechanism | Verification |
|:---|:---|:---|
| Invisible middle layer (no matrix on page) | Draft kernel bans + `linter.py` system-leak rules | `python3 scripts/run.py lint Drafts/` exit ≠ 0 on critical leaks |
| Bookkeeping is not optional | `midlayer commit` owns ledger + logs + consolidated log | After approval, commit succeeds; `status` not BLOCKED |
| Integrity before draft | `midlayer status` / `gate` | Gate exit 0 required before prose (agents) |
| Minimal draft context | `midlayer pack` compiles kernel + on-scene only | Pack file under `Build/.context/` (gitignored Build/) |
| Transformation is deterministic | `logs_io.apply_pressure` strength→bias_delta; temp-effect decay on commit | Unit tests `tests/test_midlayer.py`; inspect `_log.yaml` revision history |
| Character state has a single source of truth | `Characters/[slug]_log.yaml` wins; cards = identity defaults | `rebuild-log` regenerates consolidated markdown from YAML |
| Long-form consistency | Externalized logs + ledger chain + packs | **Author/project proof:** finish a work under pack→draft→lint→commit; not auto-guaranteed by software alone |

## Not yet automated (honest gaps)

- Dialogue asymmetry and body-before-insight are **instructional** (kernel + Rules); not fully scored by CI.
- Epistemic memory recall is **instructional** unless a future checker lands.
- Novel-scale quality is **empirical** (finish a book under the pipe), not a green unit test.

## Agent rule

If a claim in README/Main is stronger than this table, **this table wins** until the mechanism is upgraded.
