# Campaign 2 Preregistration — Minimal Decisive Historical-Language Test

Frozen: 2026-08-25

## Central question
Does the frozen Voynich representation contain historical-language phonographic structure
that exceeds what is already explained by its own within-token structural grammar?

Campaign 2 contains **one primary experiment and two secondary controls only**.

## Frozen inputs
Campaign 2 uses the exact `C1-STRUCT-v1` representation, whole-page train/validation/final-test
split, historical corpora, PHONO-* normalizers, mapping engine, scorer, complexity function,
beam width, and primary mapping class already frozen before this campaign.

Active branches: WG-ReF, WG-ReN, RO-BFM, RO-Dante, LA-LatinISE.
Families: West Germanic=mean(ReF,ReN), Romance=mean(BFM,Dante), Latin=LatinISE.
West Slavic remains NOT TESTED because primary Old Czech bulk acquisition is blocked.

No new corpus, language family, structural gate, mapping family, scorer or parameter sweep is
permitted in response to Campaign-2 results.

## Entropy-budget diagnostic — descriptive, not a gate
Train:
- independent-slot: **3.255039 bits/unit**
- first-order within-token: **2.668579 bits/unit**
- residual conditional-structure budget: **0.586460 bits/unit**

Validation:
- independent-slot: **3.232650 bits/unit**
- first-order within-token: **2.668549 bits/unit**
- residual conditional-structure budget: **0.564100 bits/unit**

This diagnostic may not alter the frozen representation or decision threshold.

# Primary — selection-inclusive weak surrogate
For each branch:
1. optimize on real TRAIN and score real VALIDATION;
2. generate **N=500** surrogates;
3. preserve page/line/token layout and exact token length at every position;
4. independently shuffle units within every token;
5. **rerun the complete mapping optimizer from scratch for every surrogate TRAIN**;
6. score the selected surrogate mapping on corresponding surrogate VALIDATION.

The optimizer is part of the null distribution.

Lower validation objective `J` is better.

    A_weak = mean(J_null) - J_real
    Z_weak = A_weak / sd(J_null)
    p_weak = (1 + count(J_null <= J_real)) / 501

No Gaussian extrapolation below 1/501.

# Secondary 1 — instrument calibration
## Positive
For every historical branch, re-encode held-out normalized historical text through a deterministic
invented source alphabet of approximately Voynich inventory size, hide the key, and run the same
optimizer. The correct branch must pass the same weak-surrogate criterion.

## Negative
Use matched synthetic source preserving token lengths and unit marginals but lacking historical
conditional structure. It must not produce a historical-language positive.

A genuine non-European language is not used as the negative control.

If the positive calibration fails or the negative calibration is falsely positive, the instrument
is invalid: Campaign 2 stops and final test remains sealed.

# Secondary 2 — independent slot-grammar surrogate
For each branch generate **N=500** surrogate corpora using TRAIN-only empirical distributions:
- preserve exact page/line/token layout and token length;
- singleton token -> TRAIN singleton distribution;
- first unit -> TRAIN START distribution;
- internal units -> independently sampled TRAIN CORE distribution;
- final unit -> TRAIN TERMINAL distribution.

Use the train-derived generator for both surrogate TRAIN and surrogate VALIDATION skeletons.
Rerun the complete mapping optimizer for every replicate.

    A_slot = mean(J_slot) - J_real
    Z_slot = A_slot / sd(J_slot)

with analogous one-sided empirical `p_slot`.

This is the decisive control: does historical-language fit exceed the frozen Voynich slot template?

# Family-relative descriptive normalization
Raw branch losses are not compared.

For each branch:
- floor = mean slot-surrogate loss
- ceiling = branch-specific positive-calibration loss

Report:
    R = (floor_loss - real_loss) / (floor_loss - ceiling_loss)

R is descriptive only; empirical surrogate tests remain primary.

# Validation advancement criterion
Final test may be opened only if ALL are true:
1. positive/negative calibration behaves correctly;
2. at least one active FAMILY passes weak surrogate;
3. the same family passes slot surrogate;
4. family evidence survives Holm correction across West Germanic, Romance, Latin at **alpha=0.01**;
5. no methodology changed after validation inspection.

# Mandatory failure rule
If validation criteria are not met:

> The historical-language phonographic mapping experiment is complete and unsuccessful under
> the frozen representation and frozen hypothesis class.

Then:
- FINAL TEST REMAINS SEALED;
- no automatic Campaign 3 mapping refinement;
- no new null to rescue the result;
- no retuning of representation, normalizer, scorer, beam, complexity, corpus or family.

The project returns to the pre-language evidence and separately reassesses:
1. direct observations;
2. interpretations;
3. assumptions introduced by the phonographic test.

At minimum reconsider whether:
- EVA-derived frozen units are at the correct encoding level;
- visible generative boundaries are phonographic word-like units;
- unit-local phonographic mapping is the right model class;
- the system may instead be syllabic, abbreviation-heavy, morphographic, mixed, or non-unit-local.

A new experiment requires that conceptual reassessment first.

# Final-test rule
Only after validation success:
1. hash-freeze selected mappings, scorer, models, calibration and surrogate implementation;
2. open the 46 final-test pages once;
3. run only the preregistered primary experiment;
4. no remapping or retuning;
5. report the outcome regardless of direction.

# Explicitly abandoned
- Campaign-1 token-order Null B repairs;
- Campaign-1 label-permutation Null D repairs;
- further structural gates;
- additional corpora/languages;
- penalty/beam/n-gram/smoothing sweeps;
- context-sensitive mappings;
- lexical exceptions;
- semantic or illustration-driven anchors.

PASS would support phonographic fit beyond both weak disorder and the independent slot template.
FAIL means no detectable historical-language phonographic fit under this representation/model
class and terminates this test family.
