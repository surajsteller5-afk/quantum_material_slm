import json
import random
import os

def load_seed_defects(path="v4/database/defects_seed.json"):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = list(data.values())
    return data

def spin_to_str(spin):
    if spin == 0.5:
        return "S = 1/2"
    elif spin == 1:
        return "S = 1"
    elif spin == 1.5:
        return "S = 3/2"
    else:
        return f"S = {spin}"

def make_output_json(defect):
    out = {
        "host": defect["host"],
        "formula": defect["formula"],
        "defect": defect["defect"],
        "spin": defect["spin"],
        "spin_str": spin_to_str(defect["spin"]),
        "symmetry": defect["symmetry"],
        "zpl_nm": defect["zpl_nm"],
        "D_GHz": defect["D_GHz"],
        "dipole_D": defect["dipole_D"],
        "radiative_lifetime_ns": defect["radiative_lifetime_ns"],
        "T1_ms_300K": defect["T1_ms_300K"],
        "T2_ms_300K": defect["T2_ms_300K"],
        "cavity_Q": defect["cavity_Q"],
        "mode_volume_factor": defect["mode_volume_factor"],
        "source_doi": defect["source_doi"]
    }
    return json.dumps(out, indent=2)

def generate_paragraph(defect):
    spin = spin_to_str(defect["spin"])
    d_info = "no zero-field splitting" if defect["spin"] == 0.5 else f"zero-field splitting D = {defect['D_GHz']} GHz"
    return (
        f"In {defect['host']} ({defect['formula']}), the {defect['defect']} center exhibits "
        f"spin {spin} with {d_info}. "
        f"The zero-phonon line is at {defect['zpl_nm']} nm, and the radiative lifetime is "
        f"{defect['radiative_lifetime_ns']} ns. The transition dipole moment is {defect['dipole_D']} Debye. "
        f"At 300 K, T1 = {defect['T1_ms_300K']} ms and T2 = {defect['T2_ms_300K']} ms. "
        f"The host dielectric constant is {defect['eps_r']}, bandgap {defect['bandgap_eV']} eV. "
        f"Source: DOI {defect['source_doi']}."
    )

def generate_partial_paragraph(defect, fields_to_include):
    """Generate a paragraph containing only the specified fields."""
    parts = []
    if "host" in fields_to_include:
        parts.append(f"In {defect['host']} ({defect['formula']})")
    if "defect" in fields_to_include:
        parts.append(f"the {defect['defect']} center")
    if "spin" in fields_to_include:
        parts.append(f"has spin {spin_to_str(defect['spin'])}")
    if "zpl" in fields_to_include:
        parts.append(f"zero-phonon line at {defect['zpl_nm']} nm")
    if "dipole" in fields_to_include:
        parts.append(f"transition dipole moment {defect['dipole_D']} Debye")
    if "T2" in fields_to_include:
        parts.append(f"T2 at 300 K is {defect['T2_ms_300K']} ms")
    if "D" in fields_to_include:
        if defect["spin"] == 0.5:
            parts.append("no zero-field splitting")
        else:
            parts.append(f"zero-field splitting D = {defect['D_GHz']} GHz")
    if "radiative_lifetime" in fields_to_include:
        parts.append(f"radiative lifetime {defect['radiative_lifetime_ns']} ns")
    if "cavity_Q" in fields_to_include:
        parts.append(f"cavity quality factor {defect['cavity_Q']}")
    if "source_doi" in fields_to_include:
        parts.append(f"DOI: {defect['source_doi']}")
    # Join parts into a coherent sentence. If no parts, use a placeholder.
    text = ". ".join(parts) + "."
    return text

def make_partial_output(defect, fields_present):
    """Create output JSON with null for missing fields."""
    all_fields = [
        "host", "formula", "defect", "spin", "spin_str", "symmetry",
        "zpl_nm", "D_GHz", "dipole_D", "radiative_lifetime_ns",
        "T1_ms_300K", "T2_ms_300K", "cavity_Q", "mode_volume_factor", "source_doi"
    ]
    out = {}
    for f in all_fields:
        if f == "spin_str":
            out[f] = spin_to_str(defect["spin"]) if "spin" in fields_present else None
        elif f == "D_GHz":
            if defect["spin"] == 0.5:
                out[f] = 0.0
            else:
                out[f] = defect["D_GHz"] if "D" in fields_present else None
        elif f == "host":
            out[f] = defect["host"] if "host" in fields_present else None
        elif f == "formula":
            out[f] = defect["formula"] if "host" in fields_present else None  # formula often tied to host
        elif f == "defect":
            out[f] = defect["defect"] if "defect" in fields_present else None
        elif f == "spin":
            out[f] = defect["spin"] if "spin" in fields_present else None
        elif f == "symmetry":
            out[f] = defect["symmetry"] if "symmetry" in fields_present else None
        elif f == "zpl_nm":
            out[f] = defect["zpl_nm"] if "zpl" in fields_present else None
        elif f == "dipole_D":
            out[f] = defect["dipole_D"] if "dipole" in fields_present else None
        elif f == "radiative_lifetime_ns":
            out[f] = defect["radiative_lifetime_ns"] if "radiative_lifetime" in fields_present else None
        elif f == "T1_ms_300K":
            out[f] = defect["T1_ms_300K"] if "T1" in fields_present else None
        elif f == "T2_ms_300K":
            out[f] = defect["T2_ms_300K"] if "T2" in fields_present else None
        elif f == "cavity_Q":
            out[f] = defect["cavity_Q"] if "cavity_Q" in fields_present else None
        elif f == "mode_volume_factor":
            out[f] = defect["mode_volume_factor"] if "mode_volume_factor" in fields_present else None
        elif f == "source_doi":
            out[f] = defect["source_doi"] if "source_doi" in fields_present else None
        else:
            out[f] = None
    return json.dumps(out, indent=2)

def main():
    defects = load_seed_defects()
    if len(defects) < 5:
        print("Warning: few defects in seed.")

    dataset = []

    for defect in defects:
        # Complete text variants (as before)
        variants = [
            generate_paragraph(defect),
            f"Host: {defect['host']}\nFormula: {defect['formula']}\nDefect: {defect['defect']}\nSpin: {spin_to_str(defect['spin'])}\nZPL: {defect['zpl_nm']} nm\nD: {defect['D_GHz']} GHz\nDipole: {defect['dipole_D']} D\nT1@300K: {defect['T1_ms_300K']} ms\nT2@300K: {defect['T2_ms_300K']} ms\nDOI: {defect['source_doi']}",
            f"The {defect['defect']} defect in {defect['host']} has ZPL at {defect['zpl_nm']} nm, spin {spin_to_str(defect['spin'])}, and dipole moment {defect['dipole_D']} D. Its D parameter is {defect['D_GHz']} GHz (or zero if spin 1/2).",
        ]
        output_full = make_output_json(defect)

        for text in variants:
            user_content = (
                "Extract the quantum defect parameters from the following text.\n"
                "Return a valid JSON object with these keys:\n"
                "host, formula, defect, spin, spin_str, symmetry, zpl_nm, D_GHz, dipole_D, "
                "radiative_lifetime_ns, T1_ms_300K, T2_ms_300K, cavity_Q, mode_volume_factor, source_doi.\n"
                "If a value is not mentioned in the text, set it to null.\n\n"
                f"Text:\n{text}"
            )
            dataset.append({
                "messages": [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": output_full}
                ]
            })

        # Partial text variants (random subsets of fields)
        possible_fields = ["host", "defect", "spin", "zpl", "dipole", "T2", "D", "radiative_lifetime", "cavity_Q", "source_doi"]
        for _ in range(3):
            num_fields = random.randint(2, 5)
            fields_included = random.sample(possible_fields, num_fields)
            fields_included_set = set(fields_included)

            partial_text = generate_partial_paragraph(defect, fields_included_set)
            output_partial = make_partial_output(defect, fields_included_set)

            user_content = (
                "Extract the quantum defect parameters from the following text.\n"
                "Return a valid JSON object with these keys:\n"
                "host, formula, defect, spin, spin_str, symmetry, zpl_nm, D_GHz, dipole_D, "
                "radiative_lifetime_ns, T1_ms_300K, T2_ms_300K, cavity_Q, mode_volume_factor, source_doi.\n"
                "If a value is not mentioned in the text, set it to null.\n\n"
                f"Text:\n{partial_text}"
            )
            dataset.append({
                "messages": [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": output_partial}
                ]
            })

    random.shuffle(dataset)
    split_idx = int(0.9 * len(dataset))
    train = dataset[:split_idx]
    valid = dataset[split_idx:]

    os.makedirs("v4/mining/data_v2", exist_ok=True)
    with open("v4/mining/data_v2/train.jsonl", "w") as f:
        for entry in train:
            f.write(json.dumps(entry) + "\n")
    with open("v4/mining/data_v2/valid.jsonl", "w") as f:
        for entry in valid:
            f.write(json.dumps(entry) + "\n")

    print(f"Generated {len(train)} training and {len(valid)} validation mining examples (v2 with nulls).")

if __name__ == "__main__":
    main()