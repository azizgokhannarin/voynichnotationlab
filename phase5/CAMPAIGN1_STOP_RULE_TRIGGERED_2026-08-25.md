# Campaign 1 — design stop before final test

Date: 2026-08-25

## Decision

**STOP CAMPAIGN 1 BEFORE FINAL-TEST SCORING.**

Reason: two preregistered primary nulls are degenerate under the frozen scoring/mapping model:

- Null B is exactly invisible to token-independent scoring;
- Null D is a source-label symmetry when the optimizer is rerun.

Because the frozen primary evidence rule requires a standardized advantage against all four nulls,
Campaign 1 cannot produce its preregistered primary statistic without changing the design after
validation results have been observed.

## What this does not mean

It does **not** mean:

- West Germanic failed;
- Romance won;
- Latin won;
- the Voynich Manuscript is not natural language;
- any mapping is a decipherment.

The raw branch cross-entropies are not directly comparable across target languages and were never
preregistered as a stand-alone family ranking.

## Data preserved

The five train/validation mappings and their hashes are frozen for audit in:

`phase5/MAPPING_FREEZE_train_validation.json`

The final-test set remains unscored.

Campaign 2 must be preregistered before any corrected null/scoring experiment is run.
