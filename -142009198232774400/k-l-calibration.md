# K and L calibration

Working note for the Theia anchor. Analytic, not an SPH run. Reproduce with `python3 -I kl_calibration.py`.

## Definitions

**K**, the escape ratio: (impact speed ÷ two-body escape speed) ÷ (critical hit-and-run speed ÷ escape speed). K < 1 merges. K ≥ 1 is hit-and-run, and the impactor leaves.

**L**, the spin budget: orbital angular momentum of the impact ÷ Earth-Moon system angular momentum (3.5 × 10⁴¹ g cm² s⁻¹). Orbital term only: μ v b (R_t + R_p), with b = sin θ. Target spin is excluded.

## Inputs

- Proto-Earth 0.88 Earth masses, 6,150 km. Theia 0.13 Earth masses, 3,500 km. Canonical contact speed 9.17 km/s at 45°. These are the anchor values in `context.md`.
- Critical speed: midpoints of the published 1:10 and 1:2 anchors (Agnor & Asphaug 2004, as reported in Kokubo & Genda 2010), interpolated linearly in mass ratio and angle. The 1:10 anchors are 1.5–2.0 at 30° and 1.2–1.3 at 45°, in units of escape speed. Valid only for 30–45°.
- Mass ratio γ = 0.148. The interpolation sits closer to the 1:10 anchors than to 1:2.

## Results

Escape speed of the anchor pair: 9.13 km/s. The canonical speed is 1.00 of it.

| Case | v (km/s) | K | L |
|---|---|---|---|
| Canonical, 45° | 9.17 | 0.81 | 1.21 |
| Same speed, 30° | 9.17 | 0.59 | 0.86 |
| K = 1 threshold, 45° | 11.3 | 1.00 | 1.49 |
| K = 1 threshold, 30° | 15.7 | 1.00 | 1.46 |

Monte Carlo (50,000 draws; Theia 0.11–0.15 Earth masses; 30–45°; speed ±10%): K median 0.68 (5th–95th percentile 0.57–0.82). L median 1.03 (0.80–1.30). Fraction in the moon window (K < 1, 1 ≤ L ≤ 2): 0.58. The ±10% speed band never reaches the hit-and-run boundary, so the sweep below covers it.

Sweep, selected rows (v/v_esc, angle → outcome):

- 1.00 at 45° → K 0.81, L 1.20, moon window
- 1.20 at 45° → K 0.97, L 1.45, moon window
- 1.40 at 45° → K 1.13, L 1.69, hit-and-run
- 1.00 at 30° → K 0.58, L 0.85, low L
- 1.40 at 30° → K 0.82, L 1.19, moon window

## What the numbers say

- The canonical anchor is consistent with the literature. Its orbital term (1.21) sits at the top of the 1.1–1.2 range that Canup gives for total pre-impact angular momentum, which includes spin. So the proto-Earth's spin must offset some of the orbital term, as the anchor assumes.
- Angle matters a lot. At the same speed, a 30° impact gives L ≈ 0.86, below the canonical range. The moon window is mostly a grazing-angle window.
- The window closes at high L. Near the 45° threshold, L is about 1.5. Impacts that deliver more angular momentum are more likely to be hit-and-run. K and L are coupled through speed and angle, so they cannot be set independently in the story.
- Both the speed and the angle set the outcome. Reaching hit-and-run at 45° takes about 1.3 times escape speed (≈12 km/s). At 30° it takes about 1.7 (≈15.7 km/s).

## Limits and assumptions

- The angle convention is assumed. The script takes b = sin θ with θ measured from the surface normal. Check this against the source papers before publishing any angle-dependent number.
- Target spin is not in L. It can add or subtract, and it is the largest term left out.
- The critical speeds are interpolated from published midpoints, not from the full Genda et al. fit (coefficients not retrieved). Composition and rock strength can shift the thresholds. The anchors use fluid SPH.
- None of this is a new simulation. Values for K and L at the boundary should be treated as ±0.1–0.2 until SPH runs check them.

## Supersedes

Earlier planning estimates (K ≈ 0.7, L ≈ 1.15 for Theia; the 1.5 threshold for 1:2 at 30°) are replaced by the values above.
