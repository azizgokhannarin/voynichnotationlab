# Phase 20 cross-phase identifiability audit rubric

Date frozen: 2026-08-26  
New model fitting: **NO**  
Voynich final-test access: **NO**

## Purpose

This audit combines already frozen Phase 13–19 decisions. It does not rescore
Voynich, change a representation or create a new hypothesis probability. Its
job is to separate calibrated conclusions from observations, identify which
hypothesis subclasses are closed, evaluate the previously stated STOP rule and
decide whether any narrowly bounded next experiment is authorized.

## Evidence classes

Every cross-phase claim is assigned exactly one class:

1. `CALIBRATED_DISCRIMINATOR` — positive and negative controls show the device
   can distinguish the tested alternatives;
2. `CALIBRATED_NONDISCRIMINATOR` — a known alternative reproduces the signal,
   so the measurement cannot rank the relevant hypotheses;
3. `BOUNDED_SUBCLASS_CLOSURE` — a preregistered model class fails, without
   closing its broader parent hypothesis;
4. `SURFACE_OBSERVATION_ONLY` — a reproducible manuscript property whose cause
   remains unidentified;
5. `OPEN_UNTESTED_DISCRIMINATOR` — a required falsifier has not yet been run.

No numerical evidence is converted into posterior odds for `H_C`, `H_D` or
`H_G`.

## Previously stated four-part STOP rule

`STOP_INTERNAL_EVIDENCE` requires all four components:

1. the measurement pipeline is certified on real and synthetic controls;
2. a bounded copy/modify generator matches the full held-out metric battery,
   including raw lexical recurrence;
3. certified residual capacity is below text-carrying bandwidth;
4. Voynich is statistically inseparable from at least one attested
   non-linguistic record genre, including quantitative effect sizes rather than
   only a qualitative phenotype.

If any component is false, this exact STOP rule is not satisfied. Failure of
the STOP rule does not authorize unrestricted exploration.

## Bounded continuation authorization

`CONTINUE_BOUNDED_ONLY` is allowed only when an experiment:

- was specified before the current audit rather than invented from a new
  result;
- targets an explicit falsifier for one open hypothesis class;
- has a finite module and parameter budget;
- uses TRAIN/VALIDATION only and leaves final-test sealed;
- is calibrated on parameter-matched controls;
- cannot be interpreted as proving its parent hypothesis if it succeeds.

The only candidate evaluated here is the deferred Phase-14 augmentation ladder:
line-final realization, copy/modify adjacency and productive vocabulary
innovation, tested one at a time and then in one frozen combination. A new
latent state is explicitly excluded because Phase 19 did not authorize larger
state spaces.

## Final-test authorization

`OPEN_FINAL_TEST` requires a newly frozen model or representation that makes a
directional prediction on a metric not used to select or tune it on VALIDATION.
All preprocessing, parameters, stopping rules and interpretation must be frozen
after control calibration and before final-test access. Existing Validation
descriptions alone cannot authorize final-test opening.

## Interpretation restrictions

The audit may not claim that Voynich is natural language, non-language,
structured data or autonomous generation. It may not treat line reset,
line-final realization, high residual capacity, a qualitative structured-data
match or fitted latent-state persistence as content-type evidence. `H_C`, `H_D`
and `H_G` remain open and unranked unless a future calibrated discriminator
directly closes a bounded subclass.

