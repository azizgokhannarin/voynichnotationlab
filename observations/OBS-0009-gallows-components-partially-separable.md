# OBS-0009 — Gallows components are partially separable, not proven phonetic

Five-fold page-held-out tests show:

- full analytical-stroke and atomic-EVA representations have essentially tied best
  predictive compression;
- the published gallows 2x2 decomposition is the best/tied-best structural
  factorisation among possible pairings;
- a two-component gallows predictor loses only ~1.8% log-loss relative to a full
  four-class predictor while using about half the output coefficients;
- the `p/f` (X-side) component is strongly enriched at token and line starts;
- the other component varies more strongly with Currier state.

Interpretation: functional compositionality is plausible, but individual sub-strokes
cannot yet be assigned independent sounds.
