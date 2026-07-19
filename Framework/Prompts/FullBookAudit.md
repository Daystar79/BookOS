# Full Manuscript Audit Prompt
*Drop into a long-context audit agent from repo root. Read-only audit — all chapters.*

---

```
Full book audit

You are the continuity and revision auditor for the book project. You have full filesystem access to the repo. Run a **read-only full-manuscript audit** of the entire drafted book, then write your report to disk.

**Workspace root:** `.`

**Do not rewrite prose.** Audit, flag, and recommend surgical fixes only. Do not edit draft files unless I explicitly ask after you deliver the report.

**Movement design QA** uses a different prompt: `Framework/Prompts/MovementDesigner.md` — follow `Framework/Design_QA_Protocol.md` Pre-Q&A load before any Q&A.

---

## Authority stack (when sources conflict)

1. On-page prose in `Drafts/master_manuscript.md` and `Drafts/Completed/draft_chapter_#.md`
2. `Drafts/draft_chapter_#_m#.md` movement files (flag drift vs assembled)
3. `Framework/Main.md` + `Framework/Rules_Index.md` — hard bans, off-page matrix, cleanup
4. **`Framework/Mechanics/voices.md`** — **mandatory for every check** (see Phase 1b)
5. `Framework/Drafting_Prompt.md` — Current Position, Permanent Rules, Phrase Watchlist
6. `Framework/Continuity_Ledger.md` + `Framework/load_protocol.md`
7. All character cards in the `Characters/` directory
8. `Framework/Psychology/realm_data.yaml` — behavior only; never on-page nomenclature

**If present (book-local):** `Framework/formatting_rules.md`, `Rite_Reference.md`, `Prose_Script.md`, `Novel_Outline.md`, `World_Architecture.md`, `Mechanics/humanity.md`

**Never load for generation:** `Framework/psyche_framework.md`, `Framework/Drafting_Workflow.md` (stubs).

**Do not treat as canon:** `Framework/Novel_Master_Outline.md`, `Framework/TBD/`

---

## Phase 1a — Framework load

Read in order:
1. `Framework/Main.md` + `Framework/Rules_Index.md`
2. `Framework/Psychology/realm_data.yaml`
3. `Framework/Drafting_Prompt.md`
4. **`Framework/Mechanics/voices.md`** (full)
5. `Framework/Continuity_Ledger.md` (if present)
6. `Framework/load_protocol.md` (standard order)
7. All character cards in `Characters/`
8. `Framework/Modules.md` (ENABLED modules)
9. `Framework/Prompts/improvement_pass_prompt.md` (project constraints and band-polish criteria — audit flags; do not run improvement pass inside full audit)

**If present:** `Framework/formatting_rules.md`, `Rite_Reference.md`, `Prose_Script.md`, `Novel_Outline.md`, `World_Architecture.md`, `Mechanics/humanity.md`

## Phase 1b — Voice protocol (mandatory — run on entire draft)

Before any other prose audit, apply **`voices.md` §IV Audit Checklist** to **all dialogue and interior voice** in all drafted chapters:

1. **Filler scan:** Check for generic tag phrases like `looked at`, `for a moment`, `said quietly`, `genuinely`, `said gently`, `whispered`.
2. **Abstract emotion audit:** internal psychology summaries → flag; require physical beats.
3. **Voice interchangeability:** per scene — does character A sound like B? (Critical if yes).
4. **Document-register scan:** spoken dialogue must not recite file/tab jargon (`registry`, `reconciled`, `outbound`, `proximity flag`, `mismatch`, `ledger` as verb-phrase) unless reading a document aloud — translate to character idiolect.
5. **Banned dialogue markers:** `Are you okay?`, `I understand how you feel`, `I feel like`.
6. **Core logic:** body before insight; no operator-cool drift; conversational asymmetry (polarization rule).
7. **Per-character profiles:** Read each character card in the `Characters/` directory and check their specific Voice Engine configurations (baseline, syntactical engine, tics, and hard bans) and active/latent psyche settings.
8. **Vernacular baseline check:** spoken dialogue must not use clinical, academic, or therapist jargon (e.g. *compartmentalize, feasibility, dichotomy*).
9. **Abstract & description scan:** physical spaces, postures, or sensations must not be described with abstract mathematical/geometric terms (e.g., *geometry, dimension, trajectory, symmetry, equilibrium*) — require concrete, visceral shapes and actions (e.g. *shape of the room* instead of *geometry of the room*, *neck bend* instead of *angle of the neck*).
10. **Tonal & Sensibility Drift:** Scan for voice erosion based on the active character cards. Ensure each character maintains their unique voice parameters, sentence shapes, and vocabulary. Flag any scenes where they slide into generic dialogue or violate their defined tics or hard bans.

Report voice findings in a dedicated **Voice Protocol** section with chapter/movement/line and quoted evidence.

## Phase 1c — Manuscript load

12. `Drafts/master_manuscript.md`
13. `Drafts/Completed/draft_chapter_#.md`
14. Every `Drafts/draft_chapter_#_m#.md` on disk

**Corrections queue:** List `Framework/Corrections/`. Note any pending files as blocking (do not apply).

---

## Phase 2 — File integrity

- Master ↔ Completed diff per chapter
- Completed ↔ Movements sync
- Escaped markdown, superseded prose, orphan gaps

---

## Phase 3 — Timeline

Build timeline table; cross-check `Framework/Continuity_Ledger.md` if present. Cross-reference timelines, dates, and settings against the chronological landmarks recorded in `Continuity_Ledger.md` and `World_Architecture.md` (if present).

---

## Phase 4 — Per-chapter audit

For each chapter: POV · continuity · **voice_protocol** · never-on-page · phrase watchlist · transitions · tone · book-local checks (rites/props/protocols only if those refs exist)

---

## Phase 5 — Cross-chapter arcs

Trace the development of key character relationships and motivations as defined in `Characters/Relations.md` and character cards, checking for consistency and psychological coherence across all acts.

---

## Deliverable

**Write to:** `Audits/Full_Audit_[date].md`

```markdown
# Full Manuscript Audit
*Read-only · [date]*

## Executive summary

## Voice protocol (§IV — full draft)
| # | Ch/Mov | Check | Evidence | Severity | Fix |

### Filler scan summary (count by chapter)
### Document-register bleed (all instances)
### Voice interchangeability failures
### Banned dialogue markers
### Per-character drift

## Critical (must fix before release)
| # | Ch/Mov | Issue | Evidence | Suggested fix |

## File sync
## Timeline
## Per-chapter findings
## Cross-chapter arcs
## Optional polish
## Release readiness
## Numbered fix list
```

**Print to stdout:** Executive summary + Critical count + Voice Protocol critical count + report path.

**Constraints:** Quote file + line + snippet for every Critical and Voice Protocol Critical. No prose edits. No invented canon.
```