# Gate B2 — Core/rime phonography versus external syntax

Date: 2026-08-24

## Question

Gate B found strong residual stem × terminal structure after removing physical line-final
tokens. Gate B2 asks whether that structure generalizes from **internal core shape** or
from **external syntactic-like context**.

No historical language is used.

## Dataset

- all physical line-final occurrences excluded;
- one-glyph stems excluded;
- retained stems occur >=12 times, on >=2 pages, with >=2 terminal variants.

Retained:

- stems: **255**
- occurrences: **18545**

## Models

`INTERNAL` uses only:

- last two core glyphs;
- first core glyph;
- core length.

`EXTERNAL` uses only:

- previous/next functional-token roles;
- previous/next terminal classes;
- line-initial status.

`STATE` uses RF1b manuscript-state metadata.

All models use the same smoothed categorical likelihood estimator.

## 1. Whole-page holdout

| model             |   bits_per_occurrence |   accuracy |
|:------------------|----------------------:|-----------:|
| INTERNAL          |                1.179  |     0.7238 |
| INTERNAL_DEEP     |                1.2059 |     0.7223 |
| INTERNAL+STATE    |                1.5155 |     0.6546 |
| INTERNAL+EXTERNAL |                2.0365 |     0.4716 |
| ALL               |                2.2015 |     0.3999 |
| EXTERNAL+STATE    |                2.2804 |     0.3721 |
| STATE             |                2.2827 |     0.3642 |
| EXTERNAL          |                2.2947 |     0.3744 |
| EXTERNAL_WIDE     |                2.3121 |     0.3689 |
| GLOBAL            |                2.3347 |     0.3627 |

This tests transfer to unseen manuscript pages.

## 2. Whole-stem holdout

| model             |   bits_per_occurrence |   accuracy |
|:------------------|----------------------:|-----------:|
| INTERNAL          |                2.0673 |     0.4635 |
| INTERNAL+STATE    |                2.165  |     0.4334 |
| INTERNAL+EXTERNAL |                2.2958 |     0.3835 |
| STATE             |                2.3315 |     0.3521 |
| ALL               |                2.3341 |     0.3713 |
| EXTERNAL+STATE    |                2.3352 |     0.3619 |
| EXTERNAL          |                2.3455 |     0.3647 |
| INTERNAL_DEEP     |                2.3457 |     0.3628 |
| EXTERNAL_WIDE     |                2.3557 |     0.3653 |
| GLOBAL            |                2.368  |     0.3627 |

Here every test stem is **completely unseen during training**.

Critical comparison:

- INTERNAL: **2.0673 bits**
- EXTERNAL: **2.3455 bits**
- STATE: **2.3315 bits**
- INTERNAL+EXTERNAL: **2.2958 bits**
- ALL: **2.3341 bits**

On unseen stems, INTERNAL beats EXTERNAL by:

    **0.2782 bits/occurrence**

This is the decisive result: core/rime shape carries terminal information that transfers
across lexical stems.

## 3. Does external context still help after core shape?

On unseen stems:

    INTERNAL -> INTERNAL+EXTERNAL gain
    = **-0.2286 bits/occurrence**

and:

    INTERNAL -> INTERNAL+STATE gain
    = **-0.0977 bits/occurrence**

Thus external context and manuscript state can still contribute, but they sit on top of a
strong core-conditioned baseline.

Full incremental table:

| from              | to                |   gain_bits |
|:------------------|:------------------|------------:|
| GLOBAL            | INTERNAL          |      0.3007 |
| GLOBAL            | EXTERNAL          |      0.0225 |
| GLOBAL            | STATE             |      0.0365 |
| INTERNAL          | INTERNAL+EXTERNAL |     -0.2286 |
| INTERNAL          | INTERNAL+STATE    |     -0.0977 |
| INTERNAL+STATE    | ALL               |     -0.1692 |
| EXTERNAL          | INTERNAL+EXTERNAL |      0.0497 |
| EXTERNAL+STATE    | ALL               |      0.0011 |
| INTERNAL+EXTERNAL | ALL               |     -0.0383 |

## 4. Explicit core-ending profiles

Final core glyph:

| last1   |   total |    p_Ø |    p_l |    p_m |    p_n |    p_r |    p_s |    p_y |
|:--------|--------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| o       |    4540 | 0.1621 | 0.4729 | 0.0099 | 0.0007 | 0.2643 | 0.0551 | 0.035  |
| i       |    3765 | 0.0013 | 0.005  | 0.004  | 0.8717 | 0.1163 | 0.0008 | 0.0008 |
| e       |    3340 | 0.0512 | 0.006  | 0.0006 | 0.0003 | 0.0099 | 0.0617 | 0.8704 |
| d       |    2706 | 0.1035 | 0.0026 | 0      | 0      | 0.0015 | 0.0011 | 0.8914 |
| a       |    2702 | 0.0044 | 0.3927 | 0.0407 | 0.0152 | 0.5363 | 0.0074 | 0.0033 |
| k       |     486 | 0.1379 | 0.0761 | 0      | 0      | 0.0391 | 0      | 0.7469 |
| ch      |     309 | 0.0421 | 0.0097 | 0.0032 | 0      | 0.0162 | 0.0194 | 0.9094 |
| t       |     302 | 0.106  | 0.053  | 0.0033 | 0      | 0.0364 | 0.0033 | 0.798  |
| ckh     |     210 | 0.0476 | 0      | 0      | 0      | 0      | 0      | 0.9524 |
| l       |     104 | 0      | 0.0192 | 0      | 0      | 0.0481 | 0.2212 | 0.7115 |
| cth     |      81 | 0.037  | 0      | 0      | 0      | 0      | 0      | 0.963  |

Final two core glyphs:

| last2   |   total |    p_Ø |    p_l |    p_m |    p_n |    p_r |    p_s |    p_y |
|:--------|--------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| i·i     |    2317 | 0.0004 | 0.0017 | 0.0013 | 0.9547 | 0.0419 | 0      | 0      |
| e·d     |    2010 | 0.0876 | 0.0015 | 0      | 0      | 0.0015 | 0.0005 | 0.909  |
| e·e     |    1643 | 0.0487 | 0.003  | 0.0006 | 0      | 0.0067 | 0.0822 | 0.8588 |
| a·i     |    1448 | 0.0028 | 0.0104 | 0.0083 | 0.739  | 0.2355 | 0.0021 | 0.0021 |
| e·o     |    1409 | 0.2186 | 0.4216 | 0.0085 | 0      | 0.1959 | 0.1008 | 0.0546 |
| ch·o    |    1142 | 0.1217 | 0.4641 | 0.0131 | 0.0026 | 0.3249 | 0.0473 | 0.0263 |
| k·a     |     848 | 0      | 0.4434 | 0.0259 | 0.0153 | 0.5035 | 0.0083 | 0.0035 |
| ch·e    |     720 | 0.0361 | 0.0069 | 0      | 0      | 0.0153 | 0.0653 | 0.8764 |
| d·a     |     590 | 0.0068 | 0.3593 | 0.0407 | 0.0102 | 0.5763 | 0.0051 | 0.0017 |
| t·a     |     540 | 0.0037 | 0.4074 | 0.0519 | 0.0074 | 0.5185 | 0.0056 | 0.0056 |
| o·d     |     474 | 0.1603 | 0.0084 | 0      | 0      | 0.0021 | 0.0042 | 0.8249 |
| sh·o    |     448 | 0.308  | 0.4085 | 0.0089 | 0      | 0.2366 | 0.0246 | 0.0134 |
| sh·e    |     404 | 0.1064 | 0.0074 | 0.0025 | 0      | 0.0099 | 0.0272 | 0.8465 |
| k·o     |     327 | 0.055  | 0.6269 | 0.0122 | 0      | 0.2661 | 0.0275 | 0.0122 |
| t·o     |     321 | 0.0717 | 0.5607 | 0.0031 | 0      | 0.2741 | 0.028  | 0.0623 |
| k·e     |     315 | 0.0413 | 0.0159 | 0      | 0.0032 | 0.0159 | 0.0127 | 0.9111 |
| o·k     |     304 | 0.1382 | 0.0789 | 0      | 0      | 0.0493 | 0      | 0.7336 |
| o·t     |     240 | 0.1125 | 0.05   | 0      | 0      | 0.0458 | 0.0042 | 0.7875 |
| q·o     |     224 | 0.2277 | 0.6161 | 0      | 0      | 0.0893 | 0.0179 | 0.0491 |
| e·a     |     208 | 0      | 0.3894 | 0.0337 | 0.0096 | 0.5529 | 0.0096 | 0.0048 |

The automatically discovered Gate-B terminal clusters are visibly tied to rime/core shapes.
In particular the earlier `ai/aii -> n` and `e/ee -> y` zones are manifestations of a wider
cross-stem pattern.

## 5. Residual external information conditional on last-two-core shape

| feature   |   I_ending_feature_given_last2_bits |
|:----------|------------------------------------:|
| I         |                              0.081  |
| prev_end  |                              0.0613 |
| H         |                              0.059  |
| next_role |                              0.0589 |
| next_end  |                              0.0576 |
| prev_role |                              0.0518 |
| L         |                              0.0384 |

External context is not irrelevant. Therefore morphology is not ruled out.

But the dominant transferable organization is internal to the core/rime.

## Gate-B2 verdict

### Strongly supported

1. The major terminal classes are **core/rime-conditioned**.
2. This relationship generalizes to completely unseen stems.
3. The first interpretation should therefore be phonographic/phonotactic rather than
   ordinary declension/conjugation.
4. External grammatical/context information is a smaller additional layer.
5. Gate A's layout/notational realization is another distinct layer.

## Updated representation

    ONSET / PREFIX
        +
    CORE / RIME CLASS
        -> preferred TERMINAL CLASS
        + possible grammatical modulation
        + layout/state realization

This gives a three-layer explanation for terminal variation instead of forcing all visible
endings into one grammatical suffix system.

## Consequence

The phonographic working assumption is strengthened.

The final major structural gate before language search is now **Gate C**:

> do visible Voynich spaces behave like genuine linguistic boundaries?

If Gate C is positive, the representation can be frozen and the first constrained
historical-language campaign can begin.
