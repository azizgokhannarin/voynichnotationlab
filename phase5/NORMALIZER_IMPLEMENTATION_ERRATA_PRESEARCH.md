# Campaign 1 — pre-search normalizer implementation errata

Date: 2026-08-25

Status: **applied before the first real Voynich→historical-language score**.

The frozen normalization specification requires corpus-only validation before Voynich mapping
search, including <=1% unhandled alphabetic tokens and inspection of 200 historical words.
Production implementation exposed two coverage omissions and one date-filter bug before any
Voynich language score had been computed.

## E1 — common historical grapheme coverage

The first implementation omitted several mechanically interpretable historical glyph forms:

- long `ſ` -> `s`;
- `ß` -> `ss` before broad S-class conversion;
- superscript letter forms (`ˢ ᵉ ᵃ ᵒ ⁱ ᵛ ᵘ`) -> their base letters;
- orthographic `x` -> ordered `K S` where no language-specific rule overrides it.

These are corpus-side transcription/orthographic handling rules. They were added because the
historical-corpus validation threshold itself failed, not because of any Voynich output.

After the correction, full selected-corpus alphabetic-token drop rates are:

- ReF: 0.118975%
- ReN: 0.018652%
- BFM: 0.000000%
- DanteSearch: 0.000000%
- LatinISE: 0.000000%

All pass the preregistered <=1% gate.

## E2 — LatinISE boundary-date contamination

The earlier interval-overlap implementation treated a century-only `cent. 16 A.D.` record as
intersecting an inclusive 1300–1500 interval at the single boundary year 1500. This admitted
records whose content is plainly later than the Campaign-1 window.

Pre-score correction:

- explicit dated ranges are retained when they overlap 1300–1500;
- century-only metadata is accepted only when the century label lies within the intended
  14th/15th-century window;
- a 16th-century label is retained only when the explicit `date` field itself overlaps the
  boundary (for example `1500A.D.` or `1500-1508A.D.`).

Corrected LatinISE primary subset:

- 51 documents;
- 451,216 normalized surface tokens.

## E3 — 200-word inspection implementation

The earlier validation file recorded deterministic examples rather than a fixed random sample.
The production freeze now draws 200 normalized historical tokens per branch with seed `20260825`.
The frozen sample is stored in:

`phase5/corpora/NORMALIZER_RANDOM_SAMPLE_200_v1.csv`

Rule-level regression tests are additionally stored in:

`phase5/tests/test_historical_normalizers.py`

No normalizer rule was changed after the first real Voynich-language score was opened.
