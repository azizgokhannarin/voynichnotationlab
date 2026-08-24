# Campaign 1 — Experiment Card

## Candidate families
- West Germanic
- Romance
- West Slavic
- Latin

## Primary historical window
1300–1500 CE

## Frozen structural model
See `FROZEN_REPRESENTATION_v1.md`.

## Split
Whole pages: 60 / 20 / 20 train-validation-test.

## Primary outcome
Held-out phoneme-sequence likelihood / cross entropy.

## Required nulls
- within-token shuffle
- token-order shuffle
- matched synthetic corpus
- unit-label permutation

## Mapping constraints
- fixed mapping
- <=2 silent units
- <=2 context-sensitive rules
- no per-word / per-page remapping
- complexity penalized

## Advancement
Must beat:
1. matched nulls,
2. competing families,
3. held-out overfitting checks.

## Forbidden
- manual test-set adjustment
- post-hoc representation changes
- isolated word resemblance as evidence

## Frozen concrete resources
See `CORPUS_FREEZE_campaign1.md`.

## Frozen target normalizers
See `PHONOGRAPHIC_NORMALIZATION_v1.md`.

## Frozen Voynich split
See `voynich_page_split_manifest.csv` and `VOYNICH_SPLIT_FREEZE.md`.

Search remains blocked until historical corpus exports/files are locally frozen and hashed.
