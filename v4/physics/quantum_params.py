import math

# Fundamental constants
HBAR = 1.0545718e-34
C = 299792458
EPSILON_0 = 8.8541878e-12
DEBYE_TO_CM = 3.33564e-30
GHZ_CONV = 1e9

def compute_g0(zpl_nm, dipole_debye, eps_r, v_m_factor):
    """Compute vacuum Rabi coupling g0 in GHz."""
    zpl_m = zpl_nm * 1e-9
    dipole_cm = dipole_debye * DEBYE_TO_CM
    n_refractive = math.sqrt(eps_r)
    v_m = v_m_factor * (zpl_m / n_refractive)**3
    omega_c = 2 * math.pi * C / zpl_m
    term1 = dipole_cm / HBAR
    term2 = math.sqrt((HBAR * omega_c) / (2 * EPSILON_0 * eps_r * v_m))
    return ((term1 * term2) / (2 * math.pi)) / GHZ_CONV

def get_D_string(spin, D_GHz=None):
    """Return D string based on spin (0.5 = 1/2, 1 = 1, 1.5 = 3/2)."""
    if spin == 0.5:
        return "N/A (S=1/2 implies D=0)"
    elif spin >= 1 and D_GHz is not None:
        return f"{D_GHz} GHz"
    else:
        raise ValueError("D_GHz required for spin >= 1")

def compute_kappa(zpl_nm, cavity_Q):
    """Cavity decay rate kappa = omega_c / Q, in Hz."""
    omega_c = 2 * math.pi * C / (zpl_nm * 1e-9)
    return omega_c / cavity_Q

def compute_cooperativity(g0_ghz, dw_factor, gamma_hz, kappa_hz):
    """
    Cooperativity C = g_eff^2 / (kappa * gamma)
    g_eff = g0 * sqrt(dw_factor)
    g0_ghz: vacuum Rabi coupling in GHz
    dw_factor: Debye-Waller factor (0-1)
    gamma_hz: homogeneous linewidth in Hz
    kappa_hz: cavity decay rate in Hz
    """
    g0_hz = g0_ghz * 1e9
    g_eff = g0_hz * math.sqrt(dw_factor)
    return (g_eff**2) / (kappa_hz * gamma_hz)
