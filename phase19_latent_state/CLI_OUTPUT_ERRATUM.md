# Phase 19 CLI summary erratum

The frozen `latent_state.py analyze` command writes the correct
`result_sha256` inside `VOYNICH_LATENT_STATE_RESULT_v1.json`, but its terminal
summary selects `calibration_sha256` first and therefore prints the calibration
hash under the generic `sha256` label.

This affects only the human-readable terminal summary. The result payload,
embedded result hash, evaluator and source/result manifest use the correct
result hash. The preregistered instrument code is preserved byte-for-byte rather
than modified after results were observed.

