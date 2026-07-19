# Agent instructions — CognitiveMiddleware / Midlayer

This file is the **standing contract for AI agents** (and humans using agent tools) working in this repository. Read it at session start when making code, docs, framework, or tooling changes. Thin entry points (`CLAUDE.md`, and any future tool-specific stubs) should point here.

Drafting fiction uses a different load stack — see `Framework/Main.md` and `Framework/load_protocol.md`. **Do not** load this file or `CHANGELOG.md` into a pure draft-generation context.

---

## Mandatory: update the changelog on every change

**Whenever you change anything substantive in this repo, update [`CHANGELOG.md`](./CHANGELOG.md) in the same session.**

| Do | Do not |
|:---|:---|
| Append under `## [Unreleased]` (or a dated `## [YYYY-MM-DD]` if the user is shipping a cut) | Skip the changelog because the change “is small” (unless pure typo / whitespace with no behavior or doc contract change) |
| Use Keep a Changelog groups: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security** | Dump raw git diffs into the changelog |
| Write plain-language bullets (what/why a reader or maintainer cares) | Use slash-command syntax anywhere in docs or changelog |
| Prefer newest-first ordering | Rewrite unrelated historical entries without cause |
| Mention important paths when useful (`Framework/Main.md`, `scripts/…`) | Load `CHANGELOG.md` or `Framework/source_changes.md` as runtime drafting context |

### When a changelog entry is required

Update `CHANGELOG.md` if the session includes any of:

- Framework / protocol / rules / mechanics changes
- Scripts, linter, deploy, build tooling
- README, agent docs, simulator runtime, modules registry
- Public templates, schemas, prompts under `Framework/Prompts/`
- Breaking renames, removals, or policy shifts (e.g. plain-language controls)

### When a changelog entry is optional

- Pure typo or formatting in a single file with no contract change
- Story-only work: draft prose, character cards for *this* book, Continuity_Ledger rows, movement commits (those use story ledgers, not product changelog)

If unsure, **add a short `[Unreleased]` bullet**.

### Same-session companion logs

| File | Purpose | Agent duty |
|:---|:---|:---|
| **`CHANGELOG.md`** (repo root) | Product / repo history | **Always** for product/framework/tooling/docs changes |
| **`Framework/source_changes.md`** | Framework design locks, session application notes | Update when applying framework design locks or Corrections queue; **never load for generation** |
| **`Framework/Character_Change_Log.md`** | In-book matrix snapshots | Post-movement commit only (story runtime) |

Corrections queue (`Framework/Corrections/`): apply → log in `source_changes.md` → if product-facing, also note in `CHANGELOG.md` → delete correction file → rebuild releases if required (`formatting_rules.md` §8).

---

## Product surface

- **Product:** invisible cognitive middle layer for long-form fiction (`Framework/`, character cards, logs, ledgers, linter).
- **Not the product surface:** `Simulator/` (optional card test / private RP). Keep docs honest about that split.
- **Author controls:** plain language only. No slash-command UI in any documentation or prompts.

---

## Scripts (Windows & Unix)

Prefer the OS-aware launcher:

```bash
python3 scripts/run.py deploy|lint|migrate|midlayer …
```

| Host | Prefer | Alternate |
|:---|:---|:---|
| Linux, macOS, BSD, WSL | `python3 scripts/run.py …` | `scripts/unix/<tool>.sh …` |
| Windows | `python scripts/run.py …` | `scripts/windows/<tool>.ps1` or `.cmd` |

Do not run `.sh` on native Windows or `.ps1` on Unix unless a compatible shell is confirmed. Details: [`scripts/README.md`](./scripts/README.md).

### Midlayer runtime (draft bookkeeping — mandatory for agents)

| Command | When |
|:---|:---|
| `python3 scripts/run.py midlayer status` / `gate` | Before design or draft; **do not draft if BLOCKED** |
| `python3 scripts/run.py midlayer pack --slugs …` | Before drafting a movement (preferred context load) |
| `python3 scripts/run.py midlayer commit …` | On **approved** movement — not freehand ledger/YAML edits |
| `python3 scripts/run.py lint Drafts/` | After draft; critical system leaks fail the linter |

Claims vs enforcement: [`Framework/midlayer/CLAIMS.md`](./Framework/midlayer/CLAIMS.md).

---

## Drafting vs maintenance

| Mode | Load | Do not load |
|:---|:---|:---|
| **Draft / design / cleanup prose** | Per `Framework/Main.md` + `load_protocol.md` | `CHANGELOG.md`, `AGENTS.md`, `source_changes.md`, `formatting_rules.md`, `Framework/Prompts/*`, stubs |
| **Repo maintenance / framework edit** | This file + relevant paths | Do not invent product history — write it to `CHANGELOG.md` |

---

## Output hygiene (always)

- Matrix 100% off-page in manuscript prose (no realm numbers, bias labels, prism jargon on the page).
- Body before insight; imperfect memory; no therapy-speak defaults.
- Age / Canon Adult gates absolute for intimacy paths.
- After approved movements: `python3 scripts/run.py midlayer commit …` (not ad-hoc file edits).

---

## Checklist before ending a maintenance session

1. [ ] Changes match the request and existing project style.
2. [ ] **`CHANGELOG.md` updated** under `[Unreleased]` or a dated section.
3. [ ] `Framework/source_changes.md` updated if design locks / framework session notes apply.
4. [ ] No slash-command syntax introduced in docs.
5. [ ] Scripts still correct for both Windows and Unix if tooling changed.
6. [ ] Did not load changelog/agent files into a drafting prompt stack.

---

*Install once. Change the product → log it in `CHANGELOG.md`. Draft the book → load Main, not the changelog.*
