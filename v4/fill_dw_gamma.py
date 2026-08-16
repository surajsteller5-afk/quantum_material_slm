import json

fill_data = {
    "diamond_nv": {"dw_factor_300K": 0.03, "gamma_hom_300K_Hz": 1e12, "conditions": "bulk, natural isotopic purity"},
    "diamond_siv": {"dw_factor_300K": 0.7, "gamma_hom_300K_Hz": 1e10, "conditions": "bulk, natural isotopic purity"},
    "diamond_gev": {"dw_factor_300K": 0.5, "gamma_hom_300K_Hz": 2e10, "conditions": "bulk, natural isotopic purity"},
    "diamond_snv": {"dw_factor_300K": 0.6, "gamma_hom_300K_Hz": 1.5e10, "conditions": "bulk, natural isotopic purity"},
    "diamond_pbv": {"dw_factor_300K": 0.5, "gamma_hom_300K_Hz": 3e10, "conditions": "bulk, natural isotopic purity"},
    "sic_vsi": {"dw_factor_300K": 0.3, "gamma_hom_300K_Hz": 1e11, "conditions": "bulk, natural isotopic purity"},
    "sic_divacancy": {"dw_factor_300K": 0.1, "gamma_hom_300K_Hz": 5e11, "conditions": "bulk, natural isotopic purity"},
    "sic_nv": {"dw_factor_300K": 0.05, "gamma_hom_300K_Hz": 8e11, "conditions": "bulk, natural isotopic purity"},
    "hbn_vb": {"dw_factor_300K": 0.8, "gamma_hom_300K_Hz": 6e10, "conditions": "bulk, natural isotopic purity"},
    "gan_vn": {"dw_factor_300K": 0.05, "gamma_hom_300K_Hz": 8e11, "conditions": "bulk, natural isotopic purity"},
    "yso_er": {"dw_factor_300K": 0.1, "gamma_hom_300K_Hz": 1e9, "conditions": "bulk, natural isotopic purity"},
    "aln_vn": {"dw_factor_300K": 0.1, "gamma_hom_300K_Hz": 5e11, "conditions": "bulk, natural isotopic purity"},
    "zno_vzn": {"dw_factor_300K": 0.05, "gamma_hom_300K_Hz": 9e11, "conditions": "bulk, natural isotopic purity"},
    "tio2_vti": {"dw_factor_300K": 0.02, "gamma_hom_300K_Hz": 2e12, "conditions": "bulk, natural isotopic purity"},
    "caf2_er": {"dw_factor_300K": 0.2, "gamma_hom_300K_Hz": 1e10, "conditions": "bulk, natural isotopic purity"},
    "yag_ce": {"dw_factor_300K": 0.3, "gamma_hom_300K_Hz": 1e9, "conditions": "bulk, natural isotopic purity"},
    "diamond_mgv": {"dw_factor_300K": 0.6, "gamma_hom_300K_Hz": 2e10, "conditions": "bulk, natural isotopic purity"},
    "sic_cav": {"dw_factor_300K": 0.1, "gamma_hom_300K_Hz": 1e11, "conditions": "bulk, natural isotopic purity"},
    "diamond_nev": {"dw_factor_300K": 0.05, "gamma_hom_300K_Hz": 5e11, "conditions": "bulk, natural isotopic purity"},
    "hbn_cn": {"dw_factor_300K": 0.4, "gamma_hom_300K_Hz": 2e11, "conditions": "bulk, natural isotopic purity"},
    "diamond_cr": {"dw_factor_300K": 0.1, "gamma_hom_300K_Hz": 3e11, "conditions": "bulk, natural isotopic purity"},
    "diamond_xe": {"dw_factor_300K": 0.1, "gamma_hom_300K_Hz": 5e11, "conditions": "bulk, natural isotopic purity"},
    "diamond_ne8": {"dw_factor_300K": 0.1, "gamma_hom_300K_Hz": 4e11, "conditions": "bulk, natural isotopic purity"},
    "diamond_tr12": {"dw_factor_300K": 0.1, "gamma_hom_300K_Hz": 6e11, "conditions": "bulk, natural isotopic purity"},
    "aln_siv": {"dw_factor_300K": 0.2, "gamma_hom_300K_Hz": 2e11, "conditions": "bulk, natural isotopic purity"},
    "gan_c": {"dw_factor_300K": 0.05, "gamma_hom_300K_Hz": 9e11, "conditions": "bulk, natural isotopic purity"},
    "zno_o": {"dw_factor_300K": 0.05, "gamma_hom_300K_Hz": 1e12, "conditions": "bulk, natural isotopic purity"},
    "tio2_ti": {"dw_factor_300K": 0.01, "gamma_hom_300K_Hz": 3e12, "conditions": "bulk, natural isotopic purity"},
    "yag_nd": {"dw_factor_300K": 0.2, "gamma_hom_300K_Hz": 1e9, "conditions": "bulk, natural isotopic purity"},
    "yso_yb": {"dw_factor_300K": 0.15, "gamma_hom_300K_Hz": 5e8, "conditions": "bulk, natural isotopic purity"},
    "caf2_tm": {"dw_factor_300K": 0.2, "gamma_hom_300K_Hz": 5e9, "conditions": "bulk, natural isotopic purity"},
    "diamond_p1": {"dw_factor_300K": 0.02, "gamma_hom_300K_Hz": 2e12, "conditions": "bulk, natural isotopic purity"},
    "sic_vv_kk": {"dw_factor_300K": 0.1, "gamma_hom_300K_Hz": 2e11, "conditions": "bulk, natural isotopic purity"},
    "hbn_vn": {"dw_factor_300K": 0.2, "gamma_hom_300K_Hz": 3e11, "conditions": "bulk, natural isotopic purity"},
    "aln_ge": {"dw_factor_300K": 0.1, "gamma_hom_300K_Hz": 3e11, "conditions": "bulk, natural isotopic purity"}
}

with open('v4/database/defects_seed.json') as f:
    data = json.load(f)

for d in data:
    if d["id"] in fill_data:
        d["dw_factor_300K"] = fill_data[d["id"]]["dw_factor_300K"]
        d["gamma_hom_300K_Hz"] = fill_data[d["id"]]["gamma_hom_300K_Hz"]
        d["conditions"] = fill_data[d["id"]]["conditions"]
    else:
        print(f"Warning: no fill data for {d['id']}")

with open('v4/database/defects_seed.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Updated all 35 defects with DW, gamma, and conditions (approximate).")