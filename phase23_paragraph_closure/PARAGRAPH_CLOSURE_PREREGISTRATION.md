# Phase 23 — Paragraph-final closure allomorph

## Sole hypothesis

Every paragraph carries a closure operation, but the visible realization of that operation
depends on the final graphic/phonographic shape of the preceding word. The operation may be an
addition, substitution or ornamental modification rather than one invariant punctuation glyph.

No claim about language, star markers, paragraph initials, genre or semantic content is in scope.

## Representation

Two bounded representations are tested without adding exceptions after results are seen:

1. **Raw suffix:** final glyph, preceded by the preceding one or two glyphs.
2. **Frozen terminal family:** `STEM + {n,m,y,r,l,s,Ø}` from the pre-existing terminal analysis.

For the second representation, the last one or two glyphs of `STEM` are the observable proxy for
the word-final shape that is proposed to condition the closure allomorph.

## Data and controls

- Only pages frozen as `TRAIN` in `phase5/voynich_page_split_manifest.csv` may be used to discover
  a mapping.
- ZL3b is the primary EVA description; IT2a is an independent transcription sensitivity check.
- Paragraph-final tokens are compared only with final tokens of other physical running lines.
  This holds physical line-final position constant and prevents the known EVA `m` line-final
  effect from masquerading as paragraph punctuation.
- Labels are permuted within page for the null distribution.
- All reported mapping performance is leave-one-page-out: the evaluated page does not teach its
  own mapping.

## Primary questions

1. After conditioning on the proxy word-final shape, does visible terminal identity carry
   transferable information about paragraph closure?
2. Can a small mapping from proxy ending to closure terminal cover most paragraph ends?
3. Do the same mappings reproduce in IT2a?
4. For exact recurring stems, does the paragraph-final terminal systematically replace the
   ordinary line-final terminal?

## Success rule

The mandatory-allomorph hypothesis advances only if all conditions hold:

1. paragraph closure receives a positive leave-one-page-out information gain over the
   proxy-ending-only baseline;
2. the gain exceeds the within-page permutation 99th percentile;
3. a bounded mapping covers at least 80% of eligible paragraph ends with balanced accuracy at
   least 0.80 against ordinary line ends;
4. direction and mapping family replicate in IT2a;
5. the result is not reducible to EVA `m` or another generic physical-line-final form.

The 80% threshold allows transcription uncertainty while remaining compatible with the word
“mandatory.” It is not a decipherment threshold.

## Failure rule

If the signal is weak, non-transferable, requires exact-token exceptions, fails IT2a, or cannot
distinguish paragraph ends from other physical line ends, the bounded terminal-allomorph model is
rejected. We then may describe paragraph-final preferences but may not call them a universal point.

## Image limitation

Transcriber paragraph ends remain provisional until the Phase-22 blind image-geometry boundary
inventory is frozen. Phase 23 can discover a candidate mapping on TRAIN; it cannot certify a point
from transcription labels alone.
