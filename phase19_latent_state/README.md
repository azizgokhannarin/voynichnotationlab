# Phase 19 small latent-state test

This directory implements a preregistered binary line-state HMM and its
parameter-matched zero-state procedural calibration. Read
`LATENT_STATE_PREREGISTRATION.md` before running it.

Calibrate without scoring real Voynich VALIDATION tokens:

```bash
python3 phase19_latent_state/latent_state.py calibrate \
  --corpus voynich_phase15.json \
  --out LATENT_STATE_CALIBRATION_v1.json
```

Only if `calibration_passed` is true:

```bash
python3 phase19_latent_state/latent_state.py analyze \
  --corpus voynich_phase15.json \
  --calibration LATENT_STATE_CALIBRATION_v1.json \
  --out VOYNICH_LATENT_STATE_RESULT_v1.json
```

Verify both embedded hashes and apply the frozen decision rule:

```bash
python3 phase19_latent_state/evaluate_latent_state.py \
  --calibration LATENT_STATE_CALIBRATION_v1.json \
  --result VOYNICH_LATENT_STATE_RESULT_v1.json \
  --out LATENT_STATE_DECISION_v1.json
```

Run `python3 test_latent_state.py` from this directory for deterministic fixture
tests, plus `python3 test_phase19_decision.py` for the evaluator. The result
cannot by itself identify linguistic content, structured data or autonomous
generation. Final-test partitions remain sealed. See `CLI_OUTPUT_ERRATUM.md`
for the terminal-summary-only hash-label issue in the frozen analyze command.
