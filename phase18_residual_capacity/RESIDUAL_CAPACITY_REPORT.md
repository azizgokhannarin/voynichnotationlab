# Phase 18 residual information-capacity report

Date: 2026-08-26  
Voynich final-test pages used: **NO**  
Hypothesis ranking performed: **NO**

## Scope

This phase asks how many lossless code bits remain after a bounded surface-only
model has been selected inside TRAIN and frozen. The result is an **upper bound**
on possible hidden-content bandwidth. It is not evidence that the residual bits
are content; they may instead be procedural innovation, noise or model
misspecification.

All four candidate codes preserve exact strings. TRAIN types seen fewer than
twice and all unseen VALIDATION strings are encoded through an explicit ESC plus
UTF-8 byte-bigram spelling code. No free `UNK` collapse is used.

## Positive calibration

The exact Phase-15 LatinISE source was rendered with heavy suspension: each
normalized word became its onset plus a generic suspension mark, with a visible
line-final variant. Source order was preserved and only Voynich TRAIN line
lengths supplied layout geometry; no Voynich token identity entered the control.

| Measure | Result |
|---|---:|
| VALIDATION lines / tokens | 840 / 6,086 |
| Hidden word types / surface types | 2,919 / 35 |
| Hidden-to-surface type ratio | 83.4 |
| Mean surface length | 2.215 codepoints |
| Exact adjacent-repeat rate | 0.0566 |
| Non-identical edit-distance-1 adjacency | 0.7978 |
| Selected bounded surface model | `LAYOUT_OPEN` |
| Residual-capacity upper bound | 3.978 bits/token |
| 95% bootstrap CI | 3.953–4.004 |
| Recoverable hidden-onset information | 3.555 bits/token |
| Permutation p | 0.000999 |

All five preregistered positive gates passed. The estimator therefore detects
ample known hidden information after an intentionally many-to-one renderer and
is certified for the frozen Voynich VALIDATION run.

## Voynich VALIDATION

Candidate selection occurred on a deterministic page partition wholly inside
TRAIN. `UNIGRAM_OPEN` achieved the smallest internal selection loss and was
refit on all 3,155 TRAIN lines / 22,716 TRAIN tokens before VALIDATION scoring.

| Measure | Result |
|---|---:|
| VALIDATION lines / tokens | 1,024 / 7,596 |
| Selected bounded surface model | `UNIGRAM_OPEN` |
| Residual-capacity upper bound | 12.372 bits/token |
| 95% bootstrap CI | 12.174–12.574 |
| Total residual codelength | 93,977.94 bits |
| Mean / median bits per line | 91.78 / 91.86 |
| 95th-percentile bits per line | 163.00 |
| Dictionary escape rate | 0.2292 |

The preregistered content-rich `H_C` falsifier required the **upper** bootstrap
bound to be below 1 bit/token. The observed upper bound is 12.574 bits/token, so
Phase 18 does **not** reject content-rich `H_C`.

## Interpretation boundary

The result establishes that the frozen bounded surface model does not compress
Voynich token selection to a low-bandwidth remainder. It does not establish that
12.372 bits/token are meaningful or independently available to a hidden source.
The looseness can include productive vocabulary, spelling cost, omitted surface
mechanisms and ordinary model error.

Consequently:

1. `H_C`, `H_D` and `H_G` remain open and unranked.
2. No language, key, semantic or illustration search is reopened.
3. No generator is enriched in this checkpoint.
4. All 46 Voynich final-test pages and every control final-test record remain
   sealed.

## Next frozen stage

The remaining scheduled experiment is a small latent-state test. It must be
preregistered, parameter-matched and calibrated on zero-state procedural null
generators; held-out predictive gain is primary and prequential/MDL gain is a
secondary complexity check. A positive gain alone will not be interpreted as
content, because scribe drift, layout and topic-free parameter wander can also
produce latent state.
