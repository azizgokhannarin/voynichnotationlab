# Phase 17 structured-data controls

This directory calibrates the frozen Phase-16 exact-identity instrument on two
real non-linguistic structured datasets and five preregistered surface encodings.

External source payloads and generated canonical corpora are not vendored. See
`SOURCE_PROVENANCE_v1.json` and `STRUCTURED_DATA_PREREGISTRATION.md` for exact
hashes, parsing rules, geometry matching and decision gates.

Build all five canonical controls:

```bash
python3 phase17_structured_data_controls/build_structured_controls.py \
  --instrument phase16_raw_token_recurrence/raw_token_recurrence.py \
  --voynich voynich_phase15.json \
  --retail "Online Retail.xlsx" \
  --mushroom agaricus-lepiota.data \
  --out-dir phase17-derived
```

Run each generated corpus with the unchanged Phase-16 `analyze` command and
2,000 default permutations. Then apply the preregistered decision rule:

```bash
python3 phase17_structured_data_controls/evaluate_structured_controls.py \
  --result RETAIL_TALLY_ORDERED_RESULT_v1.json \
  --result RETAIL_TALLY_UNORDERED_RESULT_v1.json \
  --result MUSHROOM_RAW_ORDERED_RESULT_v1.json \
  --result MUSHROOM_RAW_PERMUTED_RESULT_v1.json \
  --result MUSHROOM_QUALIFIED_ORDERED_RESULT_v1.json \
  --out STRUCTURED_DATA_CONTROL_DECISION_v1.json
```

Run deterministic tests:

```bash
cd phase17_structured_data_controls
python3 test_structured_controls.py
```

The checkpoint is calibration only. It makes no decipherment claim and performs
no H_C/H_D/H_G ranking.
