# Modules Index — BookOS
*Canonical index of optional active modules. Load with [Main.md](./Main.md).*

---

## 1. Core Supremacy Rule
No module is allowed to override, supersede, or conflict with the core rules defined in **`Rules_Index.md`** or the cognitive logic in **`Main.md`**. If a conflict exists, the core framework rules take absolute precedence, and the conflicting module rule is silently ignored.

---

## 2. Active Modules Registry

Module files are loaded according to status. Registry entries below indicate location and enabled status.

| Module Name | Path | Status | Compatibility Constraints |
|:---|:---|:---|:---|
| **Mystery Engine** | `Modules/mystery.yaml` | `DISABLED` (not shipped) | None |
| **Romance Tuning** | `Modules/romance.yaml` | `DISABLED` (not shipped) | Incompatible with Action pacing |
| **Action & Pacing** | `Modules/action.yaml` | `DISABLED` (not shipped) | Incompatible with Romance Tuning |
| **Sexuality Protocol** | `Modules/sexuality.yaml` | `ENABLED` | Requires Canon Adult: YES on cards |

To enable a module later: add the YAML file under `Modules/`, document compatibility in that file, set **Status** to `ENABLED` in this table, then re-run verification on the next session load.

---

## 3. Module Verification & Kernel-Style Loading Protocol

Agents must enforce a strict, Linux-kernel-style module loading and dependency system to prevent runtime state corruption.

### Rules of Loading & Conflict Resolution:
1. **Precedence (First-Staged Lock):** Modules are resolved in top-to-bottom order of their entry in the Active Modules Registry table above. The first module marked `ENABLED` is loaded into active memory and holds a session lock.
2. **Strict Lockout on Conflicts:** If a subsequently scanned module has a compatibility constraint or conflict with an already-loaded module:
   - The second module **cannot be loaded**. Its status is treated as `BLOCKED (conflict lock)`.
   - The agent must fail the load and print: `[Error] Module load failed: [Second Module] conflicts with already-loaded [First Module]. You must unload (set to DISABLED) [First Module] before loading [Second Module].`
3. **No Hot-Swapping Collision:** A conflicting module cannot overwrite or hot-swap into a running session. The active module must be explicitly set to `DISABLED` by the author first to clear the session lock.
4. **Dependency Resolution:** If a module requires another module as a prerequisite, the prerequisite module must be marked `ENABLED` and resolved first, or the dependent module will fail to load with: `[Error] Module load failed: [Module B] requires missing dependency [Module A].`
5. **Output Hygiene & Subordination:** Once a module is verified and loaded without conflict, its instructions apply as subordinate parameters only. It must never contradict the core rules in `Rules_Index.md` (e.g. no engine labels on page, silent execution).