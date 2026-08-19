import math

# Antenna: SiV- (best RT optical interface)
g0_ghz = 8.61
kappa_ghz = 25.52
dw = 0.65
gamma_spin_hz = 1.0 / (1.8e-3)  # from NV- T2=1.8 ms
gamma_spin_ghz = gamma_spin_hz / 1e9

# Exchange J from NV-P1 measured range
J_values_mhz = [50, 100, 200, 500, 1000]

print("Direction B final physics check")
print(f"Antenna: SiV- (g0={g0_ghz} GHz, κ={kappa_ghz} GHz, DW={dw})")
print(f"Spin proxy: T2=1.8 ms, γ={gamma_spin_hz:.3e} Hz")
print()

print(f"{'J (MHz)':<10} {'g_eff (GHz)':<12} {'C_eff':<12} {'Regime'}")
print("-" * 50)
for J_mhz in J_values_mhz:
    J_ghz = J_mhz / 1e3
    # Corrected effective coupling from three-node simulation: g_eff ≈ 0.1 J
    g_eff = 0.1 * J_ghz
    C = (g_eff**2) / (kappa_ghz * gamma_spin_ghz)
    regime = "strong" if C > 1 else ("moderate" if C > 0.1 else "weak")
    print(f"{J_mhz:<10} {g_eff:<12.4f} {C:<12.4f} {regime}")
