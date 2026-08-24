# Latent-unit segmentation v0.1

Date: 2026-08-24

## Goal

Test whether a conservative hybrid segmentation makes the manuscript's short-token and
grammatical structure cleaner.

## Frozen first-pass latent units

Only previously supported candidates are promoted:

- `q + o` -> `QO`
- `d + a` -> `DA`
- `d + y` -> `DY`
- EVA `ch` -> `CH`
- EVA `sh` -> `SH`

Gallows `k/t/p/f` remain atomic visible units in token segmentation. Their internal
components are retained conceptually as modifier features, not separate token units.

This deliberately avoids over-segmentation.

## 1. Token-length redistribution

### Raw EVA glyph length

|   length |   occurrences |   distinct |   top10_share |
|---------:|--------------:|-----------:|--------------:|
|        1 |          1220 |         25 |        92.131 |
|        2 |          3425 |        145 |        74.92  |
|        3 |          6659 |        551 |        37.934 |

### Latent-unit length

|   length |   occurrences |   distinct |   top10_share |
|---------:|--------------:|-----------:|--------------:|
|        1 |          1481 |         28 |        91.357 |
|        2 |          4198 |        175 |        66.508 |
|        3 |          7574 |        714 |        35.265 |

A correct latent model need not reduce the *number* of surface spellings. Its more useful
prediction is that meaningful grammatical classes become more compact when length is
measured in functional units rather than visible glyphs.

## 2. Global short-token comparison

| representation   |   short_forms_len<=3_count>=12 |   short_occurrences |   weighted_context_entropy |   left_edge_forms |   right_edge_forms |   broad_context_forms |
|:-----------------|-------------------------------:|--------------------:|---------------------------:|------------------:|-------------------:|----------------------:|
| EVA              |                            133 |                9762 |                      6.176 |                11 |                 12 |                    14 |
| LATENT_v0.1      |                            157 |               11279 |                      6.154 |                13 |                 14 |                    16 |

The first-pass segmentation moves additional previously longer tokens into the <=3-unit
functional search space.

### Highest-frequency newly admitted short tokens

| token   |   length |   count | behavior_class   |   line_initial_pct |   line_final_pct |   pred_types |   succ_types |
|:--------|---------:|--------:|:-----------------|-------------------:|-----------------:|-------------:|-------------:|
| chedy   |        3 |     341 | BROAD-CONTEXT    |              1.76  |            8.798 |          173 |          191 |
| shedy   |        3 |     255 | BROAD-CONTEXT    |              2.353 |            5.098 |          159 |          146 |
| dain    |        3 |     173 | LEFT-EDGE        |             24.277 |           11.561 |          103 |          114 |
| qoky    |        3 |     137 | MIXED            |              5.109 |           20.438 |           98 |           85 |
| dair    |        3 |      93 | LEFT-EDGE        |             26.882 |            7.527 |           60 |           70 |
| qoty    |        3 |      84 | MIXED            |              4.762 |           19.048 |           71 |           62 |
| chody   |        3 |      80 | MIXED            |              2.5   |            8.75  |           69 |           65 |
| shody   |        3 |      50 | MIXED            |             10     |           20     |           42 |           38 |
| daly    |        3 |      33 | RIGHT-EDGE       |              3.03  |           48.485 |           30 |           17 |
| kedy    |        3 |      25 | MIXED            |              0     |            4     |           22 |           24 |
| odar    |        3 |      25 | MIXED            |             16     |           12     |           18 |           21 |
| tedy    |        3 |      22 | MIXED            |              9.091 |            0     |           19 |           21 |
| oldy    |        3 |      21 | RIGHT-EDGE       |              9.524 |           57.143 |           19 |            9 |
| qokl    |        3 |      21 | MIXED            |              4.762 |            4.762 |           20 |           17 |
| chdar   |        3 |      19 | MIXED            |              0     |            0     |           19 |           17 |
| dary    |        3 |      18 | MIXED            |             22.222 |           77.778 |           14 |            4 |
| qockhy  |        3 |      18 | MIXED            |              5.556 |            0     |           17 |           17 |
| odal    |        3 |      16 | MIXED            |             18.75  |           18.75  |           13 |           13 |
| cthody  |        3 |      15 | MIXED            |              0     |           13.333 |           15 |           13 |
| kchdy   |        3 |      15 | MIXED            |              6.667 |           13.333 |           14 |           13 |
| chdal   |        3 |      15 | MIXED            |              6.667 |            0     |           14 |           15 |
| qody    |        2 |      14 | MIXED            |             21.429 |           14.286 |           11 |           12 |
| lchdy   |        3 |      14 | MIXED            |              0     |           28.571 |           13 |           10 |
| qoar    |        3 |      13 | MIXED            |             15.385 |            7.692 |           11 |           11 |

This is useful only if the newly admitted forms reinforce coherent behavioural classes.

## 3. `or / s / r / ar` robustness after latent suffix-family inference

Previously, raw-EVA suffix families produced unusually high shared-family cosines.

Comparison:

| a   | b   |   raw_family_cosine |   latent_family_cosine |
|:----|:----|--------------------:|-----------------------:|
| or  | s   |               0.961 |                  0.959 |
| s   | r   |               0.954 |                  0.955 |
| or  | r   |               0.951 |                  0.959 |
| ar  | or  |               0.908 |                  0.907 |

If the values remain high, the functional-paradigm signal is not an artefact of treating
`qo/da/dy/ch/sh` as separate raw glyphs.

## 4. Latent predicate-family similarities

Strongest focus pairs:

| a   | b   |   count_a |   count_b |   family_obs_a |   family_obs_b |   family_cosine |   shared_families |
|:----|:----|----------:|----------:|---------------:|---------------:|----------------:|------------------:|
| or  | r   |       390 |       196 |            407 |            180 |           0.959 |                38 |
| or  | s   |       390 |       328 |            407 |            285 |           0.959 |                52 |
| s   | r   |       328 |       196 |            285 |            180 |           0.955 |                32 |
| ar  | or  |       449 |       390 |            400 |            407 |           0.907 |                71 |
| ar  | r   |       449 |       196 |            400 |            180 |           0.889 |                44 |
| ar  | s   |       449 |       328 |            400 |            285 |           0.874 |                60 |

## 5. Latent ending-agreement recurrence

Pairs showing different dominant endings across the largest number of independent latent
stem families:

| a    | b     |   n_families |   median_TV |   support_a |   support_b |
|:-----|:------|-------------:|------------:|------------:|------------:|
| or   | ol    |            4 |       0.311 |          46 |          87 |
| or   | l     |            3 |       0.77  |          47 |          38 |
| qol  | l     |            3 |       0.5   |          43 |          38 |
| shey | shedy |            3 |       0.359 |          52 |          67 |
| or   | s     |            3 |       0.295 |          49 |          48 |
| shey | chedy |            3 |       0.286 |          52 |          64 |
| ol   | l     |            2 |       0.617 |          58 |          22 |
| chey | shedy |            2 |       0.562 |          18 |          19 |
| chol | qol   |            2 |       0.554 |          23 |          35 |
| s    | r     |            2 |       0.553 |          37 |          23 |
| chor | chol  |            2 |       0.542 |          20 |          20 |
| ol   | al    |            2 |       0.445 |          82 |          23 |
| chol | al    |            2 |       0.439 |          23 |          23 |
| chor | ol    |            2 |       0.422 |          27 |          51 |
| or   | chol  |            2 |       0.412 |          38 |          23 |
| or   | dain  |            2 |       0.395 |          25 |          21 |
| ol   | qol   |            2 |       0.394 |          65 |          33 |
| chol | ol    |            2 |       0.379 |          45 |          51 |
| s    | ol    |            2 |       0.374 |          29 |          51 |
| dain | qol   |            2 |       0.345 |          21 |          34 |

This is the crucial person-agreement test.

A true subject/person paradigm should eventually show the **same candidate subjects**
predicting consistent ending classes across many independent stems.

## 6. Interpretation rule

### Segmentation is helped if:

- important functional paradigms survive or strengthen;
- short-token classes become easier to state;
- repeated ending dependencies become more coherent;
- fewer ad-hoc EVA suffix distinctions are required.

### Segmentation is weakened if:

- previously strong distributional families disappear;
- edge/context classes become noisier;
- agreement candidates become less recurrent.

## Current verdict

This first latent pass is a **representation experiment**, not a decipherment.

The strongest success criterion is not compression alone. It is whether the same small set
of latent units simultaneously clarifies:

1. token length;
2. positional function;
3. subject/predicate family overlap;
4. ending paradigms.

The resulting measurements are stored alongside the raw-EVA controls so every promoted
unit can later be removed independently and retested.


## 7. One-unit-at-a-time ablation

The first-pass inventory was not accepted as a package. Each candidate block was removed
in turn and the complete short-token / latent-family analysis was rerun.

Key principle:

> a visually plausible block should remain promoted only if removing it makes independent
> structural metrics worse or destroys a useful invariant.

The ablation table is stored in `latent_unit_ablation.csv`.

Summary:

| active         |   short_forms |   short_occ |   weighted_context_entropy |   left |   right |   broad |   or_s_cos |   or_r_cos |   s_r_cos |   or_s_diff_families |   or_s_median_TV |   n_families |   entropy_delta_vs_full |   or_s_delta_vs_full |
|:---------------|--------------:|------------:|---------------------------:|-------:|--------:|--------:|-----------:|-----------:|----------:|---------------------:|-----------------:|-------------:|------------------------:|---------------------:|
| CH+DA+DY+QO+SH |           157 |       11279 |                     6.1539 |     13 |      14 |      16 |     0.9589 |     0.9590 |    0.9546 |                    3 |           0.2955 |          538 |                  0.0000 |               0.0000 |
| CH+DA+DY+SH    |           152 |       11006 |                     6.1642 |     13 |      14 |      16 |     0.9589 |     0.9590 |    0.9546 |                    3 |           0.2955 |          540 |                  0.0103 |              -0.0001 |
| CH+DY+QO+SH    |           149 |       10887 |                     6.1745 |     11 |      13 |      16 |     0.9571 |     0.9596 |    0.9525 |                    3 |           0.2955 |          550 |                  0.0206 |              -0.0018 |
| CH+DA+QO+SH    |           147 |       10441 |                     6.1382 |     13 |      13 |      14 |     0.9624 |     0.9495 |    0.9565 |                    3 |           0.2500 |          528 |                 -0.0157 |               0.0035 |
| DA+DY+QO+SH    |           157 |       11279 |                     6.1539 |     13 |      14 |      16 |     0.9589 |     0.9590 |    0.9546 |                    3 |           0.2955 |          538 |                  0.0000 |               0.0000 |
| CH+DA+DY+QO    |           157 |       11279 |                     6.1539 |     13 |      14 |      16 |     0.9589 |     0.9590 |    0.9546 |                    3 |           0.2955 |          538 |                  0.0000 |               0.0000 |
| NONE           |           133 |        9762 |                     6.1755 |     11 |      12 |      14 |     0.9613 |     0.9512 |    0.9543 |                    3 |           0.2500 |          539 |                  0.0217 |               0.0024 |

### Reading the ablation

`CH` and `SH` are already single EVA glyphs in this parsing convention, so promoting their
names does not change token length; their ablations are representation-label controls rather
than true segmentation changes.

The true first-pass segmentation decisions are therefore primarily `QO`, `DA`, and `DY`.

No single candidate produces a dramatic global entropy improvement. The useful result is
more conservative:

- the `or/s/r` functional-paradigm signal is highly stable under all ablations;
- it is therefore **not an artefact of any one of QO/DA/DY**;
- the latent inventory currently provides only a small global context-entropy gain;
- no block should be assigned a phonetic value merely because it was promoted.

The next inventory version should rank QO/DA/DY by *local* predictive evidence rather than
expecting one global short-token entropy metric to decide all unit boundaries.
