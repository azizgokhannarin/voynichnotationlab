# German Final Attack v1 — Bounded-Homophonic Full-Key Test

Frozen and executed: 2026-08-25

## Scope

This is the final test of a narrow hypothesis:

> the frozen Voynich units encode historical German by a deterministic one-target-per-source
> substitution, allowing bounded source homophony, while visible Voynich spaces act as fixed
> word-like generative boundaries.

This does **not** test arbitrary German encodings.

## Changes justified before the final attack

Five independent cryptanalytic reviews converged on a false-negative risk in the previous
strict-injective/greedy attack.

The final test therefore makes one central relaxation:

- source->target remains deterministic;
- multiple source units may share one target;
- maximum multiplicity is 3 source units per target.

Still prohibited:

- NULL/silent units;
- one-source->multiple-target expansion;
- context-sensitive mappings;
- lexical exceptions;
- semantic/illustration anchors;
- arbitrary token merging/splitting.

ReF and ReN are evaluated separately.

## Step 0

Before key search, compare label-invariant distributional properties:

- inventory size;
- sorted unigram spectrum;
- unigram entropy;
- within-token conditional entropy.

Result:
- Voynich inventory: 37
- PHONO-WG inventory: 19 for both ReF and ReN

Therefore a complete strict-injective 37->19 key is impossible by the pigeonhole principle.
The earlier injective attack was not a fair full-key test.

Voynich conditional entropy is also substantially lower:
- Voynich: 2.385696 bits
- ReF: 3.033878 bits
- ReN: 2.719836 bits

This is a warning sign, not an automatic rejection, because homophonic surface symbols can alter
the source-side entropy structure.

## Solver

A full-key stochastic optimizer is used:
- German trigram language model;
- add-0.25 smoothing;
- all 37 source units assigned;
- 19 PHONO-WG targets;
- max target multiplicity 3;
- random restarts;
- simulated annealing with score-scale-calibrated temperature;
- TRAIN only for key optimization;
- frozen key applied unchanged to VALIDATION.

The optimizer does not require unique lexical completions and is not seeded exclusively by cribs.

## Instrument calibration

Known historical German passages are encoded into a 37-symbol bounded-homophonic source alphabet.
The solver does not receive the key.

ReN positive control:
- recovered source mapping: 78.4%
- held-out exact token recovery: 55.4%
- validation LM advantage vs random bounded keys: z ~= 5.42
- phrase bigram lift vs within-line shuffle: z ~= 37.72
- phrase trigram lift: z ~= 128.71

ReF positive control:
- recovered source mapping: 75.7%
- held-out exact token recovery: 34.7%
- validation LM advantage vs random bounded keys: z ~= 5.79
- phrase bigram lift: z ~= 11.71
- phrase trigram lift: z ~= 31.05

Thus the instrument can detect and substantially recover a genuine bounded-homophonic German
cipher and, critically, recovered German produces overwhelming held-out phrase-order coherence.

## Voynich full-key result

### ReF model

TRAIN trigram loss:
    3.860433 bits/event

VALIDATION trigram loss:
    3.840284 bits/event

Random bounded-key validation:
    mean 7.192930, sd 0.661507

Optimized-key validation advantage:
    z = 5.07

Lexical VALIDATION:
- 3603 / 7596 tokens are attested ReF normalized words (47.43%)
- longest lexical run: 11

But phrase order:
- attested bigram rate: 0.05871
- line-shuffle mean: 0.06277
- bigram z: **-0.84**
- attested validation trigrams: 1
- trigram z: **0.49**
- longest attested-bigram chain: 3

### ReN model

TRAIN trigram loss:
    3.741643 bits/event

VALIDATION trigram loss:
    3.722923 bits/event

Random bounded-key validation:
    mean 6.916135, sd 0.567406

Optimized-key validation advantage:
    z = 5.63

Lexical VALIDATION:
- 2643 / 7596 tokens are attested ReN normalized words (34.79%)
- longest lexical run: 8

But phrase order:
- attested bigram rate: 0.07166
- line-shuffle mean: 0.06674
- bigram z: **0.70**
- attested validation trigrams: **0**
- trigram z: **-0.15**
- longest attested-bigram chain: 5

## Interpretation

The full-key optimizer can force the Voynich token-internal structure into a German trigram basin
far better than random keys. That fact is not sufficient evidence for German.

The decisive contrast is the calibrated phrase-order behavior.

When the same solver is applied to genuine German encoded under the same bounded-homophonic
mechanism, held-out German phrase order emerges explosively (bigram z 11.7--37.7; trigram z
31--129).

For Voynich, despite thousands of apparent dictionary words and long lexical runs, the original
token order is statistically indistinguishable from line-local shuffle under both German corpora.

This is exactly the signature expected when a flexible optimizer creates German-looking words
without recovering an underlying German sentence sequence.

## Decision

**CLOSE** the following hypothesis:

> Simple or bounded-homophonic historical German substitution at the frozen Voynich-unit level,
> with one target unit emitted per source unit and visible Voynich boundaries treated as fixed
> word-like boundaries.

No further German key search should be used to rescue this model.

## What is NOT rejected

This result does not establish that the manuscript cannot contain German under a different
encoding model.

Still open conceptually:
- source-unit granularity may be wrong;
- one source unit may encode a syllable/digraph/abbreviation;
- some boundary units may be grammatical/notational rather than phonographic;
- visible boundaries may not equal orthographic German words;
- a transformation layer may precede phonographic interpretation.

Those are different hypotheses and must not be introduced post hoc into this closed attack.

Final-test manuscript pages were not used.
