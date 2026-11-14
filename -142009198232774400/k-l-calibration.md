# K and L calibration

Working note for the Theia anchor. Analytic, not an SPH run. Reproduce with `python3 -I kl_calibration.py`. Input values are registered in `assumptions.md`.

## Definitions

**K**, the escape ratio: (impact speed ÷ two-body escape speed) ÷ (critical hit-and-run speed ÷ escape speed). K < 1 merges. K ≥ 1 is hit-and-run, and the impactor leaves.

**L**, the spin budget: orbital angular momentum of the impact ÷ Earth-Moon system angular momentum (3.5 × 10⁴¹ g cm² s⁻¹). Orbital term only: μ v b (R_t + R_p). Target spin is excluded.

Angle: b = sin θ, θ measured from the surface normal, so a grazing impact has b = 1 (Canup 2008). Cross-check: Canup's scaling, L ≈ 1.3 L_EM b (M_T/M⊕)^5/3 (γ/0.1)(v/v_esc), gives the same L for the anchor.

Mass ratio: γ here is impactor ÷ target (Genda et al. 2012). Canup's γ is impactor ÷ total. Don't mix the two formulas.

## Inputs

- Proto-Earth and Theia masses and radii: A-002, A-009, A-010. Contact at 45° and 9.5 km/s: A-003.
- Critical speed: A-006. Midpoints of the 1:10 and 1:2 anchors in Genda, Kokubo & Ida (2012), interpolated linearly in mass ratio and angle. The 1:10 anchors are 1.5–2.0 at 30° and 1.2–1.3 at 45°, in units of escape speed. Valid only for 30–45°.
- γ = 0.148, so the interpolation sits close to the 1:10 anchors.

## Results

Escape speed of the anchor pair: 9.13 km/s. Contact at 9.5 km/s is 1.04 of it.

| Case | v (km/s) | v / v_esc | K | L |
|---|---|---|---|---|
| Anchor, 45° | 9.5 | 1.04 | 0.84 | 1.25 |
| Same speed, 30° | 9.5 | 1.04 | 0.61 | 0.89 |
| K = 1 threshold, 45° | 11.3 | 1.24 | 1.00 | 1.49 |
| K = 1 threshold, 30° | 15.7 | 1.71 | 1.00 | 1.46 |

Monte Carlo (50,000 draws; Theia 0.11–0.15 Earth masses; 30–45°; speed ±10% of 9.5 km/s): K median 0.70 (5th–95th percentile 0.59–0.85). L median 1.07 (0.83–1.35). None reach hit-and-run. 66% fall in the heuristic moon window below.

Sweep, selected rows (v/v_esc, angle → K, L):

- 1.00 at 45° → 0.81, 1.20
- 1.20 at 45° → 0.97, 1.45
- 1.40 at 45° → 1.13, 1.69, hit-and-run
- 1.00 at 30° → 0.58, 0.85
- 1.40 at 30° → 0.82, 1.19

## Moon window (heuristic)

K < 1 and 1 ≤ L ≤ 2. This is a story device, not a published criterion. The L here is orbital only, while the published thresholds are totals that include spin: Canup's 1.1–1.2 for canonical runs, and ~2 as a minimum in the 2023 survey of Moon-forming impacts. The upper edge of 2 is a choice.

## What the numbers say

- The anchor's orbital L (1.25) sits just above Canup's 1.1–1.2 total. The proto-Earth's spin must offset part of it, which A-004 provides.
- Angle matters a lot. At the same speed, a 30° impact gives L ≈ 0.89.
- K and L are coupled through speed and angle. They cannot be set independently in a story. Near the 45° threshold, L is about 1.5. More angular momentum means closer to hit-and-run.
- Hit-and-run at 45° needs 1.24 times escape speed, 11.3 km/s. At 30° it needs 1.71, 15.7 km/s.

## Limits

- Target spin is not in L. It is the largest term left out.
- The critical speeds are interpolated from published midpoints, not the full Genda et al. fit. Composition and rock strength can shift them; the anchors use fluid SPH.
- Treat K and L near the boundaries as ±0.1–0.2 until checked by SPH runs.
