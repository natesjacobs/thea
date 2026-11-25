# Assumptions: Theia impact (−4.50 Gyr)

Chosen values for this moment. Column definitions and status words are in `../AGENTS.md`.

| ID | Assumption | Value chosen | Range considered | Why this one | Narrative | Consensus | Depends on | Used in |
|---|---|---|---|---|---|---|---|---|
| A-001 | Impact time | 4.50 Ga | 4.51–4.35 Ga | Recent work favors an old Moon (Nimmo, Kleine & Morbidelli 2024) | locked | contested | — | context.md, ../timeline.csv |
| A-002 | Theia mass | 0.13 Earth masses | 0.10–0.15 | Canonical range, mid-point | working | moderate | — | context.md, timeline.csv, last-years-approach-1.md, approach_run.py, kl_calibration.py |
| A-003 | Contact geometry | 45°, 9.5 km/s | 30–50°; 9–10 km/s | Canonical setup (Canup & Asphaug 2001), near escape speed (9.13 km/s from A-002, A-009, A-010). The chosen value in the A-003 / A-011 / A-012 chain; the other two follow from it | working | moderate | A-002, A-009, A-010 | context.md, timeline.csv, last-years-approach-1.md, approach_run.py, kl_calibration.py |
| A-004 | Proto-Earth spin | A few to ~10 hr, axis tilted off Theia's approach | 2.5–10 hr | Spin partly cancels the impact's angular momentum, so no evection drain is needed | working | contested | A-003, A-012 | context.md, k-l-calibration.md |
| A-005 | Impact angle convention | b = sin θ, θ from the surface normal | — | Canup 2008 | locked | convention | — | kl_calibration.py |
| A-006 | Critical hit-and-run speed | Midpoints of published 1:10 and 1:2 anchors, linear in mass ratio and angle | Valid 30–45° | Genda, Kokubo & Ida 2012; full fit not retrieved | working | moderate | A-002, A-005, A-009 | kl_calibration.py |
| A-007 | Theia's origin | Inner Solar System, near 1 AU | Inner vs. outer | Hopp et al. 2025 isotope data | locked | moderate | — | context.md |
| A-008 | Co-orbital origin (L4 or L5) | No value; idea only. Alternative to A-012 | — | Belbruno & Gott 2005 | idea | speculative | A-007 | context.md |
| A-009 | Proto-Earth mass and radius | 0.88 Earth masses, 6,150 km | — | Leaves ~1.01 Earth masses after merger | working | moderate | A-002 | context.md, last-years-approach-1.md, approach_run.py, kl_calibration.py |
| A-010 | Theia radius | 3,500 km | About Mars | Fits A-002 at Mars-like density | working | moderate | A-002 | context.md, approach_run.py, kl_calibration.py |
| A-011 | Approach speed far out (v∞) | 2.6 km/s | ~0.5 (low-e, non-crossing) to ~3 | √(9.5² − 9.13²): contact speed minus escape speed in quadrature | working | modeled | A-003, A-002, A-009, A-010 | last-years-approach-1.md, approach_run.py |
| A-012 | Orbits in the final decades | Crossing. Earth a 0.999 AU, e 0.011; Theia a 1.013 AU, e 0.077 | Crossing (e ≥ ~0.08); low-e Hill-unstable, ~2–3.5 mutual Hill radii apart, non-crossing; co-orbital (A-008) | A-011 forces Theia's e ≥ ~0.08, far above the 0.014 AU gap, so the orbits cross. Eccentric crossing orbits are the standard late-stage outcome | working | moderate (values modeled) | A-011, A-007 | last-years-approach-1.md, approach_run.py |
| A-013 | Mutual orbital inclination | 0° (planar run) | 0 to a few degrees | Simplification. Tilt makes deep encounters rarer and lengthens A-015 | open | unconstrained | — | last-years-approach-1.md, approach_run.py |
| A-014 | Conjunction interval (synodic period) | ~48 yr | Years (low-e case) to ~100 yr | Set only by the two semi-major axes and the Sun's mass (Kepler III): 364.7 and 372.4 day years from A-012. Eccentricity, speed and planet masses don't enter. Stable between deep encounters; one deep encounter can change it by a factor of ~2 or more | working | modeled | A-012 | — |
| A-015 | Deterministic horizon: collision certain | ~50–150 yr before impact; centuries if earlier passes were distant | Years–decades (low-e case) to centuries | Set by the last deep encounter (within ~10⁶ km), which amplifies errors ~10³. Analogy: Bennu, deterministic to its 2135 scattering approach (Chesley et al. 2014) | open | modeled | A-012, A-013, A-014, A-016 | — |
| A-016 | Untracked planetesimals and angle lock | Angle to ±1° known ~8 yr out if bodies >~30 km are tracked; ~2–3 months if a 100-km body could still hit | ~10 km to ~100 km largest untracked body | A 100-km hit shifts Theia's arrival ~100,000 km over ~50 yr. ±1° of angle is ~430 km on the target plane | open | unconstrained | A-002, A-003, A-011, A-014 | — |
