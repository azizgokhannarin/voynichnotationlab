# OBS-0017 — Paragraph-initial gallows and independent marginal-item layer

## Observation

Across two EVA transcriptions, direct gallows begin roughly 81–83% of transcriber-defined
paragraphs but only about 8.5% of other running lines. The user's highlighted bench/composite
construction is not comparably enriched at paragraph starts. In Quire 20, 324 marginal stars do
not map one-to-one onto ZL3b or IT2a visual paragraph boundaries.

## Interpretation

Tall gallows have a strong paragraph-initial graphic function. Composite gallows may also operate
as ordinary internal writing units. Marginal stars plausibly mark items or subentries at a
segmentation layer that can be smaller than a visual paragraph.

## Limits

Transcriber paragraph annotations are not image ground truth. No sound, letter, punctuation name,
genre or semantic value follows from this observation. Blind image-geometry adjudication is
required.

## Reproducibility

See `phase22_human_layout/paragraph_scan.py`, the hash-locked sources, and
`results/TRANSCRIBER_BOUNDARY_SCAN_v1.json`.
