# Modules Index — BookOS
*Canonical index of optional active modules. Load with [Main.md](./Main.md).*

---

## 1. Core Supremacy Rule
No module is allowed to override, supersede, or conflict with the core rules defined in **`Rules_Index.md`** or the cognitive logic in **`Main.md`**. If a conflict exists, the core framework rules take absolute precedence, and the conflicting module rule is silently ignored.

---

## 2. Active Modules Registry

| Module Name | Path | Status | Compatibility Constraints |
|:---|:---|:---|:---|
| **Mystery Engine** | `Modules/mystery.md` | `DISABLED` | None |
| **Romance Tuning** | `Modules/romance.md` | `DISABLED` | Incompatible with Action pacing |
| **Action & Pacing** | `Modules/action.md` | `DISABLED` | Incompatible with Romance Tuning |
| **Sexuality Protocol** | `Modules/sexuality.md` | `DISABLED` | Requires Canon Adult: YES on cards |

---

## 3. Module Verification Rules (For AI Agents)
Before applying any module instructions:
1. Scan the registry above for modules marked as `ENABLED`.
2. Locate and read the module file at the specified path.
3. Perform the **Compatibility Check**:
   - Verify that the module's instructions do not contradict any hard bans or output hygiene rules in `Rules_Index.md` (e.g. no engine labels on page, silent execution).
   - Verify that the module is not listed as incompatible with other currently enabled modules.
   - If verification fails, print to stdout: `[Warning] Module [Name] failed verification: incompatible with [System/Module]. Skipping.`
4. Apply verified module instructions as subordinate parameters.
