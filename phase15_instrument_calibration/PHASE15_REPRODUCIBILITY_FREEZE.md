# Phase 15 reproducibility freeze

Date frozen: 2026-08-26

Status: frozen before the full-size negative-control instrument was run.

## Scope

This freeze closes the missing executable/provenance layer behind Phase 15. It does not erase
or invalidate the v4.3 observations. It replaces no legacy result silently: legacy v4.4 JSON is
retained, while the executable implementation writes versioned reproduction results.

## Scientific discipline

- H_C, H_D and H_G remain open hypothesis classes.
- No ranking among H_C, H_D and H_G is permitted until the full-size control is complete.
- No new language search, semantic/illustration crib, Voynich generator enrichment or latent
  state is permitted in this phase.
- Voynich final-test pages and the control final-test partition remain sealed.
- Calibration precedes interpretation; raw identity precedes compressed classes.

## Frozen instrument

The executable instrument is `phase15_reproducibility.py` and has four operations:

1. build the frozen Voynich TRAIN/VALIDATION line corpus from RF1b-EVA;
2. build the full-size CREMMA diplomatic control from ALTO XML;
3. build a known-content LatinISE strong-renderer control;
4. fit frozen TRAIN-only distributional classes and evaluate class order, line reset, distant
   context and model competition on VALIDATION.

### Distributional classes

- minimum TRAIN token-type count: 4;
- left/right context vocabulary: 64 most frequent TRAIN token types plus boundary/other bins;
- context transform: row-frequency normalization followed by L2 normalization;
- clustering: 12-cluster KMeans, `n_init=20`, seed `20260826`;
- types below threshold or unseen in VALIDATION: `RARE`;
- class assignments are learned on TRAIN and then frozen.

### Class-order diagnostic

- mutual information at within-line lags 1 through 5;
- 200 independent within-line shuffles;
- reported statistic: z against the shuffle distribution;
- seed: `20260826`.

### Predictive models

- one-hot categorical features;
- multinomial logistic regression (`lbfgs`, `C=1`, `max_iter=1000`);
- TRAIN fit only, VALIDATION cross-entropy and accuracy;
- probability clipping: `1e-15`;
- fixed position and length buckets defined in source code.

This is the first archived executable specification of the Phase 15 instrument. Because the
original transient v4.4 script was not archived, numerical identity with the four legacy v4.4
result files is not assumed. Agreement or disagreement is reported explicitly.

## Source locks

Exact URLs, commits, checksums, licences, inclusion rules and expected derived counts are frozen
in `SOURCE_PROVENANCE_v1.json`.

## Environment

Required Python packages:

- Python 3.11+
- NumPy
- scikit-learn

The ALTO and IVTFF parsers otherwise use only the Python standard library.

