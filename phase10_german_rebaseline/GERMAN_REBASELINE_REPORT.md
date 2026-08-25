# German re-baseline under the common boundary-aware objective

Date: 2026-08-26

Final-test Voynich pages used: **NO**.

The German branches were rerun using the same continuous explicit-word-boundary trigram objective
used by the calibrated Italian attack. The mapping model remains deterministic with bounded
homophony (maximum three source units per target), with no nulls, context-sensitive values,
arbitrary expansions, or word-specific exceptions.

## Known-German positive controls

### ReF
- mapping recovery: **86.5%**
- held-out exact-token recovery: **70.1%**
- phrase bigram lift: **z=70.18**
- phrase trigram lift: **z=85.83**

### ReN
- mapping recovery: **91.9%**
- held-out exact-token recovery: **80.3%**
- phrase bigram lift: **z=94.21**
- phrase trigram lift: **z=140.56**

The corrected common objective therefore strongly recognizes genuine bounded-homophonic German.

## Voynich -> ReF

- validation LM advantage vs random bounded keys: **z=7.83**
- validation lexical hit rate: **62.05%**
- longest lexical run: **12**
- longest attested-bigram chain: **3**
- phrase bigram lift: **z=1.60**
- phrase trigram lift: **z=1.27**

## Voynich -> ReN

- validation LM advantage vs random bounded keys: **z=8.54**
- validation lexical hit rate: **47.41%**
- longest lexical run: **12**
- longest attested-bigram chain: **3**
- phrase bigram lift: **z=0.86**
- phrase trigram lift: **z=-0.26**

## Interpretation

The boundary-aware objective actually makes Voynich easier to fit to German at the raw LM /
dictionary level. This does not rescue the language hypothesis.

Genuine German controls produce enormous held-out phrase-order effects. Voynich does not:
its best phrase effects remain small, and coherent attested-bigram chains stop at three words.

Therefore the previous closure of simple/bounded-homophonic German substitution at the
frozen-unit/fixed-boundary level remains valid under the same objective used for Italian.

## Current cross-language pattern

German and Italian already show the same qualitative signature:

1. optimizer finds a strong target-LM basin relative to random keys;
2. many target-language dictionary words can be manufactured;
3. genuine positive controls produce very large phrase-order effects;
4. Voynich held-out phrase order remains weak / near shuffle.

French is the preregistered third independent language target. After French, this repeated
signature should be evaluated as a possible property of the encoding model rather than of any
one candidate language.
