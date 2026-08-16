import json
import math
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel as C
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
import sys
sys.path.append('v4/physics')
from quantum_params import compute_g0, compute_kappa, compute_cooperativity

# ------------------------- Database -------------------------
def load_defects(path="v4/database/defects_seed.json"):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = list(data.values())
    return data

def prepare_features(defects):
    hosts = sorted(set(d["host"] for d in defects))
    symms = sorted(set(d["symmetry"] for d in defects))
    X, y_zpl, y_dipole = [], [], []
    for d in defects:
        feat = []
        for h in hosts:
            feat.append(1.0 if d["host"] == h else 0.0)
        feat.append(d["spin"])
        for s in symms:
            feat.append(1.0 if d["symmetry"] == s else 0.0)
        feat.append(d["bandgap_eV"])
        feat.append(d["eps_r"])
        X.append(feat)
        y_zpl.append(d["zpl_nm"])
        y_dipole.append(d["dipole_D"])
    return np.array(X), np.array(y_zpl), np.array(y_dipole), hosts, symms

# ------------------------- GP Training -------------------------
def train_gp(X, y):
    scaler_X = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    scaler_y = StandardScaler()
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()

    kernel = C(1.0) * Matern(length_scale=1.0, nu=2.5)

    gp = GaussianProcessRegressor(kernel=kernel, optimizer=None, normalize_y=False, alpha=1e-6)
    gp.fit(X_scaled, y_scaled)
    return gp, scaler_X, scaler_y

# ------------------------- Prediction -------------------------
def predict_new_defect(features_dict, gp_zpl, gp_dipole, scaler_X, scaler_y_zpl, scaler_y_dipole, hosts, symms):
    feat = []
    for h in hosts:
        feat.append(1.0 if features_dict.get("host") == h else 0.0)
    feat.append(features_dict["spin"])
    for s in symms:
        feat.append(1.0 if features_dict.get("symmetry") == s else 0.0)
    feat.append(features_dict["bandgap_eV"])
    feat.append(features_dict["eps_r"])
    X_new = np.array(feat).reshape(1, -1)
    X_new_scaled = scaler_X.transform(X_new)

    zpl_mean_scaled, zpl_std_scaled = gp_zpl.predict(X_new_scaled, return_std=True)
    dip_mean_scaled, dip_std_scaled = gp_dipole.predict(X_new_scaled, return_std=True)

    zpl_scaled = float(zpl_mean_scaled[0])
    dip_scaled = float(dip_mean_scaled[0])
    zpl_std_scaled = float(zpl_std_scaled[0])
    dip_std_scaled = float(dip_std_scaled[0])

    zpl = scaler_y_zpl.inverse_transform([[zpl_scaled]])[0][0]
    dip = scaler_y_dipole.inverse_transform([[dip_scaled]])[0][0]
    zpl_std = zpl_std_scaled * scaler_y_zpl.scale_[0]
    dip_std = dip_std_scaled * scaler_y_dipole.scale_[0]
    return zpl, zpl_std, dip, dip_std

# ------------------------- Nearest Neighbor -------------------------
def nearest_neighbor(features_dict, defects, threshold=1.0):
    X_all, _, _, hosts, symms = prepare_features(defects)
    scaler = StandardScaler().fit(X_all)
    X_all_scaled = scaler.transform(X_all)

    feat = []
    for h in hosts:
        feat.append(1.0 if features_dict.get("host") == h else 0.0)
    feat.append(features_dict["spin"])
    for s in symms:
        feat.append(1.0 if features_dict.get("symmetry") == s else 0.0)
    feat.append(features_dict["bandgap_eV"])
    feat.append(features_dict["eps_r"])
    X_new = np.array(feat).reshape(1, -1)
    X_new_scaled = scaler.transform(X_new)

    dists = cdist(X_new_scaled, X_all_scaled, metric='euclidean').flatten()
    min_idx = np.argmin(dists)
    min_dist = dists[min_idx]
    if min_dist > threshold:
        return None, min_dist
    else:
        return defects[min_idx], min_dist

# ------------------------- LOOCV -------------------------
def loocv_evaluate(defects):
    X, y_zpl, y_dipole, hosts, symms = prepare_features(defects)
    errors_zpl = []
    errors_dipole = []
    for i in range(len(defects)):
        X_train = np.delete(X, i, axis=0)
        y_train_zpl = np.delete(y_zpl, i)
        y_train_dip = np.delete(y_dipole, i)
        X_test = X[i:i+1]
        y_test_zpl = y_zpl[i]
        y_test_dip = y_dipole[i]

        gp_zpl, sc_X, sc_y = train_gp(X_train, y_train_zpl)
        gp_dip, _, sc_y_d = train_gp(X_train, y_train_dip)

        # Need to use the same scalers fitted on training data
        X_train_scaled = sc_X.transform(X_train)
        X_test_scaled = sc_X.transform(X_test)
        zpl_pred_scaled, _ = gp_zpl.predict(X_test_scaled, return_std=True)
        dip_pred_scaled, _ = gp_dip.predict(X_test_scaled, return_std=True)
        zpl_pred = sc_y.inverse_transform([[float(zpl_pred_scaled[0])]])[0][0]
        dip_pred = sc_y_d.inverse_transform([[float(dip_pred_scaled[0])]])[0][0]
        errors_zpl.append(abs(zpl_pred - y_test_zpl))
        errors_dipole.append(abs(dip_pred - y_test_dip))

    return np.mean(errors_zpl), np.mean(errors_dipole)

# ------------------------- Main -------------------------
if __name__ == "__main__":
    defects = load_defects()
    if len(defects) < 5:
        print("Too few defects!"); sys.exit(1)

    X, y_zpl, y_dipole, hosts, symms = prepare_features(defects)
    gp_zpl, scaler_X, scaler_y_zpl = train_gp(X, y_zpl)
    gp_dipole, _, scaler_y_dipole = train_gp(X, y_dipole)

    print(f"Database size: {len(defects)} defects")
    print("Leave-one-out cross-validation (GP):")
    mae_zpl, mae_dip = loocv_evaluate(defects)
    print(f"  MAE ZPL: {mae_zpl:.1f} nm")
    print(f"  MAE dipole: {mae_dip:.2f} Debye")

    # Test with a training duplicate (should give near-zero std)
    print("\nTesting GP on a training point (Xe-related center):")
    xe_defect = next(d for d in defects if d["defect"] == "Xe-related center")
    test_features = {
        "host": xe_defect["host"],
        "spin": xe_defect["spin"],
        "symmetry": xe_defect["symmetry"],
        "bandgap_eV": xe_defect["bandgap_eV"],
        "eps_r": xe_defect["eps_r"]
    }
    zpl, zpl_std, dip, dip_std = predict_new_defect(
        test_features, gp_zpl, gp_dipole, scaler_X, scaler_y_zpl, scaler_y_dipole, hosts, symms)
    print(f"  Predicted ZPL: {zpl:.1f} ± {zpl_std:.1f} nm")
    print(f"  Predicted dipole: {dip:.2f} ± {dip_std:.2f} Debye")
    print("  (Expected: std near 0 if calibration correct)")

    # Test on a novel defect (Diamond, spin=1, D3d)
    print("\nTesting on novel defect (Diamond, spin=1, D3d):")
    new_defect = {
    "host": "Diamond",
    "spin": 1,
    "symmetry": "C3v",
    "bandgap_eV": 5.47,
    "eps_r": 5.7
    }
    zpl, zpl_std, dip, dip_std = predict_new_defect(
        new_defect, gp_zpl, gp_dipole, scaler_X, scaler_y_zpl, scaler_y_dipole, hosts, symms)
    print(f"  Predicted ZPL: {zpl:.1f} ± {zpl_std:.1f} nm")
    print(f"  Predicted dipole: {dip:.2f} ± {dip_std:.2f} Debye")

    # Nearest neighbor and cooperativity
    nn, dist = nearest_neighbor(new_defect, defects, threshold=1.0)
    if nn:
        print(f"  Nearest neighbor: {nn['defect']} (distance {dist:.2f})")
        dw = nn.get("dw_factor_300K")
        gamma = nn.get("gamma_hom_300K_Hz")
        if dw is None or gamma is None:
            print("  Warning: DW factor or gamma missing for nearest neighbor. Using conservative defaults (DW=0.1, gamma=1e12 Hz).")
            dw = 0.1 if dw is None else dw
            gamma = 1e12 if gamma is None else gamma
        else:
            print(f"  Using neighbor's DW={dw}, gamma={gamma:.2e} Hz")
        eps_r = nn.get("eps_r", 5.7)
        v_m_factor = 1.0
        g0_ghz = compute_g0(zpl, dip, eps_r, v_m_factor)
        kappa = compute_kappa(zpl, nn.get("cavity_Q", 10000))
        C = compute_cooperativity(g0_ghz, dw, gamma, kappa)
        print(f"  Computed g0: {g0_ghz:.2f} GHz")
        print(f"  Cavity κ: {kappa:.2e} Hz")
        print(f"  Cooperativity C: {C:.3f}")
        if C > 1:
            print("  → Strong coupling regime at RT (C > 1)")
        elif C > 0.1:
            print("  → Moderate Purcell enhancement (C > 0.1)")
        else:
            print("  → Poor RT coupling (C < 0.1)")
    else:
        print(f"  No close physical neighbor found (distance {dist:.2f}). Cannot estimate DW/gamma; cannot compute C.")