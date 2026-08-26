# Phase 19 calibrated small latent-state report

Date: 2026-08-26  
Voynich final-test pages used: **NO**  
Hypothesis ranking performed: **NO**

## Question and model

Phase 19 asks whether one binary state shared by all tokens on a physical line
improves transferable prediction beyond a matched zero-state surface model.
Exact TRAIN token identity is preserved for the 32 most frequent types; all
remaining identities share `OTHER`. Both models observe the same five
within-line position buckets and four line-length buckets.

The `K=1` model has 640 free emission parameters. The binary line-HMM has 1,283
free parameters including state emissions, page-start probabilities and
within-page transitions. It is fitted only on TRAIN. Held-out gain is primary;
a five-block TRAIN-only prequential code is the secondary complexity check.

## Calibration before interpretation

One hundred zero-state procedural corpora were generated from the Voynich
TRAIN-fitted `K=1` model with identical TRAIN/VALIDATION geometry, vocabulary,
contexts and fit procedure. A separate positive control injected a persistent
binary state with frozen transition persistence 0.90 and emission odds
multiplier 6.0.

| Calibration measure | Result |
|---|---:|
| Zero-state replicates | 100 |
| Zero-state median gain | -0.04133 bits/token |
| Zero-state q95 | -0.03117 bits/token |
| Zero-state q99 / maximum | -0.02685 bits/token |
| Injected-state held-out gain | +0.57683 bits/token |
| Injected-state empirical p | 0.009901 |
| Injected-state prequential gain | +0.54875 bits/token |
| Injected-state Viterbi accuracy | 99.02% |

All preregistered gates passed. The added-state model did not generate spurious
held-out gain on any zero-state replicate and recovered the deliberately
injected state strongly.

## Voynich VALIDATION

Only after certification were the 45 frozen VALIDATION pages scored.

| Measure | Result |
|---|---:|
| TRAIN pages / lines / tokens | 136 / 3,155 / 22,716 |
| VALIDATION pages / lines / tokens | 45 / 1,024 / 7,596 |
| Raw held-out `K=2 - K=1` gain | +0.00432 bits/token |
| Page-bootstrap 95% CI | -0.02051 to +0.02827 |
| Zero-state q99 | -0.02685 bits/token |
| TRAIN-only prequential/MDL gain | -0.06020 bits/token |
| Fitted state-0 self-transition | 0.97449 |
| Fitted state-1 self-transition | 0.98145 |

The point estimate exceeds the synthetic null q99, but two required gates fail:
the page-bootstrap interval includes zero and every prequential block has a
negative gain. The high fitted persistence is therefore not independently
transferable evidence; it is consistent with fitting stable-looking regimes in
TRAIN that do not pay for their complexity on new page blocks.

## Decision

The frozen rule required all three conditions: held-out gain above the null
q99, positive bootstrap lower bound and positive prequential gain. Only the
first holds.

> No robust transferable binary line-state signal is detected under the frozen
> 32+OTHER representation and model.

This result is intentionally bounded:

1. It does not prove that Voynich has no hidden states of any kind.
2. It does not authorize increasing `K`, changing representation or enriching a
   generator in response to the negative result.
3. A positive state result would not have proved language or semantics.
4. `H_C`, `H_D` and `H_G` remain open and unranked.
5. All 46 final-test pages remain sealed.

## Next stage

The preregistered internal-evidence sequence is now complete through the first
small latent-state test. The next task is a cross-phase synthesis and explicit
identifiability/stop-rule audit. It must determine which conclusions are
calibrated, which hypotheses remain observationally equivalent, and whether any
new representation or final confirmatory test is scientifically justified
before final-test pages can be considered.
