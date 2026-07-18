# Modules Index — CognitiveMiddleware (BookOS)
*Canonical index of optional active modules. Load with [Main.md](./Main.md).*

---

## 1. Core Supremacy Rule
No module is allowed to override, supersede, or conflict with the core rules defined in **`Rules_Index.md`** or the cognitive logic in **`Main.md`**. If a conflict exists, the core framework rules take absolute precedence, and the conflicting module rule is silently ignored.

---

## 2. Active Modules Registry

Module files are loaded according to status. Registry entries below indicate location and enabled status. Only files that exist are kept in this active registry.

| Module Name | Path | Status | Compatibility Constraints |
|:---|:---|:---|:---|
| **Erotica Protocol** | `Framework/Mechanics/erotica.md` | `DISABLED` | Requires Canon Adult: YES on cards |

To enable a module: document compatibility in the file, set **Status** to `ENABLED` in this table, then re-run verification on the next session load.

---

## 3. Module Verification Rules (For AI Agents)
Before applying any module instructions:
1. Scan the registry above for modules marked as `ENABLED`.
2. If none are `ENABLED`, skip the rest of this protocol (no module files to load).
3. For each ENABLED module: locate and read the module file at the specified path. If the file is missing, treat as **unverified** and skip with a short stdout warning.
4. Perform the **Compatibility Check**:
   - Verify that the module's instructions do not contradict any hard bans or output hygiene rules in `Rules_Index.md` (e.g. no engine labels on page, silent execution).
   - Verify that the module is not listed as incompatible with other currently enabled modules.
   - If verification fails, print to stdout: `[Warning] Module [Name] failed verification: incompatible with [System/Module]. Skipping.`
5. Apply verified module instructions as subordinate parameters only.

## 4. Module Loading and Order
- Modules load in registry order.
- Each module reserves only its declared capabilities and constraints.
- A later module is blocked only by an explicit incompatibility or missing dependency.
- Multiple non-conflicting modules may load simultaneously.

---

## Planned Modules
The following modules are planned but not yet shipped:
- **Mystery Engine** (`Modules/mystery.md`) - status: `DISABLED` (not shipped)
- **Romance Tuning** (`Modules/romance.md`) - status: `DISABLED` (not shipped) - Incompatible with Action pacing
- **Action & Pacing** (`Modules/action.md`) - status: `DISABLED` (not shipped) - Incompatible with Romance Tuning