# Direction B Finding: Exchange-Coupled Hybrid Requires Sub-nm Separation

**Date:** 2026-08-19  
**Author:** Suraj K.C.

---

## 1. Model

We consider a three-node system:

- Optical cavity (decay rate \(\kappa\))
- Optical antenna (bright, high Debye-Waller factor, strong dipole)
- Spin center (long \(T_2\), weak optical coupling)

The antenna couples to the cavity with rate \(g_0\). The spin couples to the antenna with interaction strength \(J\). The spin does not directly couple to the cavity.

---

## 2. Coupled-System Regimes

### Regime A: Dispersive (spin and antenna detuned by \(\Delta\))

Effective spin–photon coupling:

\[
g_{\text{eff}} \approx \frac{g_0 J}{\Delta}
\]

Cooperativity:

\[
C \approx \frac{(g_0 J / \Delta)^2}{\kappa \gamma_{\text{spin}}}
\]

Since \(J / \Delta \ll 1\), this regime gives weak coupling unless \(g_0\) is enormous.

### Regime B: Resonant Hybrid (spin and antenna near-degenerate)

If \(J\) is strong enough to mix spin and antenna states, the spin effectively inherits the antenna’s cavity coupling. Then:

\[
g_{\text{eff}} \approx J
\]

and

\[
C \approx \frac{J^2}{\kappa \gamma_{\text{spin}}}
\]

This is the regime our sensitivity analysis assumed.

---

## 3. Sensitivity Threshold

Using NV⁻ as spin center (\(T_2 = 1.8\) ms) and SiV⁻ as antenna (\(\kappa \approx 25.5\) GHz, \(\gamma_{\text{spin}} \approx 0.556\) kHz):

\[
C = \frac{J^2}{\kappa \gamma}
\]

Strong coupling (\(C > 1\)) requires:

\[
J > \sqrt{\kappa \gamma}
\]

\[
J > \sqrt{(25.5\times 10^9)(0.556\times 10^3)} \approx 3.77 \text{ MHz}
\]

Our numerical sweep gave **\(J \ge 5\) MHz** for strong coupling.

---

## 4. What Provides \(J \ge 5\) MHz?

### Exchange Coupling

- Requires wavefunction overlap.
- Typical for adjacent defect pairs (1–2 nm).
- Known values: 10–100 MHz for NV-P1 pairs, up to GHz for NV-NV at sub-nm.
- Feasible but requires **sub-nm to 1 nm separation**.

### Dipole-Dipole Coupling

- No wavefunction overlap required.
- For electron spins, typical values at 2–5 nm: **kHz to low MHz**.
- **Below the 5 MHz threshold.**
- Insufficient for strong coupling in this architecture.

**Conclusion:** Exchange coupling is required. Dipole-dipole is too weak.

---

## 5. Consequences

- The hybrid architecture must use **adjacent defect pairs** with direct electronic overlap.
- Fabrication of two different defect species at sub-nm separation is **beyond current deterministic implantation capability**.
- Placing a second defect so close may **break the symmetry protection** of the antenna, destroying its high Debye-Waller factor.

This is a **fabrication feasibility problem**, not just a literature search problem.

---

## 6. Revised Search Strategy

Focus on:

- Accidentally-formed close pairs in high-density samples.
- Exchange-coupled defect pairs in diamond, SiC, hBN.
- Theoretical proposals for hybrid spin-antenna pairs with wavefunction overlap.

Suggested queries:

- "exchange coupled defect pair quantum interface diamond"
- "adjacent donor-acceptor pair silicon carbide exchange"
- "NV-P1 exchange coupling GHz"
- "deterministic defect pair implantation nanoscale"

---

## 7. Status

Direction B is **not ruled out**, but it depends on either:

1. A fabrication breakthrough for deterministic sub-nm defect pair placement, or
2. Discovery of naturally occurring close pairs with preserved symmetry.

The next step is a targeted search for evidence of either.