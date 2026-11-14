"""K (escape ratio) and L (spin budget) for the Theia anchor.

Analytic calibration against published anchors. Not an SPH simulation.
Run with: python3 -I kl_calibration.py
"""
import math
import random

G = 6.674e-8        # cm^3 g^-1 s^-2
M_E = 5.972e27      # g
L_EM = 3.5e41       # g cm^2 s^-1

# Anchor values from context.md in this folder
M_PE, R_PE = 0.88 * M_E, 6.15e8     # proto-Earth (6,150 km)
M_TH, R_TH = 0.13 * M_E, 3.5e8      # Theia (3,500 km)
V_CANON = 9.5e5                     # cm/s, contact speed at 45 deg (A-003)


def v_esc(m_t, r_t, m_p, r_p):
    return math.sqrt(2 * G * (m_t + m_p) / (r_t + r_p))


def v_cr_over_vesc(gamma, theta_deg):
    """Critical hit-and-run speed / v_esc.

    Midpoints of the published 1:10 and 1:2 anchors (Genda, Kokubo & Ida
    2012, ApJ 744, 137), linear in mass ratio and angle.
    gamma = impactor/target (Genda). Canup uses impactor/total.
    Valid for 30-45 deg only.
      1:10 -> 30 deg 1.5-2.0, 45 deg 1.2-1.3
      1:2  -> 30 deg 1.4-1.5, 45 deg 1.1-1.2
    """
    if not 30.0 <= theta_deg <= 45.0:
        raise ValueError("angle outside the anchored range (30-45 deg)")
    f = min(max((gamma - 0.10) / 0.40, 0.0), 1.0)
    v30 = 1.75 + (1.45 - 1.75) * f
    v45 = 1.25 + (1.15 - 1.25) * f
    return v30 + (v45 - v30) * (theta_deg - 30.0) / 15.0


def L_orb(m_t, r_t, m_p, r_p, v, theta_deg):
    """Orbital angular momentum / L_EM. b = sin(theta), theta from the
    surface normal (Canup 2008). Target spin excluded."""
    mu = m_t * m_p / (m_t + m_p)
    b = math.sin(math.radians(theta_deg))
    return mu * v * b * (r_t + r_p) / L_EM


def K(m_t, r_t, m_p, r_p, v, theta_deg):
    ratio = v / v_esc(m_t, r_t, m_p, r_p)
    return ratio / v_cr_over_vesc(m_p / m_t, theta_deg)


def outcome(k, l):
    if k >= 1:
        return "hit-and-run"
    if l < 1:
        return "low L"
    if l <= 2:
        return "moon window*"
    return "high L, merge"


def main():
    ve = v_esc(M_PE, R_PE, M_TH, R_TH)
    print(f"Anchor v_esc = {ve / 1e5:.2f} km/s; gamma = {M_TH / M_PE:.3f}")

    print("\nAnchor and threshold cases")
    for label, v, th in [
        ("anchor 45 deg", V_CANON, 45.0),
        ("same speed 30 deg", V_CANON, 30.0),
    ]:
        k = K(M_PE, R_PE, M_TH, R_TH, v, th)
        l = L_orb(M_PE, R_PE, M_TH, R_TH, v, th)
        print(f"  {label}: v/v_esc = {v / ve:.2f}, K = {k:.2f}, L = {l:.2f}")
    for th in (30.0, 45.0):
        vc = v_cr_over_vesc(M_TH / M_PE, th) * ve
        l = L_orb(M_PE, R_PE, M_TH, R_TH, vc, th)
        print(f"  K = 1 at {th:.0f} deg: v = {vc / 1e5:.1f} km/s, L = {l:.2f}")

    print("\nMonte Carlo: Theia 0.11-0.15 M_E, 30-45 deg, speed +/-10% of anchor")
    rng = random.Random(42)
    n = 50000
    ks, ls, window = [], [], 0
    for _ in range(n):
        m_th = rng.uniform(0.11, 0.15) * M_E
        r_th = R_TH * (m_th / M_TH) ** (1 / 3)
        th = rng.uniform(30.0, 45.0)
        v = V_CANON * rng.uniform(0.90, 1.10)
        k = K(M_PE, R_PE, m_th, r_th, v, th)
        l = L_orb(M_PE, R_PE, m_th, r_th, v, th)
        ks.append(k)
        ls.append(l)
        window += outcome(k, l) == "moon window*"
    ks.sort()
    ls.sort()
    print(f"  K: p5 {ks[int(.05 * n)]:.2f}, median {ks[n // 2]:.2f}, p95 {ks[int(.95 * n)]:.2f}")
    print(f"  L: p5 {ls[int(.05 * n)]:.2f}, median {ls[n // 2]:.2f}, p95 {ls[int(.95 * n)]:.2f}")
    print(f"  moon window* fraction: {window / n:.2f}")

    print("\nSweep: speed (v/v_esc) and angle, anchor Theia")
    print("  v/v_esc  theta    K     L     outcome (* heuristic: orbital L only)")
    for th in (30.0, 35.0, 40.0, 45.0):
        for vr in (0.8, 1.0, 1.2, 1.4, 1.6):
            v = vr * ve
            k = K(M_PE, R_PE, M_TH, R_TH, v, th)
            l = L_orb(M_PE, R_PE, M_TH, R_TH, v, th)
            print(f"  {vr:5.2f}   {th:4.0f}   {k:4.2f}  {l:4.2f}  {outcome(k, l)}")


if __name__ == "__main__":
    main()
