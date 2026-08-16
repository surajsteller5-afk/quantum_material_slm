import numpy as np
import matplotlib.pyplot as plt

def dw_from_mu(mu_debye, alpha=0.1):
    S = alpha * mu_debye**2
    return np.exp(-2.4 * S)

# Dipole range from 0.1 to 3 D
mu_range = np.linspace(0.1, 3, 200)

plt.figure(figsize=(8,5))
for alpha in [0.02, 0.05, 0.1, 0.2]:
    dw = dw_from_mu(mu_range, alpha)
    plt.plot(mu_range, dw, label=f'alpha={alpha}')

# SOC-free target region
plt.axhline(0.9, color='red', linestyle='--', label='DW=0.9 target')
plt.axvline(0.63, color='gray', linestyle=':', label='mu=0.63 D (alpha=0.1)')

plt.xlabel('Dipole moment (Debye)')
plt.ylabel('Debye-Waller factor at 300 K')
plt.title('DW–Dipole Trade-off (simple model)')
plt.legend()
plt.grid(True)
plt.savefig('dw_dipole_tradeoff.png')
print('Plot saved as dw_dipole_tradeoff.png')
