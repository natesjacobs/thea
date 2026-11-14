# Assumptions: Theia impact (−4.50 Gyr)

Chosen values for this moment. Status words are defined in `../AGENTS.md`.

| ID | Assumption | Value chosen | Range considered | Why this one | Status | Depends on |
|---|---|---|---|---|---|---|
| A-001 | Impact time | 4.50 Ga | 4.51–4.35 Ga | Recent work favors an old Moon (Nimmo, Kleine & Morbidelli 2024) | canon | context.md, ../timeline.csv |
| A-002 | Theia mass | 0.13 Earth masses | 0.10–0.15 | Canonical range, mid-point | provisional | context.md, timeline.csv, last-years-approach-1.md, approach_run.py, kl_calibration.py |
| A-003 | Contact geometry | 45°, 9.5 km/s | 30–50°; 9–10 km/s | Canonical setup (Canup & Asphaug 2001), near escape speed | provisional | context.md, timeline.csv, last-years-approach-1.md, approach_run.py, kl_calibration.py |
| A-004 | Proto-Earth spin | A few to ~10 hr, axis tilted off Theia's approach | 2.5–10 hr | Spin partly cancels the impact's angular momentum, so no evection drain is needed | provisional | context.md, k-l-calibration.md |
| A-005 | Impact angle convention | b = sin θ, θ from the surface normal | — | Canup 2008 | canon | kl_calibration.py |
| A-006 | Critical hit-and-run speed | Midpoints of published 1:10 and 1:2 anchors, linear in mass ratio and angle | Valid 30–45° | Genda, Kokubo & Ida 2012; full fit not retrieved | provisional | kl_calibration.py |
| A-007 | Theia's origin | Inner Solar System, near 1 AU | Inner vs. outer | Hopp et al. 2025 isotope data | canon | context.md |
| A-008 | Co-orbital origin (L4 or L5) | No value; idea only | — | Belbruno & Gott 2005 | speculative | context.md |
| A-009 | Proto-Earth mass and radius | 0.88 Earth masses, 6,150 km | — | Leaves ~1.01 Earth masses after merger | provisional | context.md, last-years-approach-1.md, approach_run.py, kl_calibration.py |
| A-010 | Theia radius | 3,500 km | About Mars | Fits A-002 at Mars-like density | provisional | context.md, approach_run.py, kl_calibration.py |
