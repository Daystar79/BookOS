# Sexuality Protocol (Optional — 18+ Only)
*Location: `Framework/Mechanics/sexuality.md` · Commercial heat + somatic integrity.*

> [!IMPORTANT]
> This protocol is strictly optional and restricted to **canonically adult (18+)** characters only. It requires explicit user enablement via the `/18+ on` command or scene brief. Both conditions must be met.

---

## 1. Eligibility Gate

1. **Verify Cards:** Load character cards for everyone in the scene.
2. **Age Check:** Each character must have `Canon Adult (18+): YES` and an age of 18 or older.
3. **Strict Ban on AU/Age-Up:** If any character is under 18 or status is missing, **do not load this protocol**. No explicit content is allowed.
4. **Default Status:** Protocol remains **OFF** until explicitly activated.
5. **No Default Eroticization:** Enabling the protocol does not force or default characters into an intimate or sexual posture. Physical intimacy must be earned naturally through the scene's emotional context and narrative progression. If the scene does not involve romantic development, physical intimacy, or touch, the character must react with standard, non-erotic behavior.
6. **Strict Boundary Gating (Decision Tree):** If a character's internal psychological state (defined by active Focus, Bias, trust, and matrix evolution from the character log) does not support intimacy, the decision tree is locked, and adult situations **do not happen** (even if the user attempts to force or initiate them). The character must stand by their boundaries and react with boundary-defense behaviors (e.g., somatic muscle lock, stepping back, deflection, or direct verbal boundary setting) in accordance with their card.
7. **Simulation Termination (Scene Exit):** If the interaction reaches a point of irreconcilable conflict, boundary violation, safety threat, or persistent pressure where the character would not logically continue the scenario, they are allowed to physically leave the scene. The character must execute an in-character departure, followed immediately by the system termination marker: `[Simulation Terminated: Character Exited Scene]`. The engine must refuse further interaction once this marker is output.

---

## 2. Integration with Transformation Engine & Psyche Matrix

Intimacy is a high-cost biological and emotional event. It is deeply governed by the character's active Focus, Bias, and matrix evolution (card defaults + `_log.yaml` snapshot).

### Focus-Warped Intimacy
- **Realm III (Identity) / IV (Will) Focus:** Creates high somatic guards, rigid posture, or need for control/performance.
- **Realm IX (Threshold) Focus:** Somatics show as trembling fingers, shallow rapid breathing, and hesitation before physical touch.
- **Dormant vs Active Bias:** In intimate scenes, a character's wounds are highly prone to activation. If emotional pressure spikes, their Bias shifts to `ACTIVE`, and touch or affection is instantly misconstrued (e.g., peace is perceived as debt due).

### Transformation Engine Calculations
- Intimate encounters act as **Extreme Emotional/Somatic pressure events**.
- If the scene lands a milestone connection, apply a permanent delta (+10 to +20) to `latent_weights` or shift `active_focus` in `Characters/[slug]_log.yaml` (and sync Character_Change_Log) — not on the character card.
- Somatic changes (e.g. release tells, dropping role partitions) must be recorded in the log snapshot + history entry at Post-Movement Commit.

---

## 3. Laws of Kinetic Heat

Intimate descriptions must follow biological reality, not idealized tropes.

- **Thermal Pacing:** Describe skin temperature, sweat, flushed skin, goosebumps, and cold drafts on bare skin.
- **Kinetic Mass:** Emphasize physical weight, resistance, muscle contraction, friction, and the force of grip.
- **Last Barrier Rule:** Keep clothing barriers active and awkward as long as possible (tugging at stiff boots, catching zippers, fabric sliding) before full exposure.
- **Output Hygiene:** Never use abstract romance cliches or euphemisms. Use precise, concrete somatic language. Never name Realms, biases, or trauma labels on-page.

---

## 4. Interruption & Somatic Glitches

Under pressure, intimacy can trigger cognitive defense mechanisms.

- **Tripwire Activation:** If a character's core Bias is triggered, they experience an immediate somatic freeze, muscle lock, or sudden withdrawal.
- **No Monologues:** Show the physical retreat and body tension. Do not allow characters to immediately explain or analyze the glitch out loud. Leave the scene physically broken.
