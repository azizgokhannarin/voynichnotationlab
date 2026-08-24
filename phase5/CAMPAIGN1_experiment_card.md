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
