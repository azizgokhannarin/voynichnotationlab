# Phase 16 exact-identity recurrence/burstiness

This directory contains the frozen, executable raw-token instrument introduced
after the v4.4.1 full-size diplomatic-control checkpoint.

## Run

Build the three canonical Phase-15 line corpora as documented in
`../phase15_instrument_calibration/README.md`. Then run:

```bash
python3 phase16_raw_token_recurrence/raw_token_recurrence.py calibrate \
  --out synthetic_calibration.json

python3 phase16_raw_token_recurrence/raw_token_recurrence.py analyze \
  --corpus renderer_phase15.json --label strong_renderer \
  --out strong_renderer_recurrence.json

python3 phase16_raw_token_recurrence/raw_token_recurrence.py analyze \
  --corpus cremma_phase15.json --label cremma \
  --out cremma_recurrence.json

python3 phase16_raw_token_recurrence/raw_token_recurrence.py analyze \
  --corpus voynich_phase15.json --label voynich_validation \
  --out voynich_recurrence.json
```

Run deterministic fixtures:

```bash
cd phase16_raw_token_recurrence
python3 test_raw_token_recurrence.py
```

External source payloads and generated canonical corpora are intentionally not
vendored. Their frozen hashes are inherited from Phase 15 and repeated in the
Phase-16 source/result manifest.

