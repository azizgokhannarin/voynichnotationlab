# Representation-layer diagnostics

Date: 2026-08-26

Final-test Voynich pages used: **NO**.

This phase follows the three-language convergence result. It asks whether the recurring signature

> high target-LM fit + many lexical hits + near-zero phrase-order lift

can be explained merely by using the wrong token boundaries / granularity, and whether Voynich
contains language-like sequential dependency without assuming any target language.

## Experiment 1 — controlled representation distortion

Known historical ReF and Italian plaintext were deliberately segmented incorrectly before any
language identification claim.

Two deterministic distortions were tested:

1. syllable-like chunks;
2. core + terminal-ending chunks.

The true plaintext phonographic units were retained. The distorted chunks were then evaluated as
if they were orthographic words against the original historical language phrase statistics.

### Results

| Language | Distortion | chunks/word | lexical hit | bigram z | trigram z |
|---|---|---:|---:|---:|---:|
| ReF | syllable-like | 1.61 | 92.2% | 24.43 | 54.74 |
| ReF | core+ending | 1.48 | 89.6% | 7.59 | 47.64 |
| Italian | syllable-like | 1.87 | 81.9% | 14.00 | 30.34 |
| Italian | core+ending | 1.49 | 80.0% | 16.31 | 45.14 |

The key negative result is that **mild deterministic mis-segmentation did not reproduce the
Voynich signature**. Genuine natural-language phrase order remained strongly detectable even when
orthographic words were split into these smaller chunks.

Therefore:

> "Voynich spaces are merely syllable/morpheme boundaries" is not, by itself, sufficient to
> explain the observed loss of phrase coherence.

This does not reject a more substantial transformation layer that also inserts, reorders,
duplicates, abbreviates, or otherwise changes the relation between surface tokens and plaintext
words.

## Experiment 2 — language-agnostic sequential dependency

No candidate language or substitution mapping is used.

Token identity mutual information was measured by lag within real Voynich lines and compared with
matched ReF/Italian word-level and syllable-like streams. Because raw plug-in MI is strongly
biased for large vocabularies at long lag, the reported interpretation uses matched permutation
bias correction.

### Bias-corrected token MI

Excess MI over the matched independence null:

| Stream | lag 1 | lag 2 | lag 5 |
|---|---:|---:|---:|
| Voynich | 0.094 | 0.016 | -0.030 |
| ReF words | 0.402 | 0.113 | -0.001 |
| ReF syllable-like | 0.969 | 0.240 | -0.008 |
| Italian words | 0.743 | 0.113 | -0.019 |
| Italian syllable-like | 0.950 | 0.297 | -0.006 |

Voynich has real adjacent-token dependency, but it is substantially weaker than the word-level
historical references and rapidly decays.

### Line-boundary diagnostic

Permutation-bias-corrected excess token MI:

| Stream | within-line lag 1 | across line boundary |
|---|---:|---:|
| Voynich | 0.108 | 0.015 |
| ReF words | 0.460 | 0.238 |
| Italian words | 0.812 | 0.506 |

Voynich's measurable dependency is strongly line-local: the excess drops from about
0.108 inside lines to about
0.015 across line boundaries.

The historical reference lines here are artificial matched-length cuts, so their linguistic
sequence naturally continues across those cuts. This contrast is therefore evidence for a
line-aware Voynich surface mechanism, not a direct language-identification statistic.

## Experiment 3 — induced token-class grammar

Frequent Voynich token types were clustered only from their left/right distributional contexts.
The class assignment was then frozen and the real class sequence compared with 200 line-local
token shuffles.

Voynich class-MI shuffle z by lag:

- lag 1: **30.62**
- lag 2: **2.36**
- lag 3: **-0.32**
- lag 4: **-1.17**
- lag 5: **-1.27**

Matched word-level references:

- ReF: 138.62, 26.02, 3.89, -1.60, -0.36
- Italian: 190.05, 29.25, 1.95, -2.69, -3.19

Thus Voynich has a **very strong immediately adjacent class-order constraint**, a weak lag-2
effect, and no positive class-order signal from lag 3 onward. ReF and Italian word streams show
much stronger lag-1 and lag-2 class structure and retain some positive lag-3 structure.

## Interpretation

Three conclusions are warranted.

### 1. Simple boundary mismatch is insufficient

Splitting real natural-language words into plausible smaller chunks does not collapse historical
phrase order to the Voynich level. A surviving natural-language hypothesis therefore needs a
more consequential representation/transformation layer than merely "spaces are syllable
boundaries."

### 2. Voynich is sequentially structured, but mainly locally

The stream is not shuffled noise. Adjacent token classes have a highly significant ordering
constraint. But the structure decays much faster than the matched natural-language word streams.

### 3. The visible layer is strongly line-aware

Sequential dependency nearly disappears across Voynich line boundaries. This is consistent with
a surface generation / notation mechanism that treats the line as a meaningful production unit.

These results **do not prove pseudo-text**. They increase the plausibility of a procedural or
templatic surface generator, but a natural-language plaintext behind a stronger transformation
layer remains viable.

A conventional constructed language is not specifically supported: a content-bearing grammar
would normally be expected to leave language-agnostic class-order structure extending beyond
immediate adjacency, though the present test cannot exclude unusual grammars.

## Updated hypothesis ordering

1. Natural language behind a substantial systematic transformation / representation layer.
2. Procedural or template-generated structured text.
3. Constructed language with its own grammar.
4. Genuinely unknown natural language.

The gap between (1) and (2) is now smaller than before.

## Next decision

A fourth language is no longer needed to discover a language by lexical search. If Latin is run,
it should be a **preregistered confirmation prediction** only:

- expected Voynich LM z under the current direct-mapping model: roughly 6.5--9;
- expected phrase bigram/trigram z: near the existing null band;
- only a replicated, held-out sequence effect (e.g. both bigram and trigram z >= 5 with multiple
  distinct attested n-grams) should reopen direct language identification.

After that confirmation, direct language search at this representation level should stop.
