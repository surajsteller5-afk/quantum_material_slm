import math
import sys
sys.path.append('v4/physics')
from quantum_params import compute_g0, compute_kappa, compute_cooperativity

REFERENCE_CAVITY_Q = 100000
REFERENCE_V_M_FACTOR = 0.1

def compare(zpl_nm, dipole_D, eps_r, dw_soc, gamma_soc, dw_free, gamma_free):
    g0_ghz = compute_g0(zpl_nm, dipole_D, eps_r, REFERENCE_V_M_FACTOR)
    kappa = compute_kappa(zpl_nm, REFERENCE_CAVITY_Q)

    C_soc = compute_cooperativity(g0_ghz, dw_soc, gamma_soc, kappa)
    C_free = compute_cooperativity(g0_ghz, dw_free, gamma_free, kappa)

    print(f"Reference cavity: Q={REFERENCE_CAVITY_Q}, Vm factor={REFERENCE_V_M_FACTOR}")
    print(f"g0 = {g0_ghz:.2f} GHz, kappa = {kappa/1e9:.2f} GHz")
    print(f"ZPL = {zpl_nm} nm, dipole = {dipole_D} D, eps_r = {eps_r}")
    print()
    print(f"SOC-mediated:  DW = {dw_soc}, gamma = {gamma_soc:.2e} Hz -> C = {C_soc:.3f}")
    print(f"SOC-free:      DW = {dw_free}, gamma = {gamma_free:.2e} Hz -> C = {C_free:.3f}")
    print()
    if C_free > 1:
        print("SOC-free mechanism reaches strong coupling at RT.")
    elif C_free > 0.1:
        print("SOC-free mechanism reaches moderate Purcell enhancement.")
    else:
        print("SOC-free still insufficient under this cavity.")
    return C_soc, C_free

if __name__ == "__main__":
    # Use SiV- as baseline (SOC-mediated)
    zpl = 738.0
    dipole = 1.8
    eps_r = 5.7
    # SOC-mediated values (from database)
    dw_soc = 0.6
    gamma_soc = 8e9
    # Hypothetical SOC-free values
    dw_free = 0.95
    gamma_free = 1e8

    compare(zpl, dipole, eps_r, dw_soc, gamma_soc, dw_free, gamma_free)