# Phase 23 — Paragraph-final closure allomorph report

## Verdict

The bounded hypothesis that every paragraph stop is encoded as a transferable raw final-glyph or
`{n,m,y,r,l,s,Ø}` terminal allomorph conditioned by the preceding word-final shape is **not
supported on TRAIN**.

This does not rule out a visually subtle allograph that EVA transcription collapses into the same
symbol, a flourish not represented by the transcription, or incorrect paragraph-end annotation.
It does rule against calling the currently transcribed terminal identity a universal point.

## Design

Paragraph-final words were compared only with words at other physical line ends. Thus every case
was already line-final, preventing the known generic EVA `m` line-final effect from becoming a
false paragraph-stop signal. The proposed conditioning context was either the preceding raw glyph
or the last one/two glyphs of the pre-existing frozen stem decomposition. Mapping performance was
leave-one-page-out. Significance used 1,000 within-page label permutations. Only frozen TRAIN
pages were used.

## Primary results

| Test | ZL3b | IT2a | Required |
|---|---:|---:|---:|
| Stem-last-1 conditional information | 0.0421 bits | 0.0436 bits | Above null q99 |
| Within-page null q99 | 0.0449 bits | 0.0481 bits | — |
| Permutation upper-tail p | 0.0509 | 0.0779 | ≤0.01 |
| Leave-one-page-out AUC | 0.5240 | 0.5558 | ≥0.80 |
| Balanced accuracy | 0.5539 | 0.5534 | ≥0.80 |
| Candidate-terminal coverage | 27.96% | 1.44% | ≥80% |

Raw-glyph variants were also near chance: AUC 0.5358 in ZL3b and 0.5674 in IT2a. Adding two
preceding glyphs increased sparsity but did not beat the permutation null.

## Instrument power

A positive control injected a deterministic closure terminal selected from the same existing
terminal inventory and conditioned only on the last stem glyph. The instrument recovered it:

| Positive control | ZL3b geometry | IT2a geometry |
|---|---:|---:|
| Conditional information | 0.6200 bits | 0.6436 bits |
| Null q99 | 0.0627 bits | 0.0661 bits |
| Permutation p | 0.000999 | 0.000999 |
| Leave-one-page-out AUC | 0.9987 | 0.9995 |
| Balanced accuracy | 0.9913 | 0.9919 |
| Mapping coverage | 100% | 100% |

The failure on real data is therefore not caused by an incapable detector.

## Descriptive terminal preferences

Paragraph ends are not distributionally identical to other physical line ends:

| Terminal | ZL3b paragraph end | ZL3b other line end | Odds ratio | IT2a odds ratio |
|---|---:|---:|---:|---:|
| `n` | 23.23% | 13.82% | 1.89 | 1.96 |
| `r` | 9.89% | 7.63% | 1.34 | 1.30 |
| `y` | 44.30% | 38.22% | 1.29 | 1.27 |
| `l` | 9.03% | 12.28% | 0.72 | 0.68 |
| `m` | 8.17% | 16.17% | 0.47 | 0.46 |
| `s` | 2.58% | 3.99% | 0.66 | 0.71 |
| `Ø` | 2.80% | 7.88% | 0.35 | 0.39 |

The `n/y/r` enrichment is real as a surface description, especially `n`. It does not behave like
a mandatory transferable mark after word-final shape is controlled. Exact recurring stems tell
the same story: most retain the same dominant terminal in paragraph and non-paragraph line endings,
and eligible exact stems cover only 38–40% of paragraph ends.

## Licensed inference

1. A single visible EVA terminal is not the paragraph point.
2. A small preceding-glyph-to-terminal substitution table does not encode a universal point in
   the tested representation.
3. `m` is again excluded: it is depleted, not enriched, at paragraph ends relative to other line
   endings.
4. `n`, then `y/r`, should be prioritized in image-level allography because their shapes may hide
   variants collapsed by EVA.

## Next and only authorized target

Construct image crops of paragraph-final and matched other-line-final tokens, matched by the same
transcribed terminal and, where possible, the same stem family. Annotate only graphic properties:

- terminal stroke length and direction;
- loop closure/opening;
- pen lift or reconnect;
- tail, hook or dot-like addition;
- spacing after the word;
- baseline and rightward extension.

The annotator must not see the paragraph label during the primary graphic call. If no graphic
feature transfers across pages and transcriptions, the universal-visible-point hypothesis is
rejected. No language attack is authorized by this phase.
