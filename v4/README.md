# Quantum Materials SLM and Spin-Photon Coupling Screening

This repository contains the code, data, and report for an exploratory study on room-temperature spin-photon coupling in solid-state defects. The original aim was to build a small language model (SLM) for material science, but the project evolved into a physics-grounded screening pipeline using deterministic calculations, Gaussian Process regression, and a manually curated defect database.

## Key Findings

- Established a verified SOC-mediated baseline for room-temperature cooperativity: SnV⁻, PbV⁻, SiV⁻, GeV⁻ in diamond, and V_B⁻ in hBN, with C ≈ 0.12–0.23 at Q=10⁵.
- Screened four SOC-free mechanism classes and found none that currently beat the baseline.
- Discovered that zero-temperature DFT Debye-Waller factors systematically overestimate room-temperature viability; a temperature correction can lower cooperativity by nearly an order of magnitude.
- Identified a sharper search directive: inversion-symmetric sites with orbital degeneracy but SOC-free spin transitions, inspired by SiV⁻'s behavior.

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
