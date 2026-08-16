from mlx_lm import load, generate

model, tokenizer = load(
    "mlx-community/Llama-3.2-1B-Instruct-4bit",
    adapter_path="./adapters_mining_v2"
)

sample_text = (
    "The germanium vacancy in diamond has a zero-phonon line at 602 nm "
    "and ground state spin S = 1/2. Its transition dipole moment is 1.9 Debye."
)

prompt_text = (
    "Extract the quantum defect parameters from the following text.\n"
    "Return a valid JSON object with these keys:\n"
    "host, formula, defect, spin, spin_str, symmetry, zpl_nm, D_GHz, dipole_D, "
    "radiative_lifetime_ns, T1_ms_300K, T2_ms_300K, cavity_Q, mode_volume_factor, source_doi.\n"
    "If a value is not mentioned in the text, set it to null.\n\n"
    f"Text:\n{sample_text}"
)

prompt = tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt_text}],
    tokenize=False,
    add_generation_prompt=True
)

output = generate(model, tokenizer, prompt=prompt, max_tokens=300)
print(output)