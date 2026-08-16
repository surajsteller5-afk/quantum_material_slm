import json
import math
import sys
sys.path.append('v4/physics')
from quantum_params import compute_g0, compute_kappa, compute_cooperativity

import qutip as qt
import numpy as np

REFERENCE_V_M_FACTOR = 0.1
REFERENCE_CAVITY_Q = 100000

def load_defects(path="v4/database/defects_seed.json"):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = list(data.values())
    return data

def master_equation_simulation(defect, Q, v_m_factor):
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

    # Define operators
    a = qt.destroy(2)
    sm = qt.sigmam()
    sm_dag = qt.sigmap()
    I2 = qt.qeye(2)

    a_full = qt.tensor(a, I2)
    a_dag_full = qt.tensor(a.dag(), I2)
    sm_full = qt.tensor(I2, sm)
    sm_dag_full = qt.tensor(I2, sm_dag)
    sigma_z_full = qt.tensor(I2, qt.sigmaz())

    H = omega_c * a_dag_full * a_full + (omega_c/2) * sigma_z_full + g_eff * (a_full * sm_dag_full + a_dag_full * sm_full)

    # Initial state: cavity vacuum, emitter excited
    psi0 = qt.tensor(qt.basis(2,0), qt.basis(2,1))

    # Collapse operators
    c_ops = [
        math.sqrt(kappa) * a_full,       # cavity loss
        math.sqrt(gamma_hz) * sm_full    # emitter dephasing/decay (using total gamma)
    ]

    # Time array: several Rabi periods but limited by decay
    tlist = np.linspace(0, 1e-8, 1000)   # 10 ns window

    result = qt.mesolve(H, psi0, tlist, c_ops=c_ops, e_ops=[a_dag_full * a_full, sm_dag_full * sm_full])

    # Print parameters
    C = compute_cooperativity(g0_ghz, dw, gamma_hz, kappa)
    print(f"Defect: {defect['defect']} ({defect['host']})")
    print(f"g_eff: {g_eff/1e9:.2f} GHz, kappa: {kappa/1e9:.2f} GHz, gamma: {gamma_hz/1e9:.2f} GHz")
    print(f"Cooperativity C: {C:.3f}")
    print(f"Vacuum Rabi period: {2*math.pi/g_eff*1e9:.2f} ns")
    print()

    return result, tlist

if __name__ == "__main__":
    defects = load_defects()
    target = next(d for d in defects if d["id"] == "diamond_siv")
    result, tlist = master_equation_simulation(target, REFERENCE_CAVITY_Q, REFERENCE_V_M_FACTOR)

    # Optional: plot populations if matplotlib available
    try:
        import matplotlib.pyplot as plt
        cav_pop = result.expect[0]
        atom_pop = result.expect[1]
        plt.figure()
        plt.plot(tlist*1e9, cav_pop, label='Cavity population')
        plt.plot(tlist*1e9, atom_pop, label='Emitter excited population')
        plt.xlabel('Time (ns)')
        plt.ylabel('Population')
        plt.legend()
        plt.title('Room-temperature vacuum Rabi oscillations (SiV- with dissipation)')
        plt.savefig('si_v_rt_rabi.png')
        print('Plot saved as si_v_rt_rabi.png')
    except ImportError:
        print('Matplotlib not available; skipping plot.')