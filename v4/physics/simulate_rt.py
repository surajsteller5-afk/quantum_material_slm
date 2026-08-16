import json
import math
import sys
sys.path.append('v4/physics')
from quantum_params import compute_g0, compute_kappa, compute_cooperativity

import qutip as qt
import numpy as np

REFERENCE_V_M_FACTOR = 0.1
REFERENCE_CAVITY_Q = 100000   # we can vary this

def load_defects(path="v4/database/defects_seed.json"):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = list(data.values())
    return data
def jaynes_cummings_simulation(defect, Q, v_m_factor):
    zpl = defect["zpl_nm"]
    dipole = defect["dipole_D"]
    eps_r = defect["eps_r"]
    dw = defect["dw_factor_300K"]
    gamma_hz = defect["gamma_hom_300K_Hz"]

    g0_ghz = compute_g0(zpl, dipole, eps_r, v_m_factor)
    g0 = g0_ghz * 1e9
    omega_c = 2 * math.pi * 299792458 / (zpl * 1e-9)
    kappa = compute_kappa(zpl, Q)
    g_eff = g0 * math.sqrt(dw)
    C = compute_cooperativity(g0_ghz, dw, gamma_hz, kappa)

    print(f"Defect: {defect['defect']} ({defect['host']})")
    print(f"ZPL: {zpl} nm, Dipole: {dipole} D, eps_r: {eps_r}")
    print(f"DW: {dw}, gamma: {gamma_hz:.2e} Hz")
    print(f"g0: {g0_ghz:.2f} GHz, g_eff: {g_eff/1e9:.2f} GHz")
    print(f"kappa: {kappa:.2e} Hz")
    print(f"Cooperativity C: {C:.3f}")
    print(f"Vacuum Rabi frequency: {g_eff/1e9:.2f} GHz")
    print()
    return None, None, C
if __name__ == "__main__":
    defects = load_defects()
    targets = [
        next(d for d in defects if d["id"] == "diamond_siv"),
        next(d for d in defects if d["id"] == "hbn_vb")
    ]
    Q = REFERENCE_CAVITY_Q
    for defect in targets:
        jaynes_cummings_simulation(defect, Q, REFERENCE_V_M_FACTOR)
