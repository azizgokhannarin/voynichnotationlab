# Campaign 2 — Production Instrument Calibration

Date: 2026-08-25

**Overall status: VALID — all five active branches passed the frozen calibration protocol.**

Positive criterion: 500 weak-surrogate draws, empirical `p < 0.01`. Negative criterion: must not pass; irreversible early failure occurs at the 5th null hit.

| Branch | Positive J | Null mean | Z_adv | positive p | Negative stop | Instrument |
|---|---:|---:|---:|---:|---:|---|
| ReF | 6.985175 | 7.625282 | 4.91 | 0.001996 | 35 draws / 5 hits | VALID |
| ReN | 7.474499 | 7.718480 | 4.80 | 0.001996 | 339 draws / 5 hits | VALID |
| BFM | 6.930965 | 7.726313 | 5.11 | 0.001996 | 13 draws / 5 hits | VALID |
| Dante | 5.494095 | 7.509891 | 16.65 | 0.001996 | 5 draws / 5 hits | VALID |
| Latin | 7.226436 | 7.403235 | 10.00 | 0.001996 | 7 draws / 5 hits | VALID |

Every positive calibration completed all 500 draws with **0 hits**, giving the empirical resolution floor `1/501 = 0.001996`.

Every matched negative reached five hits, making `p < 0.01` mathematically impossible even if every remaining draw were a miss. No negative calibration was therefore classified as a historical-language positive.

Raw calibration-null values SHA-256: `c18cf2e50527d8c49a50f8391a251c5596d72d6835180a1f32fbbd3647deb02e`

## Decision

The preregistered instrument-validity condition is satisfied. Campaign 2 may proceed to the real Voynich TRAIN/VALIDATION weak-surrogate and slot-grammar surrogate experiment. Final-test pages remain sealed.

Calibration regression SHA-256: `d30584fd3ae7e89a55640fe2b282dbefa20876baab6e16c2d39aaea0aad6a946`
