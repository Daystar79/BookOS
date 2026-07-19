# Changelog

All notable changes to **CognitiveMiddleware / Midlayer** are recorded here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).  
Dates are **YYYY-MM-DD**. Newest entries first.

**Agents:** After any substantive change to this repository, append an entry under `[Unreleased]` (or a dated release section if shipping). See [AGENTS.md](./AGENTS.md).

**Related logs (not this file):**
- `Framework/source_changes.md` — detailed framework session / design-lock notes (never load for draft generation)
- `Framework/Character_Change_Log.md` — in-book character matrix snapshots (story runtime, not product history)

---

## [Unreleased]

### Changed

- **Init and character builder remove demo cast:** Sample characters (`reed`, `helen`, `cass`, `wren`, `nora`, `lior` + logs) are deleted and `Relations.md` / `Relationships.canvas` cleared by novel init post-cleanup **and** by character builder Pre-Step (if init was skipped). Scaffolds/templates kept. Documented in `Characters/README.md`; reset restores demos when Git is available.
- **Renamed project host from BookOS → Midlayer** (folder, docs, license, scripts, canvas paths, build helpers). Product remains Cognitive Middleware / Psyche Matrix; no longer branded as an “OS.”
- Deploy script examples use a generic sibling book folder (`MyNovel`) instead of the project name.

### Added

- Root `CHANGELOG.md` as the project product changelog.
- Root `AGENTS.md` with mandatory changelog maintenance and agent operating rules.
- Root `CLAUDE.md` thin entry pointing at `AGENTS.md` / `CHANGELOG.md`.

---

## [2026-07-18]

### Changed

- Removed all slash-style author/simulator command syntax from documentation.
- Author and simulator controls use plain language only (e.g. “enable adult mode”, “unlock style”, “draft the next movement”).
- Prompt invoke headers rewritten without slash prefixes (`Build character`, `Build world`, `Initialize novel`, etc.).
- Historical notes in `Framework/source_changes.md` rephrased so they no longer teach slash syntax.

### Files touched (summary)

- `README.md`, `Simulator/README.md`, `Simulator/CharacterRuntime.md`
- `Framework/Mechanics/prose.md`, `Framework/Mechanics/erotica.md`, `Framework/Drafting_Prompt.md`
- `Framework/Prompts/*`, `Framework/source_changes.md`

---

## [2026-07-17]

### Added

- Embodiment baseline → runtime filters pipeline in `Framework/Main.md` (body sets capacity; culture, occupation, Focus, belief, memory, Bias, and scene pressure filter output).
- Simulator one-switch plain-language **enable adult mode** (sets `adult_auth` + HEAT when canon adult).
- Bond setup via plain language for established relationships.

### Changed

- Renamed Sexuality module → **Erotica** (`Framework/Mechanics/erotica.md`); ambient desire remains Main middleware; erotica file is scene craft only.
- Execute-on-movement order: body baseline → filters → Focus/Bias → body-first prose → prism → modules → transform → bans → commit.

---

## [2026-07-13]

### Added

- `Simulator/` side tool for live card testing and private sessions (not the product surface).
- Hard bans against debug dumps, matrix footers, and bracketed somatics in draft/sample prose.

### Changed

- Main entry path: honest load protocol; drafting-only execute loop; stubs point at Main.
- Removed `Web/` mirrored copies; simulator holds optional chat runtime.

---

## [2026-07-12]

### Added

- Wound activity & dormancy (Bias ACTIVE vs DORMANT).
- Dynamic Focus shifting and Focus Lock state machine.
- Somatic-cognitive sequence (body before insight) and somatic pacing/decay rules.
- Dynamic canon character synthesis for playground/card demos.

### Changed

- Humanity / prose protocols reorganized; prose style auto-lock after first response.
- Token-oriented psychology loading (realm index / dense data path).

---

## [2026-07-09]

### Added

- Prose style selector and lock-on-select (`llm` default; optional `natural` and catalog styles).
- Character-first load model and Canon Adult 18+ gate for intimacy protocols.
- Optional sexuality/erotica protocol (gated; default off).
- Imperfect recall, deflection, and cognitive misconstrual (biased hearing) rules.
- Single-prompt playground drop-in for chat demos.

### Changed

- Mechanics renamed to short names: `humanity.md`, `voices.md`, `prose.md`, sexuality/erotica path.
- Voice profiles generalized to archetypes A–F (demo novel names removed from protocol).

---

## Notes

- Patch-level or typo-only edits may be folded into the current `[Unreleased]` bullet rather than a new dated section.
- Prefer user-visible / structural / API / protocol changes over every internal whitespace tweak.
- When both apply: update **this file** for product/repo history; use `Framework/source_changes.md` for design locks and session detail that drafting must not load.
