import json
import math
import sys
sys.path.append('v5/physics')
from hybrid_coupling import exchange_coupling_from_distance

REFERENCE_CAVITY_Q = 100000
REFERENCE_V_M_FACTOR = 0.1

def load_json(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = list(data.values())
    return data

def compute_kappa(zpl_nm, cavity_Q):
    omega_c = 2 * math.pi * 299792458 / (zpl_nm * 1e-9)
    return omega_c / cavity_Q

def main():
    spin_centers = load_json('v5/database/spin_centers_seed.json')
    antennas = load_json('v5/database/antennas_seed.json')

    spin = next(d for d in spin_centers if d["id"] == "diamond_nv")
    antenna = next(d for d in antennas if d["id"] == "diamond_siv")

    T2_ms = spin["T2_ms"]
    gamma_spin_hz = 1.0 / (T2_ms * 1e-3)
    kappa_hz = compute_kappa(antenna["zpl_nm"], REFERENCE_CAVITY_Q)
    kappa_ghz = kappa_hz / 1e9
    gamma_ghz = gamma_spin_hz / 1e9

    print("Sensitivity of cooperativity to exchange coupling J")
    print(f"Spin: {spin['defect']}, T2 = {T2_ms} ms")
    print(f"Antenna: {antenna['defect']}, κ = {kappa_ghz:.2f} GHz")
    print(f"γ_spin = {gamma_spin_hz:.3e} Hz\n")

    J_values_mhz = [1, 5, 10, 50, 100, 500, 1000]
    print(f"{'J (MHz)':<10} {'C_eff':<12} {'Regime'}")
    print("-" * 40)
    for J_mhz in J_values_mhz:
        J_ghz = J_mhz / 1e3
        C = (J_ghz**2) / (kappa_ghz * gamma_ghz)
        regime = "strong" if C > 1 else ("moderate" if C > 0.1 else "weak")
        print(f"{J_mhz:<10} {C:<12.4f} {regime}")

if __name__ == "__main__":
    main()
