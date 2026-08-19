import json
import math
import sys
sys.path.append('v5/physics')
from hybrid_coupling import dipole_dipole_coupling

REFERENCE_CAVITY_Q = 100000
REFERENCE_V_M_FACTOR = 0.1

def load_json(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = list(data.values())
    return data

def compute_g0(zpl_nm, dipole_debye, eps_r, v_m_factor):
    # same deterministic g0 as before
    HBAR = 1.0545718e-34
    C = 299792458
    EPSILON_0 = 8.8541878e-12
    DEBYE_TO_CM = 3.33564e-30
    zpl_m = zpl_nm * 1e-9
    dipole_cm = dipole_debye * DEBYE_TO_CM
    n_refractive = math.sqrt(eps_r)
    v_m = v_m_factor * (zpl_m / n_refractive)**3
    omega_c = 2 * math.pi * C / zpl_m
    term1 = dipole_cm / HBAR
    term2 = math.sqrt((HBAR * omega_c) / (2 * EPSILON_0 * eps_r * v_m))
    return ((term1 * term2) / (2 * math.pi)) / 1e9

def compute_kappa(zpl_nm, cavity_Q):
    omega_c = 2 * math.pi * 299792458 / (zpl_nm * 1e-9)
    return omega_c / cavity_Q

def cooperativity(g0_ghz, dw, gamma_hz, kappa_hz):
    g_eff = g0_ghz * math.sqrt(dw) * 1e9
    return (g_eff**2) / (kappa_hz * gamma_hz)

def main():
    spin_centers = load_json('v5/database/spin_centers_seed.json')
    antennas = load_json('v5/database/antennas_seed.json')

    print("Screening hybrid pairs (dipole-dipole coupling only, no exchange assumed)\n")
    print(f"{'Spin':<12} {'Antenna':<12} {'r (nm)':<8} {'J_dd (GHz)':<10} {'C_eff':<10} {'Note'}")
    print("-" * 70)

    # Assume spin centers have a small transition dipole (magnetic-like) of 0.01 D for coupling estimate
    spin_dipole_assumed = 0.01  # Debye

    for spin in spin_centers:
        for antenna in antennas:
            # Use a fixed trial distance of 1 nm for all pairs
            r_nm = 1.0
            eps_r = antenna.get("eps_r", 5.7)
            # Dipole-dipole coupling between spin transition dipole and antenna dipole
            try:
                J_dd = dipole_dipole_coupling(spin_dipole_assumed, antenna["dipole_D"], r_nm, eps_r)
            except Exception as e:
                J_dd = None

            # Compute antenna g0
            g0_ghz = compute_g0(antenna["zpl_nm"], antenna["dipole_D"], eps_r, REFERENCE_V_M_FACTOR)
            kappa = compute_kappa(antenna["zpl_nm"], REFERENCE_CAVITY_Q)
            C_antenna = cooperativity(g0_ghz, antenna["dw_factor"], antenna["gamma_hom_Hz"], kappa)

            # Effective coupling: antenna g0 reduced by ratio J_dd / (optical transition energy)
            # This is a rough estimate; if J_dd is much smaller than optical frequency, spin sees weak coupling.
            optical_freq_hz = 299792458 / (antenna["zpl_nm"] * 1e-9)
            if J_dd is not None:
                g_eff_spin = g0_ghz * (J_dd / optical_freq_hz)
            else:
                g_eff_spin = 0.0

            C_spin = (g_eff_spin * math.sqrt(antenna["dw_factor"]) * 1e9)**2 / (kappa * antenna["gamma_hom_Hz"])

            note = "promising" if C_spin > 0.01 else "weak"
            print(f"{spin['defect']:<12} {antenna['defect']:<12} {r_nm:<8} {J_dd if J_dd else 0:<10.4f} {C_spin:<10.2e} {note}")

if __name__ == "__main__":
    main()
