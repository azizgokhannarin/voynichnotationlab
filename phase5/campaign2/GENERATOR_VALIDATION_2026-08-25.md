# Campaign 2 Generator Validation

Date: 2026-08-25

Status: **PASS**

No real Campaign-2 Voynich validation surrogate distribution was run.

Validated components:

- deterministic weak within-token shuffle;
- exact layout/token-length preservation for weak surrogate;
- exact global source-unit multiset preservation for weak surrogate;
- deterministic TRAIN-fit independent-slot generator;
- slot-role support restricted to TRAIN-estimated role inventories;
- deterministic positive calibration encoding;
- negative calibration preserves exact token-length vector and global class multiset;
- end-to-end synthetic instrument fixture scores known positive better than matched negative;
- frozen mapping-engine, Numba-equivalence and Campaign-1 null regression tests still pass.

Combined regression-output SHA-256:

`01d734b73cd837b0a5b451e22a880f50357ddc3343ff8d94a7ad0b049608f697`

Next allowed step under the frozen Campaign-2 plan:

1. build branch-specific real calibration streams;
2. run instrument calibration;
3. only if calibration is valid, run the N=500 weak and N=500 slot validation experiment.

Final-test pages remain sealed.
