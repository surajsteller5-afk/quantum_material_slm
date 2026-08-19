# Direction B Hybrid Database Schema

## Important Temperature Rule
We do not restrict strictly to 300 K. We accept near-room-temperature values (200 K–350 K)
and record the measurement temperature explicitly for every parameter.

## Spin Center Fields
- host
- formula
- defect
- spin
- symmetry
- soc_constant_meV
- T1_ms
- T1_temp_K
- T2_ms
- T2_temp_K
- source_doi

## Optical Antenna Fields
- host
- formula
- defect
- spin (if any)
- symmetry
- zpl_nm
- dw_factor
- dw_temp_K
- gamma_hom_Hz
- gamma_temp_K
- dipole_D
- source_doi

## Hybrid Pair Fields
- spin_center_id
- antenna_id
- pair_distance_nm
- exchange_coupling_GHz
- dipole_dipole_coupling_GHz
- estimated_total_coupling_GHz
- coupling_temp_K
- source_doi (if proposed)
