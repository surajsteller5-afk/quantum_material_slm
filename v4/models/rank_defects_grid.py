import json
import sys
sys.path.append('v4/physics')
from quantum_params import compute_g0, compute_kappa, compute_cooperativity

REFERENCE_V_M_FACTOR = 0.1
Q_VALUES = [1e4, 1e5, 1e6]

def load_defects(path="v4/database/defects_seed.json"):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = list(data.values())
    return data

def main():
    defects = load_defects()
    valid_defects = [d for d in defects if d.get("dw_gamma_provenance") != "placeholder"]
    if not valid_defects:
        print("No non-placeholder defects. Update provenance first.")
        return

    for Q in Q_VALUES:
        print(f"\n=== Reference cavity Q = {Q:.0e}, Vm factor = {REFERENCE_V_M_FACTOR} ===\n")
        results = []
        for d in valid_defects:
            zpl = d["zpl_nm"]
            dipole = d["dipole_D"]
            eps_r = d["eps_r"]
            dw = d["dw_factor_300K"]
            gamma = d["gamma_hom_300K_Hz"]
            g0_ghz = compute_g0(zpl, dipole, eps_r, REFERENCE_V_M_FACTOR)
            kappa = compute_kappa(zpl, Q)
            C = compute_cooperativity(g0_ghz, dw, gamma, kappa)
            results.append({
                "defect": d["defect"],
                "host": d["host"],
                "zpl_nm": zpl,
                "dw": dw,
                "gamma_Hz": gamma,
                "g0_GHz": g0_ghz,
                "kappa_Hz": kappa,
                "C": C,
                "provenance": d["dw_gamma_provenance"]
            })
        results.sort(key=lambda x: x["C"], reverse=True)
        print(f"{'Defect':<20} {'Host':<12} {'ZPL':<8} {'DW':<6} {'gamma':<12} {'g0':<8} {'C':<12} {'Provenance'}")
        print("-" * 90)
        for r in results:
            print(f"{r['defect']:<20} {r['host']:<12} {r['zpl_nm']:<8} {r['dw']:<6.2f} {r['gamma_Hz']:<12.1e} {r['g0_GHz']:<8.2f} {r['C']:<12.4f} {r['provenance']}")
        strong = [r for r in results if r["C"] > 1]
        moderate = [r for r in results if 0.1 < r["C"] <= 1]
        print(f"\nStrong (C>1): {len(strong)}  Moderate (0.1<C<1): {len(moderate)}")
        for r in strong:
            print(f"  Strong: {r['defect']} ({r['host']}): C={r['C']:.3f}")
        for r in moderate:
            print(f"  Moderate: {r['defect']} ({r['host']}): C={r['C']:.3f}")

if __name__ == "__main__":
    main()
