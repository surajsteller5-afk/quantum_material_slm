cat > README.md << 'EOF'
# Quantum Materials SLM and Spin-Photon Coupling Screening

This is an exploratory, self-directed computational screening study. It is not a lab measurement and has not been peer-reviewed.

The original aim was to build a small language model (SLM) for material science, but the project evolved into a physics-grounded screening pipeline using deterministic calculations, Gaussian Process regression, and a manually curated defect database.

## Key Findings

- Established a verified SOC-mediated baseline for room-temperature cooperativity: SnV⁻, PbV⁻, SiV⁻, GeV⁻ in diamond, and V_B⁻ in hBN, with C ≈ 0.12–0.23 at Q=10⁵.
- Screened four SOC-free mechanism classes and found none that currently beat the baseline.
- Discovered that zero-temperature DFT Debye-Waller factors systematically overestimate room-temperature viability; a temperature correction can lower cooperativity by nearly an order of magnitude.
- Identified a sharper search directive: inversion-symmetric sites with orbital degeneracy but SOC-free spin transitions, inspired by SiV⁻'s behavior.

## Full Report

The complete technical report is available at: [v4/final_report.md](v4/final_report.md)

## Directory Structure

- `v4/database/defects_seed.json`: curated database of 35 defects with physical parameters.
- `v4/models/`: ranking and GP regression scripts.
- `v4/physics/`: deterministic calculators for g0, kappa, cooperativity, and QuTiP simulation.
- `v4/final_report.md`: consolidated technical report.

## Reproduction

1. Create a Python virtual environment.
2. Install dependencies: `pip install numpy scipy scikit-learn matplotlib qutip`
3. Run ranking: `python3 v4/models/rank_defects_grid.py`
4. Run report scripts as needed.

## Status

This project is archived as an internal study. Before any public release, a human verification pass is required to confirm all literature values and conventions.

## License

MIT License. See [LICENSE](LICENSE).
EOF

## Direction B: Exchange-Coupled Hybrid Architecture

We also evaluated a two-site hybrid approach: a bright optical antenna (e.g., SiV⁻) exchange-coupled to a long-lived spin center.

- Strong coupling is predicted for exchange J ≥ 50 MHz.
- This is physically plausible and has precedent in NV⁻–P1 pairs.
- However, deterministic fabrication of such pairs is 30–50× beyond current capability.

See `v5/` for the full investigation.

## Final Summary

This project began as an attempt to use a small language model (SLM) for quantum parameter prediction. It failed—but the process led to a physics-grounded screening pipeline that produced real, verifiable results.

### Key Findings

1. **LLMs are not suitable for numerical quantum physics.** Deterministic formulas, Gaussian Process regression, and a curated database are the right tools.

2. **Room-temperature spin-photon coupling is governed by Debye-Waller factor and linewidth, not just coupling strength.**

3. **Zero-temperature DFT Debye-Waller factors systematically overestimate room-temperature viability.** This is a transferable methodological warning for the field.

4. **Single-defect SOC-free coupling is unlikely** due to a DW–dipole trade-off.

5. **Hybrid exchange-coupled architectures are physically possible**—strong coupling requires \(J \ge 50\) MHz, which exists in NV⁻–P1 pairs—but **no material platform currently satisfies all requirements**. Silicon lacks an RT antenna; diamond requires impossible fabrication precision.

### What This Project Demonstrated

A complete, honest scientific workflow:
- Built a screening pipeline.
- Verified sources and caught errors.
- Ran simulations to test assumptions.
- Revised conclusions when models contradicted heuristics.
- Documented negative results as boundaries, not failures.

### Repository Contents

- `v4/` – Single-defect screening pipeline, SOC-free analysis, Debye-Waller correction.
- `v5/` – Direction B hybrid architecture investigation, platform gap analysis, exchange coupling model.

### Status

Archived as a complete internal study. Human verification pending for public release.
