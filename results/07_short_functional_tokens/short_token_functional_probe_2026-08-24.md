# Short-token simplification and separable-particle probe

Date: 2026-08-24

## Goal
Reduce 1–3 EVA-glyph tokens to a small number of behavioural classes before assigning meanings.

## Corpus
- clean tokens: 37948
- lines: 5360
- baseline line-initial: 14.12%
- baseline line-final: 14.12%

## Repertoire concentration
| glyph length | occurrences | distinct forms | top-10 share |
|---:|---:|---:|---:|
| 1 | 1220 | 25 | 92.1% |
| 2 | 3425 | 145 | 74.9% |
| 3 | 6659 | 551 | 37.9% |

Shorter tokens are dramatically more concentrated into a small repertoire.

## Behaviour classes

### RIGHT-EDGE
| token   |   glyph_len |   count |   line_final_pct |   line_initial_pct |   pred_types |   succ_types |
|:--------|------------:|--------:|-----------------:|-------------------:|-------------:|-------------:|
| dy      |           2 |     204 |            35.78 |               0.98 |          153 |          107 |
| am      |           2 |     115 |            69.57 |               0.87 |           84 |           34 |
| oly     |           3 |      65 |            64.62 |               0    |           60 |           22 |
| dam     |           3 |      59 |            66.1  |               0    |           47 |           20 |
| d       |           1 |      53 |            30.19 |              15.09 |           35 |           26 |
| sy      |           2 |      40 |            55    |               2.5  |           37 |           17 |
| aly     |           3 |      39 |            53.85 |               0    |           34 |           17 |
| lol     |           3 |      35 |            45.71 |              14.29 |           25 |           14 |
| ary     |           3 |      32 |            78.12 |               3.12 |           27 |            7 |
| cham    |           3 |      24 |            58.33 |               0    |           24 |            9 |
| ldy     |           3 |      20 |            70    |               0    |           19 |            6 |
| om      |           2 |      20 |            70    |               5    |           17 |            6 |

### LEFT-EDGE
| token   |   glyph_len |   count |   line_initial_pct |   line_final_pct |   pred_types |   succ_types |
|:--------|------------:|--------:|-------------------:|-----------------:|-------------:|-------------:|
| sho     |           2 |     118 |              27.97 |             0    |           75 |           96 |
| sar     |           3 |      77 |              40.26 |            18.18 |           42 |           39 |
| dor     |           3 |      63 |              41.27 |             0    |           34 |           48 |
| sol     |           3 |      63 |              57.14 |             1.59 |           25 |           48 |
| qo      |           2 |      51 |              27.45 |             0    |           36 |           44 |
| sal     |           3 |      48 |              22.92 |            27.08 |           37 |           32 |
| tar     |           3 |      43 |              37.21 |             4.65 |           27 |           32 |
| sor     |           3 |      43 |              72.09 |             0    |           12 |           34 |
| tol     |           3 |      42 |              59.52 |             0    |           17 |           38 |
| oar     |           3 |      22 |              36.36 |            13.64 |           14 |           14 |
| qor     |           3 |      22 |              31.82 |             9.09 |           13 |           15 |

### BROAD-CONTEXT
| token   |   glyph_len |   count |   pred_types |   succ_types |   pred_entropy |   succ_entropy |
|:--------|------------:|--------:|-------------:|-------------:|---------------:|---------------:|
| ol      |           2 |     588 |          322 |          262 |           7.87 |           7.33 |
| chey    |           3 |     510 |          285 |          282 |           7.64 |           7.69 |
| ar      |           2 |     449 |          262 |          245 |           7.49 |           7.17 |
| or      |           2 |     390 |          239 |          196 |           7.52 |           6.63 |
| chol    |           3 |     367 |          232 |          220 |           7.44 |           7.16 |
| shey    |           3 |     344 |          228 |          221 |           7.51 |           7.4  |
| s       |           1 |     328 |          232 |          138 |           7.65 |           5.99 |
| al      |           2 |     311 |          172 |          191 |           6.79 |           7.34 |
| dar     |           3 |     287 |          190 |          167 |           7.39 |           7.07 |
| chor    |           3 |     215 |          151 |          146 |           6.99 |           6.9  |
| y       |           1 |     210 |          127 |          133 |           6.75 |           6.91 |
| chy     |           2 |     197 |          145 |          135 |           6.94 |           6.85 |

### SELECTIVE
| token   |   glyph_len |   count |   best_prior_pmi |   best_prior_support |   best_prior_distance | best_prior_token   |
|:--------|------------:|--------:|-----------------:|---------------------:|----------------------:|:-------------------|
| l       |           1 |     156 |             4.79 |                   12 |                     1 | o                  |
| qol     |           3 |     147 |             3.26 |                   11 |                     1 | chedy              |
| chckhy  |           3 |     141 |             3.32 |                   10 |                     1 | qokain             |
| air     |           3 |      95 |             3.52 |                    9 |                     1 | s                  |
| cthor   |           3 |      45 |             3.29 |                    8 |                     1 | daiin              |

## Named working candidates
| token   |   glyph_len |   count | behavior_class   |   line_initial_pct |   line_final_pct |   pred_types |   succ_types |
|:--------|------------:|--------:|:-----------------|-------------------:|-----------------:|-------------:|-------------:|
| ol      |           2 |     588 | BROAD-CONTEXT    |               6.63 |             8.16 |          322 |          262 |
| ar      |           2 |     449 | BROAD-CONTEXT    |               2.23 |             8.69 |          262 |          245 |
| or      |           2 |     390 | BROAD-CONTEXT    |               7.69 |             4.1  |          239 |          196 |
| s       |           1 |     328 | BROAD-CONTEXT    |               8.54 |            12.2  |          232 |          138 |
| al      |           2 |     311 | BROAD-CONTEXT    |               0.96 |            13.5  |          172 |          191 |
| y       |           1 |     210 | BROAD-CONTEXT    |              20    |            21.9  |          127 |          133 |
| dy      |           2 |     204 | RIGHT-EDGE       |               0.98 |            35.78 |          153 |          107 |
| sho     |           2 |     118 | LEFT-EDGE        |              27.97 |             0    |           75 |           96 |
| am      |           2 |     115 | RIGHT-EDGE       |               0.87 |            69.57 |           84 |           34 |
| oly     |           3 |      65 | RIGHT-EDGE       |               0    |            64.62 |           60 |           22 |
| dam     |           3 |      59 | RIGHT-EDGE       |               0    |            66.1  |           47 |           20 |
| qo      |           2 |      51 | LEFT-EDGE        |              27.45 |             0    |           36 |           44 |
| sy      |           2 |      40 | RIGHT-EDGE       |               2.5  |            55    |           37 |           17 |

## German-style separable-particle probe

For line-final `am/dam/oly/sy/dy`, inspect all words 1–6 positions earlier.

| token   |   line_final_count |   earlier_types_1to6 |   earlier_entropy |   top5_share_pct | top_predecessors                     |
|:--------|-------------------:|---------------------:|------------------:|-----------------:|:-------------------------------------|
| am      |                 80 |                  259 |              7.52 |            12.95 | aiin:16; ar:13; ol:11; chedy:9; or:9 |
| dy      |                 73 |                  262 |              7.79 |             8.31 | dy:7; daiin:7; dar:6; ar:6; cthy:5   |
| oly     |                 42 |                  166 |              7.02 |            16.32 | ol:14; qol:7; aiin:6; or:6; qokeey:6 |
| dam     |                 39 |                  160 |              7.12 |            12.08 | daiin:8; ol:5; chy:4; chor:4; chey:4 |
| sy      |                 22 |                   96 |              6.47 |            12.93 | daiin:4; aiin:4; s:3; qotchy:2; ol:2 |

A strongly lexically selected separable particle should repeatedly pair with a narrow stem family.
Instead, these high-frequency candidates have broad earlier contexts.

### Joined-form control
If S is a separable prefix, an especially strong clue would be recurrent surface forms `S+stem`
(or `stem+S`) elsewhere.

| token   |   final_count |   opportunities |   prefix_compound_hits |   suffix_compound_hits |   prefix_hit_pct |   suffix_hit_pct |
|:--------|--------------:|----------------:|-----------------------:|-----------------------:|-----------------:|-----------------:|
| am      |            80 |             448 |                      7 |                    120 |             1.56 |            26.79 |
| dy      |            73 |             373 |                     30 |                    122 |             8.04 |            32.71 |
| oly     |            42 |             239 |                      0 |                     29 |             0    |            12.13 |
| dam     |            39 |             207 |                      0 |                     25 |             0    |            12.08 |
| sy      |            22 |             116 |                      0 |                      8 |             0    |             6.9  |

There are occasional surface coincidences, but no strong productive joined/separated correspondence.

## Verdict
- **Short-token functional-class hypothesis:** supported structurally.
- **Current high-frequency right-edge tokens as German-like separable verb particles:** weakened.
- **Separable particles elsewhere or after latent stem inference:** still open.

## Simplification achieved
Hundreds of short surface forms can now be treated as five behavioural classes:

1. RIGHT-EDGE
2. LEFT-EDGE
3. BROAD-CONTEXT
4. SELECTIVE
5. MIXED

This is deliberately not a grammatical translation.

## Next falsifiable prediction
Resegment `qo`, `da`, `dy`, `ch`, `sh` and selected gallows constructions as candidate latent units,
then repeat this analysis using **latent-unit length** rather than EVA-glyph length.

If the hybrid-unit model is useful, the short-token inventory should become smaller and the
behaviour classes cleaner. If it does not, the proposed segmentation is not buying us anything.
