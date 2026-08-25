# Latin preregistered confirmation and direct-language-search closure

Date: 2026-08-26

Final-test Voynich pages used: **NO**.

## Purpose

Latin was not run as another exploratory attempt to find a language. It was preregistered as a
confirmation test of the cross-language convergence already observed for German, Italian, and
French.

Prediction before the run:

- Voynich Latin-LM z: **6.5–9.0**
- held-out phrase bigram/trigram z: approximately **-1.0–2.5**
- reopen direct Latin identification only if **both bigram and trigram z >= 5**, with multiple
  distinct held-out attested n-grams.

## Positive control

A genuine normalized medieval-Latin passage was encoded into the same matched 37-symbol,
max-3-homophonic cipher and attacked blindly.

- mapping recovery: **94.6%**
- held-out exact-token recovery: **98.5%**
- LM z vs random bounded keys: **18.85**
- phrase bigram z: **120.47**
- phrase trigram z: **384.94**

The instrument therefore has excellent power for genuine Latin under the tested representation.

## Voynich -> Latin

Observed validation:

- LM z vs random bounded keys: **7.72**
- lexical hit rate: **38.88%**
- longest lexical run: **10**
- longest attested-bigram chain: **4**
- phrase bigram z: **0.14**
- phrase trigram z: **0.30**
- attested validation trigrams: **2**

The result falls squarely inside the preregistered generic-fit prediction and nowhere near the
Latin-reopen threshold.

## Four-target comparison

| Target | Voynich LM z | Lexical hit | Phrase bigram z | Phrase trigram z |
|---|---:|---:|---:|---:|
| German ReF | 7.83 | 62.0% | 1.60 | 1.27 |
| German ReN | 8.54 | 47.4% | 0.86 | -0.26 |
| Italian | 6.93 | 31.8% | -0.06 | -0.61 |
| French | 7.45 | 42.4% | 0.92 | 2.00 |
| Latin | 7.72 | 38.9% | 0.14 | 0.30 |

Across all five historical branches:

- LM-z mean: **7.69**
- LM-z SD: **0.59**
- LM-z range: **6.93–8.54**
- phrase-bigram-z mean: **0.69**
- phrase-trigram-z mean: **0.54**

## Interpretation

The Latin run converts the previous post-hoc cross-language observation into a successful
preregistered prediction.

A fourth independent historical language again shows the same signature:

1. a strong optimized target-language LM improvement over random bounded keys;
2. many genuine target-language dictionary forms;
3. no corresponding held-out target-language phrase order.

Known-language positive controls produce phrase z values in the tens to hundreds under the same
pipeline, so this is not a low-power failure.

The evidence now supports a model-level conclusion:

> the frozen Voynich-unit, one-unit-to-one-phonographic-target, max-3-homophonic,
> fixed-word-like-boundary representation is not a useful direct language-identification layer.

This conclusion is stronger than rejection of German, Italian, French, or Latin individually.

## Decision

**STOP direct language search at this representation level.**

Spanish, Middle English, Dutch, or additional lexicons should not be run under the same direct
mapping merely to look for a winner. Such runs have low expected information gain and invite
phonotactic overfitting.

The next work should discriminate:

- natural language behind a substantial transformation / representation layer;
- procedural or template-generated structured text.

The v4.1 language-agnostic results already provide the starting point: strong immediate local
class ordering, rapid decay at larger lags, and strong line awareness.

The sealed final-test pages remain untouched.
