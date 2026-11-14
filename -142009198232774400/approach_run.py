"""Last year's approach: Sun, proto-Earth and Theia, point masses, one plane.

Integrated backward one year from contact. Contact values from assumptions.md
(A-002, A-003, A-009, A-010). Modeled, not published.

Run:  python3 -I approach_run.py          (tables for the chosen direction)
      python3 -I approach_run.py scan     (approach-direction scan)
"""
import math
import sys

import numpy as np
from scipy.integrate import solve_ivp

GM_SUN = 1.32712440018e11          # km^3 s^-2
GM_E = 398600.4418                 # km^3 s^-2, today's Earth
AU = 1.495978707e8                 # km
DAY = 86400.0
YEAR = 365.25 * DAY
R_E_TODAY = 6371.0
MOON_D = 384400.0
M_MOON_E = 1 / 81.3                # Moon / Earth mass
R_SUN = 696000.0
M_SUN_MAG = -26.74

M_PE, R_PE = 0.88, 6150.0          # A-009 (Earth masses, km)
M_TH, R_TH = 0.13, 3500.0          # A-002, A-010
V_CONTACT = 9.5                    # km/s, A-003
ANGLE = 45.0                       # deg from surface normal, A-003/A-005
ALB_TH, ALB_PE = 0.15, 0.30        # geometric albedo: rock, cloud

GM = np.array([GM_SUN, M_PE * GM_E, M_TH * GM_E])
PHI_CHOSEN = 255.0                 # contact direction, deg: lowest-e lane with Theia outside (scan)


def contact_state(phi_deg):
    """Barycentric state at contact. Pair barycentre on a 1 AU circular orbit."""
    m1, m2 = GM[1], GM[2]
    phi = math.radians(phi_deg)
    rhat = np.array([math.cos(phi), math.sin(phi)])
    that = np.array([-math.sin(phi), math.cos(phi)])
    a = math.radians(ANGLE)
    r_rel = (R_PE + R_TH) * rhat                       # Theia minus Earth
    v_rel = V_CONTACT * (-math.cos(a) * rhat + math.sin(a) * that)  # prograde
    vc = math.sqrt((GM_SUN + m1 + m2) / AU)
    bary_r, bary_v = np.array([AU, 0.0]), np.array([0.0, vc])
    f1, f2 = m2 / (m1 + m2), m1 / (m1 + m2)
    pos = [np.zeros(2), bary_r - f1 * r_rel, bary_r + f2 * r_rel]
    vel = [np.zeros(2), bary_v - f1 * v_rel, bary_v + f2 * v_rel]
    # shift to the system barycentre
    mt = GM.sum()
    cp = sum(GM[i] * pos[i] for i in range(3)) / mt
    cv = sum(GM[i] * vel[i] for i in range(3)) / mt
    return np.concatenate([np.concatenate([p - cp for p in pos]),
                           np.concatenate([v - cv for v in vel])])


def rhs(_t, y):
    p = y[:6].reshape(3, 2)
    acc = np.zeros((3, 2))
    for i in range(3):
        for j in range(3):
            if i != j:
                d = p[j] - p[i]
                acc[i] += GM[j] * d / np.linalg.norm(d) ** 3
    return np.concatenate([y[6:], acc.ravel()])


def run(phi_deg):
    return solve_ivp(rhs, (0.0, -YEAR), contact_state(phi_deg), method="DOP853",
                     rtol=1e-12, atol=1e-6, dense_output=True)


def unpack(sol, t):
    y = sol.sol(t)
    p, v = y[:6].reshape(3, 2), y[6:].reshape(3, 2)
    return p, v


def elements(r, v, gm):
    rn, vn = np.linalg.norm(r), np.linalg.norm(v)
    a = 1 / (2 / rn - vn ** 2 / gm)
    h = r[0] * v[1] - r[1] * v[0]
    e = math.sqrt(max(0.0, 1 - h ** 2 / (gm * a)))
    return a, e, 2 * math.pi * math.sqrt(a ** 3 / gm) / DAY


def signed_angle(frm, to):
    """CCW angle from frm to to, deg in (-180, 180]. CCW = east on the sky."""
    a = math.degrees(math.atan2(frm[0] * to[1] - frm[1] * to[0], frm @ to))
    return a


def phase_lambert(alpha):
    return (math.sin(alpha) + (math.pi - alpha) * math.cos(alpha)) / math.pi


def view(obs, tgt, sun, r_tgt, albedo):
    """Elongation (deg, +east), angular diameter (deg), magnitude, lit fraction."""
    to_t, to_s = tgt - obs, sun - obs
    d = np.linalg.norm(to_t)
    elong = signed_angle(to_s, to_t)
    s_t, o_t = sun - tgt, obs - tgt
    alpha = math.acos(np.clip(s_t @ o_t / (np.linalg.norm(s_t) * d), -1, 1))
    rh = np.linalg.norm(s_t) / AU
    flux = albedo * (r_tgt / d) ** 2 * phase_lambert(alpha) / rh ** 2
    mag = M_SUN_MAG - 2.5 * math.log10(flux) if flux > 0 else float("nan")
    size = math.degrees(2 * math.atan(r_tgt / d))
    return elong, size, mag, (1 + math.cos(alpha)) / 2, d


def tide_on_earth(d):
    """Tidal acceleration / surface gravity, in units of today's Moon on today's Earth."""
    return (M_TH / M_MOON_E) / M_PE * (R_PE / R_E_TODAY) ** 3 * (MOON_D / d) ** 3


def tide_on_theia(d):
    return (M_PE / M_MOON_E) / M_TH * (R_TH / R_E_TODAY) ** 3 * (MOON_D / d) ** 3


def fmt_size(deg):
    return f"{deg * 60:.1f}'" if deg < 1 else f"{deg:.1f} deg"


def scan():
    print(" phi |  a_PE   e_PE |  a_TH   e_TH | sep 1yr (AU) | min sep t<-2d (km)")
    for phi in range(0, 360, 15):
        sol = run(phi)
        p, v = unpack(sol, -YEAR)
        ape, epe, _ = elements(p[1] - p[0], v[1] - v[0], GM[0] + GM[1])
        ath, eth, _ = elements(p[2] - p[0], v[2] - v[0], GM[0] + GM[2])
        ts = np.linspace(-2 * DAY, -YEAR, 4000)
        mins = min(np.linalg.norm(unpack(sol, t)[0][2] - unpack(sol, t)[0][1]) for t in ts)
        sep = np.linalg.norm(p[2] - p[1]) / AU
        print(f"{phi:4d} | {ape/AU:.3f} {epe:.3f} | {ath/AU:.3f} {eth:.3f} | {sep:6.3f}       | {mins:,.0f}")


def tables(phi):
    sol = run(phi)
    p, v = unpack(sol, -YEAR)
    print(f"Contact direction phi = {phi} deg")
    for name, i in (("Proto-Earth", 1), ("Theia", 2)):
        a, e, per = elements(p[i] - p[0], v[i] - v[0], GM[0] + GM[i])
        print(f"  {name} one year out: a = {a/AU:.3f} AU, e = {e:.3f}, year = {per:.0f} d")
    hill = AU * (GM[1] / (3 * GM_SUN)) ** (1 / 3)
    print(f"  Hill radius {hill:,.0f} km; Roche limit 18,500 km")

    # event times
    def sep(t):
        q = unpack(sol, t)[0]
        return np.linalg.norm(q[2] - q[1])
    ts = np.linspace(0, -YEAR, 200001)
    seps = np.array([sep(t) for t in ts[:20001]])  # last ~36 days, fine grid
    for label, target in (("Hill entry", hill), ("Moon distance", MOON_D), ("Roche", 18500.0)):
        idx = np.where(seps > target)[0]
        if len(idx):
            print(f"  {label}: {-ts[idx[0]] / 3600:.2f} hr before contact "
                  f"({-ts[idx[0]] / DAY:.2f} d)")

    print("\nClosing distance and tides")
    print("  before | distance (km) | rel. speed (km/s) | size from Earth | size from Theia | tide Earth | tide Theia")
    marks = [("1 yr", YEAR), ("6 mo", YEAR / 2), ("3 mo", YEAR / 4), ("1 mo", 30 * DAY),
             ("2 wk", 14 * DAY), ("1 wk", 7 * DAY), ("5 d", 5 * DAY), ("3 d", 3 * DAY),
             ("1 d", DAY), ("12 hr", 12 * 3600), ("6 hr", 6 * 3600), ("2 hr", 7200),
             ("1 hr", 3600), ("10 min", 600), ("0", 0.0)]
    for label, dt in marks:
        q, w = unpack(sol, -dt)
        rel, vrel = q[2] - q[1], w[2] - w[1]
        d = np.linalg.norm(rel)
        closing = np.linalg.norm(vrel)
        s_e = math.degrees(2 * math.atan(R_TH / d))
        s_t = math.degrees(2 * math.atan(R_PE / d))
        print(f"  {label:6s} | {d:13,.0f} | {closing:6.2f} | {fmt_size(s_e):>9s} | "
              f"{fmt_size(s_t):>9s} | {tide_on_earth(d):10.3g} | {tide_on_theia(d):10.3g}")

    print("\nTheia from Earth / Earth from Theia (monthly, then fine)")
    print("  before | T elong | T size | T mag | T lit || E elong | E size | E mag | E lit")
    fine = [(f"{m} mo", m * YEAR / 12) for m in range(12, 0, -1)]
    fine += [("3 wk", 21 * DAY), ("2 wk", 14 * DAY), ("1 wk", 7 * DAY), ("3 d", 3 * DAY),
             ("1 d", DAY), ("6 hr", 6 * 3600), ("1 hr", 3600), ("30 min", 1800),
             ("10 min", 600), ("1 min", 60)]
    for label, dt in fine:
        q, _ = unpack(sol, -dt)
        te, ts_, tm, tl, _ = view(q[1], q[2], q[0], R_TH, ALB_TH)
        ee, es, em, el, _ = view(q[2], q[1], q[0], R_PE, ALB_PE)
        print(f"  {label:6s} | {te:7.1f} | {fmt_size(ts_):>7s} | {tm:5.1f} | {tl:4.0%} || "
              f"{ee:7.1f} | {fmt_size(es):>7s} | {em:5.1f} | {el:4.0%}")

    # opposition / smallest elongation / eclipse of the Sun from Earth's centre
    tt = np.linspace(-YEAR, 0, 400001)
    best_opp, eclipse = (0, None), []
    for t in tt[::20]:
        q, _ = unpack(sol, t)
        te = view(q[1], q[2], q[0], R_TH, ALB_TH)[0]
        if abs(te) > abs(best_opp[0]):
            best_opp = (te, t)
    print(f"\nMax elongation {best_opp[0]:.1f} deg at {-best_opp[1] / DAY:.1f} d before contact")
    for t in np.linspace(-4 * 3600, 0, 24001):
        q, _ = unpack(sol, t)
        to_t, to_s = q[2] - q[1], q[0] - q[1]
        dt_ = np.linalg.norm(to_t)
        sepang = math.degrees(math.acos(np.clip(to_t @ to_s / (dt_ * np.linalg.norm(to_s)), -1, 1)))
        rad_t = math.degrees(math.asin(min(1, R_TH / dt_)))
        rad_s = math.degrees(math.asin(R_SUN / np.linalg.norm(to_s)))
        if sepang < rad_t - rad_s:
            eclipse.append(t)
    if eclipse:
        print(f"Sun fully covered from Earth's centre: {-eclipse[0] / 60:.0f} to {-eclipse[-1] / 60:.0f} min before contact")
    else:
        print("No total eclipse from Earth's centre in the last 4 hr")
    def first_before(fn, thresh):
        for t in np.linspace(-YEAR, 0, 200001):
            if fn(t) >= thresh:
                return -t
    dist = lambda t: np.linalg.norm(unpack(sol, t)[0][2] - unpack(sol, t)[0][1])
    t_moon = first_before(lambda t: math.degrees(2 * math.atan(R_TH / dist(t))), 31.0 / 60)
    t_te = first_before(lambda t: tide_on_earth(dist(t)), 1.0)
    t_tt = first_before(lambda t: tide_on_theia(dist(t)), 1.0)
    print(f"Theia wider than the full Moon from Earth: {t_moon / DAY:.1f} d before")
    print(f"Tide on Earth reaches today's lunar tide: {t_te / DAY:.1f} d before")
    print(f"Tide on Theia reaches today's lunar tide on Earth: {t_tt / DAY:.1f} d before")
    mins = min((abs(view(unpack(sol, t)[0][1], unpack(sol, t)[0][2], unpack(sol, t)[0][0], R_TH, ALB_TH)[0]), t)
               for t in np.linspace(-40 * DAY, 0, 40001))
    print(f"Smallest elongation {mins[0]:.1f} deg at {-mins[1] / DAY:.1f} d before")
    q, _ = unpack(sol, 0.0)
    delta = signed_angle(q[0] - q[1], q[2] - q[1])
    print(f"Contact point: {delta:+.1f} deg from the Sun direction -> local time "
          f"{12 + delta / 15:.2f} h (today's hours)")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        scan()
    else:
        tables(PHI_CHOSEN)
