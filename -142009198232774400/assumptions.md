# Assumptions: Theia impact (−4.50 Gyr)

The one place where this moment's fixed values are chosen. Stories and notes cite IDs here, not restated numbers. Change a value here and update its dependents.

## Status

- **canon**: fixed for all stories.
- **provisional**: a value is chosen with low or medium confidence. Stories may use it but should flag it.
- **open**: needs checking before any story relies on it.
- **speculative**: an idea with no committed value. Not used in canon. Gets a value and becomes `provisional` when someone picks one.

## Register

| ID | Assumption | Value chosen | Range considered | Why this one | Status | Depends on |
|---|---|---|---|---|---|---|
| A-001 | Impact time | 4.50 Ga | 4.51–4.35 Ga | Recent work favors an old Moon (Nimmo, Kleine & Morbidelli 2024) | canon | context.md, timeline.csv |
| A-002 | Theia mass | 0.13 Earth masses | 0.10–0.15 | Canonical range, mid-point | provisional | context.md, k-l-calibration.md |
| A-003 | Impact geometry | 45°, 9.17 km/s | 30–45°; ~9–10 km/s | Canonical Canup & Asphaug (2001) setup | provisional | context.md, last-years-approach-1.md, k-l-calibration.md |
| A-004 | Proto-Earth spin | A few to ~10 hr, axis tilted off Theia's approach | 2.5–10 hr | Anchor choice. Lets spin partly cancel the orbital angular momentum, without needing evection | provisional | context.md, timeline.csv, k-l-calibration.md |
| A-005 | Angle convention in the calibration | b = sin θ, θ measured from the surface normal | Convention not checked | Assumed in the calibration script | open | k-l-calibration.md, kl_calibration.py |
| A-006 | Critical hit-and-run speed | Midpoints of published 1:10 and 1:2 anchors, linear in mass ratio and angle | 30–45° only | Full fit coefficients not retrieved | provisional | k-l-calibration.md, kl_calibration.py |
| A-007 | Theia's origin | Inner Solar System, near 1 AU | Inner vs. outer origin | Hopp et al. (2025) isotope data | canon | context.md |
| A-008 | Co-orbital origin (L4 or L5) | none | — | Belbruno & Gott (2005) | speculative | context.md |
| A-009 | Proto-Earth mass and radius | 0.88 Earth masses, 6,150 km | — | Anchor values used in the calibration | provisional | context.md, k-l-calibration.md, kl_calibration.py |
| A-010 | Theia radius | 3,500 km | ~Mars-sized | Matches A-002 with Mars-like density | provisional | context.md, k-l-calibration.md, kl_calibration.py |

## Notes

- A-005 is `open`. The calibration reads the angle as sin θ. If the source papers measure it the other way, every angle-dependent value in `k-l-calibration.md` changes.
- A-006 and the calibration numbers in `k-l-calibration.md` use the same method. Revisit both together.
- Speculative items stay out of the register's values until they have a number.
