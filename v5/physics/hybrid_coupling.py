import math

def dipole_dipole_coupling(mu1_debye, mu2_debye, r_nm, eps_r, angle_deg=0):
    """
    Dipole-dipole coupling between two transition dipoles (GHz).
    mu1, mu2 in Debye; r in nm; eps_r relative permittivity.
    """
    mu1 = mu1_debye * 3.33564e-30  # C m
    mu2 = mu2_debye * 3.33564e-30
    r = r_nm * 1e-9
    # Dipole-dipole interaction energy in Hz
    # V = (1/4π ε0 εr) * (μ1 μ2 / r^3) * (angular factor)
    h = 6.626e-34
    V_joules = (1 / (4 * math.pi * 8.854e-12 * eps_r)) * (mu1 * mu2 / r**3)
    # angular factor ~1 for aligned dipoles
    return V_joules / h / 1e9  # GHz

def exchange_coupling_estimate(overlap=0.1, orbital_energy=1e-19):
    """
    Crude estimate for exchange coupling J (GHz).
    overlap: dimensionless wavefunction overlap
    orbital_energy: relevant orbital energy scale (J)
    """
    J_joules = overlap * orbital_energy
    h = 6.626e-34
    return J_joules / h / 1e9

if __name__ == "__main__":
    # Test dipole-dipole: two 1 D dipoles 1 nm apart, eps=2
    print(dipole_dipole_coupling(1.0, 1.0, 1.0, 2.0), "GHz")
