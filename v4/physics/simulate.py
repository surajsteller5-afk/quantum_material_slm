import qutip as qt
import math
from v4.physics.quantum_params import compute_g0

def jaynes_cummings_simulation(zpl_nm, dipole_debye, eps_r, v_m_factor, cavity_kappa, spin_T2):
    # g0 in GHz
    g0_GHz = compute_g0(zpl_nm, dipole_debye, eps_r, v_m_factor)
    g0 = g0_GHz * 1e9  # Hz
    omega_c = 2 * math.pi * 299792458 / (zpl_nm * 1e-9)  # cavity resonant with ZPL
    # Two-level system (spin qubit) coupled to cavity
    # Hamiltonian (Jaynes-Cummings, rotating wave)
    # Use hbar = 1 units, so g0 is in rad/s
    # For simplicity, simulate vacuum Rabi oscillations
    # Define spin lowering/raising and cavity operators
    sm = qt.sigmam()
    sm_dag = qt.sigmap()
    a = qt.destroy(2)  # two-level cavity
    H = omega_c * a.dag() * a + omega_c/2 * qt.sigmaz() + g0 * (a * sm_dag + a.dag() * sm)
    # Initial state: excited atom, empty cavity
    psi0 = qt.tensor(qt.basis(2,0), qt.basis(2,0))  # cavity in 0, atom in excited? Actually need tensor product order
    # Correct: cavity first, atom second
    psi0 = qt.tensor(qt.basis(2,0), qt.basis(2,1))  # cavity vacuum, atom excited
    # Solve Schrödinger equation
    tlist = qt.np.linspace(0, 2*math.pi/g0, 100)
    result = qt.sesolve(H, psi0, tlist, [a.dag()*a, sm_dag*sm])
    return result