# Phase 18 residual information capacity

This directory freezes an open-vocabulary lossless residual-capacity estimator
and its known-content heavy-suspension positive control. Read
`RESIDUAL_CAPACITY_PREREGISTRATION.md` before running either corpus.

Build the aligned control:

```bash
python3 phase18_residual_capacity/build_lossy_renderer.py \
  --repo . --latinise latin14.txt --voynich voynich_phase15.json \
  --out lossy_renderer_phase18.json
```

Calibrate before opening Voynich VALIDATION:

```bash
python3 phase18_residual_capacity/residual_capacity.py calibrate-positive \
  --corpus lossy_renderer_phase18.json --label LATINISE_HEAVY_SUSPENSION \
  --out LOSSY_RENDERER_POSITIVE_RESULT_v1.json
```

Only if `positive_calibration_passed` is true:

```bash
python3 phase18_residual_capacity/residual_capacity.py analyze \
  --corpus voynich_phase15.json --label VOYNICH_VALIDATION \
  --out VOYNICH_RESIDUAL_CAPACITY_RESULT_v1.json
```

Apply the frozen decision rule:

```bash
python3 phase18_residual_capacity/evaluate_capacity.py \
  --positive LOSSY_RENDERER_POSITIVE_RESULT_v1.json \
  --voynich VOYNICH_RESIDUAL_CAPACITY_RESULT_v1.json \
  --out RESIDUAL_CAPACITY_DECISION_v1.json
```

Run deterministic tests from this directory with
`python3 test_residual_capacity.py` and `python3 test_phase18_decision.py`.

The result is a bandwidth upper bound, not a decipherment or hypothesis-ranking
claim. All final-test partitions remain sealed.
