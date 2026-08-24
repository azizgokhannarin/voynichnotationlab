# Gate C — Are visible Voynich spaces meaningful generative boundaries?

Date: 2026-08-24

## Goal

All previous token-level work assumes that visible manuscript spaces mark meaningful
segmentation points.

Gate C hides the spaces from the statistical model.

Each manuscript line is converted into one continuous EVA-glyph stream. Every possible
inter-glyph cut is then scored using statistics learned on other pages.

No language, dictionary, token identity, or visible-space label is used to construct the
boundary scores.

## Scores

For each possible cut:

- forward branching entropy from left glyph contexts;
- backward branching entropy from right glyph contexts;
- cross-cut glyph-transition surprisal.

Five-fold **whole-page holdout** is used.

## 1. Can true spaces be distinguished from internal cuts?

| metric          |   AUC_true_space_vs_internal |
|:----------------|-----------------------------:|
| branch2         |                       0.8333 |
| branch1         |                       0.8327 |
| branch3         |                       0.8055 |
| cross_surprisal |                       0.7368 |

Chance:

    AUC = 0.50

Best single metric:

    branch2 = **0.833**

Thus real manuscript spaces occur at substantially different glyph-statistical environments
from ordinary cuts inside visible tokens.

## 2. Page-level robustness

| metric          |   pages |   mean_page_AUC |   median_page_AUC |   ci95_low |   ci95_high |   pages_above_0_5_pct |
|:----------------|--------:|----------------:|------------------:|-----------:|------------:|----------------------:|
| branch1         |     227 |          0.8467 |            0.847  |     0.8408 |      0.8524 |              100      |
| branch2         |     227 |          0.836  |            0.8417 |     0.8306 |      0.841  |               99.5595 |
| branch3         |     227 |          0.8002 |            0.8115 |     0.7929 |      0.8066 |               99.5595 |
| cross_surprisal |     227 |          0.7293 |            0.7353 |     0.7221 |      0.7366 |              100      |

The bootstrap unit is the manuscript page, not the individual glyph cut.

This guards against pseudo-replication from thousands of cuts on the same pages.

## 3. Score distributions

| metric          |   space_mean |   internal_mean |   space_median |   internal_median |   mean_delta |
|:----------------|-------------:|----------------:|---------------:|------------------:|-------------:|
| branch1         |       3.0329 |          2.413  |         3.1434 |            2.5354 |       0.6199 |
| branch2         |       2.8829 |          2.1848 |         2.963  |            2.3057 |       0.698  |
| branch3         |       2.6953 |          2.0214 |         2.7795 |            2.1257 |       0.6738 |
| cross_surprisal |       3.3863 |          2.3468 |         2.8934 |            2.0142 |       1.0395 |

## 4. Blind retrieval at the manuscript's true boundary rate

The algorithm is told only how many cuts to select, not which cuts are spaces.

| metric          |   boundary_prevalence |   top_k |   precision |   recall |
|:----------------|----------------------:|--------:|------------:|---------:|
| branch1         |                0.2001 |   32588 |      0.6515 |   0.6515 |
| branch2         |                0.2001 |   32586 |      0.5669 |   0.5669 |
| branch3         |                0.2001 |   32531 |      0.5242 |   0.5234 |
| cross_surprisal |                0.2001 |   32588 |      0.3491 |   0.3491 |

## 5. Boundary strength is graded

For the best metric:

- 95.6% of true spaces exceed the
  median internal-cut score;
- 54.3% exceed the 90th percentile of
  internal cuts.

This matters because the correct conclusion is not that all spaces are identical.

Some may be strong lexical boundaries; others may be weaker clitic, morpheme, prosodic,
or notation boundaries.

## Gate-C verdict

### Supported

Visible Voynich spaces are **meaningful generative boundaries**. They are recoverable
above chance from the continuous glyph stream itself on pages not used to estimate the
statistics.

Therefore the token level used in the project is not merely an arbitrary transcription
convenience.

### Not established

A visible Voynich space is not thereby proven to equal a modern orthographic word boundary.

The manuscript may package:

- words;
- clitic groups;
- morphemes;
- phonographic units;
- prosodic units

with related but non-identical spacing rules.

## Structural gates A–C: consolidated model

The first structural campaign now supports:

1. visible spaces are meaningful generative boundaries;
2. `QO` and `DA` remain strong block/onset candidates;
3. `DY` is not an indivisible unit;
4. final `y` belongs to a productive terminal-feature layer;
5. residual terminal choice is strongly core/rime-conditioned and transfers to unseen stems;
6. EVA `m` has an exceptional physical-line-final realization component;
7. external grammatical context is secondary but nonzero;
8. `or/s/r` is a stable functional-paradigm candidate, not a claimed pronoun set;
9. gallows remain atomic token units with separately modelled internal features.

## Decision

**Gate C passes.**

The structural representation can now be frozen for the first constrained
historical-language campaign.

Any future segmentation change must be evaluated as a separate preregistered ablation and
must not be introduced merely to rescue a poor language match.
