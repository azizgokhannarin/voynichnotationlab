# Italian calibrated bounded-homophonic attack

Date: 2026-08-25

Final-test pages used: NO.

## Engine calibration correction
The first Italian control exposed that the previous token-reset trigram objective could optimize token-internal phonotactics without reliably locating the true Italian key. Before Voynich Italian scoring, the fitness was replaced by a continuous explicit-word-boundary PHONO-OIT trigram objective.

Known Italian control mapping recovery: 91.9%
Known Italian held-out exact-token recovery: 98.8%
Known Italian phrase bigram z: 102.77
Known Italian phrase trigram z: 303.17

## Voynich validation
LM z vs random bounded keys: 6.93
Lexical hit rate: 31.85%
Longest lexical run: 7
Longest attested-bigram chain: 5
Phrase bigram z: -0.06
Phrase trigram z: -0.61
Attested validation trigrams: 0

Decision: CLOSE_SIMPLE_BOUNDED_HOMOPHONIC_ITALIAN_AT_FROZEN_UNIT_FIXED_BOUNDARY_LEVEL

The cross-language convergence table is now tracked explicitly. If the next calibrated language shows the same qualitative pattern—strong generic LM fit / lexical hits but no held-out phrase-order emergence—the single-phonographic-unit mapping model itself becomes the more likely failure point.
