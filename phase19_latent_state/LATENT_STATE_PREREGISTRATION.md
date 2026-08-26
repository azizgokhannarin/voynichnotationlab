# Phase 19 small latent-state preregistration

Date frozen: 2026-08-26  
Voynich final-test pages used: **NO**

## Question

Does one binary line-level latent state improve lossless held-out prediction of
raw-token selection beyond a parameter-matched zero-state surface model?

This is a test of transferable hidden heterogeneity, not of language or
semantics. A state can represent scribal drift, layout regime, section/topic,
record type or procedural parameter wander.

## Frozen representation

- The source is the Phase-15 RF1b C1-STRUCT corpus with its unchanged page
  TRAIN/VALIDATION/final-test split.
- The observation vocabulary is the 32 most frequent exact TRAIN token types
  plus one `OTHER` symbol. No class induction or normalization is used.
- Visible emission context is the Cartesian product of five within-line
  position buckets and four line-length buckets.
- State is constant for one physical line and resets only at a page boundary.

The common spelling/identity side code for `OTHER` is identical under both
models and cancels in the codelength difference. Phase 19 therefore reports a
bounded categorical gain, not a replacement for the Phase-18 total residual
capacity bound.

## Frozen models

`K=1` is a layout-conditioned categorical model with Jeffreys 0.5 smoothing.

`K=2` is a binary line-state HMM:

- one state per physical line;
- a first-order transition matrix within each page;
- page-start state probabilities;
- state- and visible-context-conditioned categorical emissions;
- emissions shrunk toward the fitted `K=1` probabilities with concentration
  8.0;
- transition and initial probabilities smoothed by 1.0;
- two deterministic starts, maximum 30 EM iterations, tolerance `1e-7`
  nats/token.

Both models are fitted only on TRAIN. Primary gain is

`(K1 VALIDATION bits - K2 VALIDATION bits) / VALIDATION tokens`.

The 95% interval is a 2,000-replicate page bootstrap. Secondary prequential/MDL
gain uses five deterministic page blocks inside TRAIN: block 1 is warm-up and
each later block is coded by models fitted to all preceding blocks.

## Parameter-matched calibration

Before real VALIDATION is scored, fit `K=1` on real TRAIN and generate:

1. 100 independent **zero-state procedural null** TRAIN/VALIDATION pairs with
   identical page/line geometry, visible contexts, vocabulary size, fitting
   algorithm and model parameter counts;
2. one **injected-state positive control** with binary state persistence 0.90,
   balanced page starts and a deterministic hash partition of symbols whose
   state-matched emission odds are multiplied by 6.0.

The positive gate passes only if:

- all 100 null runs complete and their median held-out gain is `<= 0`;
- their empirical 99th percentile/max gain is `<= 0.02 bits/token`;
- injected-state held-out gain is at least `0.05 bits/token` and exceeds every
  null gain (`p = 1/101 <= 0.01`);
- injected-state prequential gain is positive;
- label-swap-invariant Viterbi state accuracy on positive VALIDATION is at least
  0.80;
- no final-test records are used.

If any gate fails, the instrument is uncertified and real Voynich VALIDATION is
not opened.

## Voynich decision rule

A robust small-state signal requires all three conditions:

1. observed held-out gain exceeds the frozen null 99th percentile;
2. page-bootstrap 95% lower bound is greater than zero;
3. TRAIN-only prequential/MDL gain is positive.

If all hold, only the parameter-matched `K=1` zero-state mechanism is rejected.
The result does not rank `H_C`, `H_D` or `H_G`. If any condition fails, Phase 19
does not detect transferable binary line state; larger state spaces are not
authorized automatically.

No new language search, semantic/illustration crib, representation change or
generator enrichment is permitted. All final-test partitions remain sealed.

