# Subject → predicate-family → ending agreement probe

Date: 2026-08-24

## Goal

Test a stronger consequence of the explicit-subject hypothesis.

If some frequent short tokens are personal pronouns/subject markers in an inflecting
European language, two levels of structure should appear:

1. several candidate subjects should select overlapping predicate/verb stem families;
2. within the same stem family, different subject candidates may prefer different endings.

This approximates structures such as:

    ich geh-e
    du geh-st
    er geh-t
    wir geh-en

without assuming German spellings or even that the underlying language is German.

## Predicate-family inference

No dictionary or language was used.

A conservative surface stem family is created when tokens:

- contain at least 3 EVA glyphs;
- share an exact prefix of at least 2 EVA glyphs;
- differ in the last 1 or 2 glyphs;
- have at least 2 observed ending variants;
- have at least 12 total occurrences.

This is intentionally simple. It detects suffixal paradigms but will miss stem-changing,
prefixal and non-concatenative morphology.

## Coverage

Top short tokens by fraction of immediate successors that fall into an inferred
predicate/morphological family:

| subject   |   family_coverage |   family_obs |   successor_obs |
|:----------|------------------:|-------------:|----------------:|
| oly       |             1.435 |           33 |              23 |
| sal       |             1.257 |           44 |              35 |
| chey      |             1.211 |          580 |             479 |
| chcthy    |             1.205 |           94 |              78 |
| oky       |             1.2   |           90 |              75 |
| cthey     |             1.19  |           50 |              42 |
| chdy      |             1.189 |          113 |              95 |
| shckhy    |             1.185 |           64 |              54 |
| lor       |             1.182 |           39 |              33 |
| chckhy    |             1.177 |          153 |             130 |
| qo        |             1.157 |           59 |              51 |
| shey      |             1.147 |          374 |             326 |
| tol       |             1.143 |           48 |              42 |
| shcthy    |             1.138 |           33 |              29 |
| chos      |             1.132 |           43 |              38 |
| ol        |             1.128 |          609 |             540 |
| key       |             1.125 |           36 |              32 |
| sol       |             1.113 |           69 |              62 |
| dy        |             1.099 |          144 |             131 |
| chal      |             1.096 |           57 |              52 |

High coverage does **not** make a token a pronoun; it only says its following tokens
often belong to repeatable stem/ending families.

## Candidate subject pairs in predicate-family space

Across all eligible short-token pairs, the family-distribution cosine baseline is:

- median: 0.279
- 95th percentile: 0.654
- 99th percentile: 0.821

Selected pairs among the earlier broad-context/pronoun-zone candidates:

| a    | b    |   count_a |   count_b |   family_obs_a |   family_obs_b |   family_cosine |   shared_families |   shared_min_count |
|:-----|:-----|----------:|----------:|---------------:|---------------:|----------------:|------------------:|-------------------:|
| or   | s    |       390 |       328 |            406 |            291 |           0.961 |                54 |                227 |
| s    | r    |       328 |       196 |            291 |            176 |           0.954 |                34 |                127 |
| or   | r    |       390 |       196 |            406 |            176 |           0.951 |                42 |                143 |
| ar   | or   |       449 |       390 |            388 |            406 |           0.908 |                77 |                225 |
| ar   | r    |       449 |       196 |            388 |            176 |           0.895 |                45 |                145 |
| ar   | s    |       449 |       328 |            388 |            291 |           0.884 |                57 |                176 |
| y    | ol   |       210 |       588 |            176 |            609 |           0.828 |                66 |                142 |
| shey | chey |       344 |       510 |            374 |            580 |           0.808 |                95 |                258 |
| ol   | al   |       588 |       311 |            609 |            245 |           0.765 |                80 |                165 |
| dar  | ol   |       287 |       588 |            242 |            609 |           0.754 |                77 |                163 |
| s    | cheo |       328 |        75 |            291 |             62 |           0.748 |                17 |                 32 |
| y    | al   |       210 |       311 |            176 |            245 |           0.739 |                50 |                100 |
| or   | cheo |       390 |        75 |            406 |             62 |           0.732 |                16 |                 32 |
| r    | cheo |       196 |        75 |            176 |             62 |           0.731 |                14 |                 28 |
| or   | lor  |       390 |        38 |            406 |             39 |           0.73  |                16 |                 31 |
| r    | lor  |       196 |        38 |            176 |             39 |           0.723 |                10 |                 23 |
| ar   | dar  |       449 |       287 |            388 |            242 |           0.717 |                78 |                150 |
| or   | ol   |       390 |       588 |            406 |            609 |           0.689 |                82 |                229 |
| s    | lor  |       328 |        38 |            291 |             39 |           0.688 |                11 |                 24 |
| or   | dar  |       390 |       287 |            406 |            242 |           0.685 |                65 |                130 |
| ar   | lor  |       449 |        38 |            388 |             39 |           0.673 |                12 |                 27 |
| ar   | cheo |       449 |        75 |            388 |             62 |           0.659 |                17 |                 33 |
| ar   | ol   |       449 |       588 |            388 |            609 |           0.647 |                95 |                219 |
| y    | dar  |       210 |       287 |            176 |            242 |           0.634 |                46 |                 84 |
| dar  | al   |       287 |       311 |            242 |            245 |           0.615 |                60 |                100 |

A high score means that the two short tokens tend to be followed by the **same inferred
stem families**, not merely by the same exact words.

## Person/agreement probe

For every shared stem family with >=8 observations after each of two short candidates,
we compare the distributions of final 1–2 glyph endings.

The strongest cases where the two candidates prefer different endings are:

| subject_a   | subject_b   | family   |   support_a |   support_b |    TV |   JSD | top_end_a   |   top_end_a_pct | top_end_b   |   top_end_b_pct |
|:------------|:------------|:---------|------------:|------------:|------:|------:|:------------|----------------:|:------------|----------------:|
| chor        | dar         | F0001    |          12 |          11 | 0.917 | 0.881 | ky          |          33.333 | dy          |          54.545 |
| s           | dar         | F0001    |          19 |          11 | 0.895 | 0.864 | ol          |          26.316 | dy          |          54.545 |
| dar         | dor         | F0001    |          11 |           8 | 0.875 | 0.85  | dy          |          54.545 | ey          |          37.5   |
| r           | dar         | F0001    |           8 |          11 | 0.875 | 0.767 | ey          |          37.5   | dy          |          54.545 |
| chor        | qol         | F0001    |          12 |          19 | 0.864 | 0.797 | ky          |          33.333 | dy          |          63.158 |
| ar          | dar         | F0001    |          14 |          11 | 0.857 | 0.732 | ey          |          28.571 | dy          |          54.545 |
| chol        | dar         | F0001    |          13 |          11 | 0.846 | 0.734 | ol          |          30.769 | dy          |          54.545 |
| chor        | l           | F0001    |          12 |          18 | 0.806 | 0.728 | ky          |          33.333 | dy          |          44.444 |
| y           | dar         | F0001    |          14 |          11 | 0.786 | 0.638 | ol          |          28.571 | dy          |          54.545 |
| ar          | l           | F0001    |          14 |          18 | 0.746 | 0.537 | ey          |          28.571 | dy          |          44.444 |
| y           | qol         | F0001    |          14 |          19 | 0.733 | 0.502 | ol          |          28.571 | dy          |          63.158 |
| y           | dor         | F0001    |          14 |           8 | 0.732 | 0.554 | ol          |          28.571 | ey          |          37.5   |
| s           | l           | F0001    |          19 |          18 | 0.722 | 0.598 | ol          |          26.316 | dy          |          44.444 |
| y           | chor        | F0001    |          14 |          12 | 0.702 | 0.54  | ol          |          28.571 | ky          |          33.333 |
| chor        | al          | F0001    |          12 |          15 | 0.7   | 0.597 | ky          |          33.333 | dy          |          40     |
| r           | l           | F0001    |           8 |          18 | 0.694 | 0.521 | ey          |          37.5   | dy          |          44.444 |
| dor         | qol         | F0001    |           8 |          19 | 0.684 | 0.61  | ey          |          37.5   | dy          |          63.158 |
| s           | qol         | F0001    |          19 |          19 | 0.684 | 0.634 | ol          |          26.316 | dy          |          63.158 |
| r           | al          | F0001    |           8 |          15 | 0.683 | 0.528 | ey          |          37.5   | dy          |          40     |
| or          | dar         | F0001    |          28 |          11 | 0.679 | 0.495 | ey          |          25     | dy          |          54.545 |
| chor        | dor         | F0001    |          12 |           8 | 0.667 | 0.54  | ky          |          33.333 | ey          |          37.5   |
| chor        | ol          | F0001    |          12 |          51 | 0.657 | 0.469 | ky          |          33.333 | dy          |          35.294 |
| dor         | l           | F0001    |           8 |          18 | 0.653 | 0.535 | ey          |          37.5   | dy          |          44.444 |
| ar          | al          | F0001    |          14 |          15 | 0.652 | 0.413 | ey          |          28.571 | dy          |          40     |
| ar          | y           | F0001    |          14 |          14 | 0.643 | 0.456 | ey          |          28.571 | ol          |          28.571 |

This table is the first direct search for a possible:

    subject-class ↔ predicate-ending

dependency.

## Interpretation

Three outcomes are possible:

### A — strong recurring agreement
The same 3–6 short tokens repeatedly share stems but select different endings across
many independent families.

This would be powerful evidence for a personal-pronoun / agreement system and would
strongly constrain candidate languages.

### B — shared predicates but no ending preference
Short tokens may be function words, articles, prepositions or discourse markers rather
than subjects.

### C — ending preference exists only in one or two families
Likely lexical/morphological coincidence or overfitting; not enough for person agreement.

## Current result

The corpus **does contain short-token pairs with high overlap in inferred predicate-family
space**, and it also contains isolated subject-pair × stem-family cases with different
ending preferences.

However, the ending differences are not yet a clean, repeated 3–6-person paradigm across
many independent stem families.

Therefore:

- a subject/pronoun interpretation remains plausible;
- person agreement is **not yet established**;
- the next step is to replace raw EVA suffixes with the hybrid latent-unit inventory,
  because endings such as `dy`, `y`, `aiin`, etc. are themselves likely structured units.

## Why this is useful even as a non-confirmation

This test narrows what a successful language model must explain:

1. short functional classes;
2. predicate-family overlap;
3. any stable short-token ↔ ending dependencies;
4. pro-drop vs explicit-subject rate.

A candidate language cannot be accepted merely because a few Voynich strings resemble
known words.

## Next step

Construct the first **latent-unit segmentation** for the strongest supported blocks:

- `qo`
- `ch`
- `sh`
- `da`
- `dy`
- gallows as hybrid atomic/modifier structures

Then rerun:

    short-token classes
    pronoun-family similarity
    subject ↔ predicate-family overlap
    subject ↔ ending agreement

If the proposed units are closer to the real writing system, the grammatical signal
should become cleaner rather than noisier.


## Post-hoc robustness check on the strongest signal

The strongest earlier distributional pair, `or / s`, remains unusually similar after
replacing exact successor words with inferred stem families:

- `or / s`: family cosine = **0.961**
- `s / r`: **0.954**
- `or / r`: **0.951**
- `ar / or`: **0.908**

For all eligible short-token pairs:

- median family cosine = **0.279**
- 95th percentile = **0.654**
- 99th percentile = **0.821**

Thus `or/s/r`, and to a lesser degree `ar`, form a genuinely unusual distributional
neighbourhood. This is stronger than a simple spelling resemblance.

### Agreement caution

The single strongest ending-contrast family, `F0001`, is very broad:

- stem: `ch-e`
- total occurrences: 1,226
- major final variants: `dy`, `ey`, `ol`, `or`, `ky`, `ar`, `ckhy`, `al`, ...

Therefore the dramatic one-family ending differences cannot be treated as person
agreement.

More interestingly, some candidate pairs show differential ending preferences in
**multiple independent families**:

- `or / s`: 3 families
- `s / r`: 2 families
- `ar / s`: 2 families
- `or / ol`: 3 families

For `or / s`, the three observed families show only moderate ending divergence rather
than one overwhelming person-specific suffix. That is intriguing but still below the
threshold for an agreement claim.

### Updated interpretation

`or / s / r` is now a priority **functional-paradigm candidate**, not yet a pronoun
paradigm.

The decisive next criterion is recurrence:

> the same short-token contrasts must predict compatible ending contrasts across many
> independent latent stem families.

This is exactly what the latent-unit resegmentation will test next.
