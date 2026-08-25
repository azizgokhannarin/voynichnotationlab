# French calibrated attack and three-language convergence

Date: 2026-08-26

Final-test manuscript pages used: **NO**.

## French positive control

- mapping recovery: **89.2%**
- held-out exact-token recovery: **96.5%**
- LM z vs random bounded keys: **17.82**
- phrase bigram z: **76.59**
- phrase trigram z: **203.57**

## Voynich -> French

- validation LM z vs random: **7.45**
- lexical hit rate: **42.36%**
- phrase bigram z: **0.92**
- phrase trigram z: **2.00**
- attested validation trigrams: **2**
- longest attested-bigram chain: **5**

The trigram z is close to 2 but is supported by only two attested trigrams and is not accompanied
by a strong bigram effect. It is not treated as a coherent-language breakthrough.

**Decision:** close simple/bounded-homophonic French substitution at the frozen-unit/fixed-boundary level.

## Common-objective comparison

| Target | LM z | Lexical hit | Phrase bigram z | Phrase trigram z |
|---|---:|---:|---:|---:|
| German ReF | 7.83 | 62.0% | 1.60 | 1.27 |
| German ReN | 8.54 | 47.4% | 0.86 | -0.26 |
| Italian | 6.93 | 31.8% | -0.06 | -0.61 |
| French | 7.45 | 42.4% | 0.92 | 2.00 |

Across these branches:
- LM-z mean **7.69**, SD **0.68**
- LM-z range **6.93–8.54**
- phrase-bigram-z mean **0.83**
- phrase-trigram-z mean **0.60**

## Interpretation

German, Italian and French now show the same qualitative signature under one calibrated attack:
strong optimized target-LM fit and many dictionary hits, but held-out phrase order near line-local
shuffle. Genuine positive controls instead produce very large phrase-order effects.

This repeated signature is evidence against the shared model—one frozen Voynich unit emitting one
phonographic target unit with bounded homophony and fixed word-like boundaries—rather than
evidence favoring any one of these languages.

Further languages can be used as confirmation controls, but the main unresolved question has
shifted from target-language choice to which shared notation assumption is wrong.
