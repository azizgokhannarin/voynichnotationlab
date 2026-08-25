# Transformation-layer probe 1 — Boundary operator graph

Date: 2026-08-25

Status: **STRUCTURAL REASSESSMENT; LANGUAGE-INDEPENDENT**

Final-test pages used: **NO**

## Question

Do recurrent near-duplicate Voynich tokens support a small, transferable dictionary of
boundary transformations such as `A↔B`, consistent with a simple surface-transformation layer?

This test does not assign sounds or meanings.

## Global adjacency enrichment

On TRAIN pages, same-length adjacent tokens differing at exactly one frozen unit were compared
with 300 line-local token-order permutations.

| Difference position | Observed | Null mean | z |
|---|---:|---:|---:|
| first unit | 340 | 292.73 | 3.56 |
| final unit | 111 | 90.66 | 2.79 |
| internal unit | 88 | 90.36 | -0.29 |

Thus the previously observed adjacency effect is specifically concentrated at token boundaries,
not in arbitrary internal substitutions.

## Held-out transfer

TRAIN operator edges were then used to predict which boundary-unit pairs occur around the same
core on VALIDATION pages.

### Initial boundary
- TRAIN edges with >=3 distinct cores: **244**
- recurrent on VALIDATION: **226**
- transfer: **92.6%**
- raw pair-support AUC: **0.934**
- marginal-frequency baseline AUC: **0.944**
- pair-specific lift AUC: **0.539**

### Terminal boundary
- TRAIN edges with >=3 distinct cores: **129**
- recurrent on VALIDATION: **110**
- transfer: **85.3%**
- raw pair-support AUC: **0.923**
- marginal-frequency baseline AUC: **0.903**
- pair-specific lift AUC: **0.556**

## Interpretation

Two distinct statements must be separated.

### Supported

1. Near-duplicate adjacency is not random.
2. The excess is boundary-specific.
3. The set of boundary units involved is highly stable between TRAIN and VALIDATION.
4. Terminal variation is especially concentrated: the top 20 terminal edges account for
   **63.3%** of TRAIN terminal edge support.

This reinforces a small boundary/slot vocabulary.

### Not supported

The held-out predictive power of **specific transformation pairs after removing marginal unit
frequency is weak**:

- initial pair-specific AUC: **0.539**
- terminal pair-specific AUC: **0.556**

An AUC near 0.5 means that knowing that a particular pair such as `QO↔o` was unusually associated
on TRAIN adds little held-out information beyond knowing that `QO` and `o` are simply common
boundary units.

Therefore the data do **not** presently support a fixed pairwise operator dictionary of the form:

    QO <-> o
    r  <-> l
    CH <-> SH

as a transformation cipher.

The stronger statement supported by the data is instead:

> a restricted and transferable set of units occupies/change at boundary slots around recurrent
> cores.

That pattern is compatible with morphology, positional notation, abbreviation/state realization,
or a more general transformation layer. This probe does not distinguish those mechanisms.

## Consequence

Do not promote individual boundary substitutions to decoding rules.

The next structural question, if pursued, should concern whether recurrent cores plus boundary
classes can be compressed into a generative template with fewer latent states—not whether a
specific surface pair is a fixed substitution operator.

The simple `A-X-A` bird-language-like expansion hypothesis was already weakened by the lag-repeat
probe; this operator-graph test further weakens the simplest fixed boundary-transformation version
without ruling out more complex notation transforms.
