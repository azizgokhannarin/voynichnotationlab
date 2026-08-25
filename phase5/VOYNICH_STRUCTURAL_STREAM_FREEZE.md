# Campaign 1 — real Voynich structural-stream freeze

Date: 2026-08-25

Input:

- `RF1b-e.txt`
- SHA-256: `e7d3238e35743e06c63367a933909ec37b1e2de7ada3a1b449447eafa1918782`
- frozen split manifest: `phase5/voynich_page_split_manifest.csv`

Serializer:

- schema: `C1-STRUCT-v1`
- generator: `phase5/search/build_c1_structural_stream.py`
- generated stream is a local analysis artifact and is not vendored in the repository.

## Parser lock

The parser was selected by reproducing the already-frozen split-manifest token counts.
It removes `@<digits>;` transcription control codes, treats `<->` as a visible token separator,
splits on period/whitespace/comma, then removes non-lowercase-EVA characters from each resulting
surface token.

This reproduces the split manifest **exactly on 227/227 pages**, preventing a post-hoc cleaner
parser from silently changing the Campaign-1 data.

## Frozen segmentation

- EVA `ch` / `sh` remain single EVA glyph units (`CH`, `SH` labels);
- `QO` promoted;
- `DA` promoted;
- `DY` is not promoted: `d` and final `y` remain separate;
- compound EVA gallows glyph forms already recognized by the project glyphizer remain atomic;
- no language-dependent segmentation is performed.

## Stream audit

- pages: 227
- train pages: 136
- validation pages: 45
- final-test pages: 46
- train tokens: 22,716
- validation tokens: 7,596
- final-test tokens: 8,150
- total tokens: 38,462
- frozen unit inventory: 37

Canonical `C1-STRUCT-v1` SHA-256:

`1ea0e5a32bb5b63ac25e26bdd2c629144cd1232a7aba03d4e2eb384923cad478`

Final-test pages were not supplied to the mapping objective during train/validation search.
