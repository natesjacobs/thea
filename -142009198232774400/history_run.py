"""Approach history: the centuries before contact, and when the hit becomes certain.

Sun, proto-Earth and Theia, point masses, one plane (A-013). Same contact state as
approach_run.py (A-002, A-003, A-009, A-010). Integrated backward from contact to
list every conjunction, then forward from earlier epochs with small errors to see
when the collision stops depending on them. Modeled, not published.

Run:  python3 -I history_run.py   (needs: pip install rebound)
"""
import math
import os
import sys

import numpy as np
import rebound

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from approach_run import AU, DAY, GM, PHI_CHOSEN, R_PE, R_TH, YEAR, contact_state

YEARS_BACK = 3000
R_SUM = R_PE + R_TH
HILL = AU * ((GM[1] + GM[2]) / (3 * GM[0])) ** (1 / 3)   # mutual Hill radius
SAMPLE = 1 * DAY
EPOCHS = [1, 5, 10, 20, 30, 40, 50, 52, 53, 54, 55, 60, 80, 100]
RUNS = 40
# One-off kicks to Theia from a planetesimal hit at ~10 km/s: dv ~ (m/M) * 10 km/s
KICKS = {"10 km": 2e-8, "30 km": 5.4e-7, "100 km": 2e-5}   # km/s
RNG = np.random.default_rng(1)


def make_sim(state):
    sim = rebound.Simulation()
    sim.G = 1.0
    sim.integrator = "ias15"
    p, v = state[:6].reshape(3, 2), state[6:].reshape(3, 2)
    for i in range(3):
        sim.add(m=GM[i], x=p[i, 0], y=p[i, 1], vx=v[i, 0], vy=v[i, 1])
    return sim


def sep(sim):
    a, b = sim.particles[1], sim.particles[2]
    return math.dist((a.x, a.y), (b.x, b.y))


def state_of(sim):
    ps = sim.particles
    return np.array([ps[i].x for i in range(3)] + [ps[i].y for i in range(3)]
                    + [ps[i].vx for i in range(3)] + [ps[i].vy for i in range(3)])


def to_state(s):
    """Reorder (x0..x2, y0..y2, vx.., vy..) into contact_state layout."""
    x, y, vx, vy = s[0:3], s[3:6], s[6:9], s[9:12]
    return np.concatenate([np.ravel(np.column_stack([x, y])), np.ravel(np.column_stack([vx, vy]))])


def orbit(sim, i):
    o = sim.particles[i].orbit(primary=sim.particles[0])
    return o.a / AU, o.e, o.P / DAY


def history():
    """Backward from contact. Returns passes and saved states (every 10 yr)."""
    sim = make_sim(contact_state(PHI_CHOSEN))
    sim.dt = -0.01 * DAY
    lon0 = math.atan2(sim.particles[1].y, sim.particles[1].x)
    t, prev2, prev1 = 0.0, None, None
    passes, saves = [], {}
    n = int(YEARS_BACK * YEAR / SAMPLE)
    for k in range(1, n + 1):
        t = -k * SAMPLE
        sim.integrate(t, exact_finish_time=1)
        d = sep(sim)
        if k % int(YEAR / SAMPLE) == 0:
            saves[round(-t / YEAR)] = state_of(sim)
        if prev2 is not None and prev1 < prev2 and prev1 < d and k > 30:
            e = sim.particles[1]
            lon = math.degrees(math.atan2(e.y, e.x) - lon0) % 360
            passes.append((-(t + SAMPLE) / YEAR, prev1, lon, orbit(sim, 1), orbit(sim, 2)))
        prev2, prev1 = prev1, d
    return passes, saves


def forward(state, t0, dv=0.0, dr=0.0):
    """Forward from t0 (s, negative) with errors on Theia. Returns (hit, min sep, angle)."""
    st = to_state(state).copy()
    if dr or dv:
        u = RNG.normal(size=2); u /= np.linalg.norm(u)
        w = RNG.normal(size=2); w /= np.linalg.norm(w)
        st[4:6] += dr * u          # Theia position (x, y)
        st[10:12] += dv * w        # Theia velocity
    sim = make_sim(st)
    sim.t = t0
    sim.integrate(-40 * DAY)
    best = float("inf")
    t = -40 * DAY
    while t < 40 * DAY:
        prev = sim.copy()
        t += 600.0
        sim.integrate(t, exact_finish_time=1)
        d = sep(sim)
        best = min(best, d)
        if d < R_SUM:
            sim, t = prev, prev.t          # step back, then close in at 1 s
            while sep(sim) > R_SUM:
                t += 1.0
                sim.integrate(t, exact_finish_time=1)
            a, b = sim.particles[1], sim.particles[2]
            r = np.array([b.x - a.x, b.y - a.y]); v = np.array([b.vx - a.vx, b.vy - a.vy])
            ang = math.degrees(math.acos(abs(r @ v) / (np.linalg.norm(r) * np.linalg.norm(v))))
            return True, R_SUM, ang
    return False, best, None


def main():
    passes, saves = history()
    print(f"Mutual Hill radius {HILL:,.0f} km. Contact at {R_SUM:,.0f} km.")
    print("\nClose passes inside 2 mutual Hill radii, last 3,000 years.")
    print("Orbits listed are those before the pass (the integration runs backward).")
    print("  yr before   min dist (km)  Hill   a_E     a_T     e_T    gap(d)")
    for yr, d, lon, oe, ot in passes:
        if d < 2 * HILL:
            print(f"  {yr:8.1f} {d:14,.0f} {d/HILL:6.2f} {oe[0]:.4f} {ot[0]:.4f} {ot[1]:.3f} {ot[2]-oe[2]:7.1f}")
    deep = [p[0] for p in passes if p[1] < HILL]
    gaps = np.diff(deep)
    print(f"\n{len(passes)} close passes (local minima of distance); {len(deep)} inside one Hill radius.")
    print(f"Interval between Hill-radius passes: median {np.median(gaps):.0f} yr, "
          f"range {gaps.min():.0f}-{gaps.max():.0f} yr.")

    def spread(res):
        angs = np.array([r[2] for r in res if r[0]])
        if len(angs) == 0:
            return f"{0:3d}%        -      "
        lo, hi = np.percentile(angs, [5, 95])
        return f"{100 * len(angs) / len(res):3.0f}%  {lo:4.1f}-{hi:4.1f} deg"

    print(f"\nCertainty test: forward from each epoch, {RUNS} runs per cell.")
    print("Cell: share of runs that still hit on this pass, and the 5-95% range of the "
          "contact angle (from the surface normal, A-005).")
    print("Tracking: Theia's position and velocity known to 1 km and 1 mm/s.")
    print("Kick: one unseen planetesimal hit on Theia at that epoch, size as labelled.")
    print("  yr back | nominal | tracking            | kick 10 km          | kick 30 km          | kick 100 km")
    for yr in EPOCHS:
        nom = forward(saves[yr], -yr * YEAR)
        cells = [spread([forward(saves[yr], -yr * YEAR, dr=1.0, dv=1e-6) for _ in range(RUNS)])]
        for dv in KICKS.values():
            cells.append(spread([forward(saves[yr], -yr * YEAR, dv=dv) for _ in range(RUNS)]))
        n = f"{nom[2]:5.1f}" if nom[0] else " miss"
        print(f"  {yr:6d}  | {n}   | " + " | ".join(cells))


if __name__ == "__main__":
    main()
