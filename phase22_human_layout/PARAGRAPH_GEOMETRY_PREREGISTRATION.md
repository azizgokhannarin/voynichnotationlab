# Phase 22 — Image-grounded paragraph and boundary scan

## Status

`TRAIN_GEOMETRY_DESIGN; NO VALIDATION IMAGE SCORING AUTHORIZED`

The project now imposes a human-executability prior: candidate mechanisms must
be learnable, memorable and writable by a fifteenth-century person without
machine-scale search or long hidden-state calculations.

## Research questions

1. Do geometry-only cues identify stable visual paragraph boundaries?
2. Are tall/composite gallows constructions enriched at those independently
   identified starts?
3. Does a fixed de-ornamentation or frame/interior decomposition map paragraph-
   initial tokens to ordinary non-initial token families?
4. Is EVA `m`, or any other visible unit, paragraph-final specifically rather
   than merely physical-line-final?
5. In illustration class `S`, does one marginal star correspond to one
   geometry-defined paragraph/entry?

## Non-circular annotation rule

Paragraph labels must be assigned without viewing or transcribing the first
glyph of the candidate next paragraph. The annotation form records only:

- normalized unused width on the preceding line;
- return to the local left margin;
- vertical gap above the candidate line;
- indentation relative to neighbouring lines;
- drawing intrusion or obstacle;
- local writing-block width;
- star adjacency for the `S` section, hidden during the primary geometry call
  and revealed only for the separate entry-marker test.

The first-glyph crop is masked until the geometry label is frozen.

## Boundary classes

- `B0_CONTINUATION`
- `B1_PARAGRAPH_START`
- `B2_ENTRY_START_STAR_SECTION`
- `BX_UNDECIDABLE`

`BX_UNDECIDABLE` cases are never forced into either class.

## Composite-initial representation

The user-supplied crop shows tall frames with ordinary-sized marks placed
between the uprights. The scan therefore stores:

- `outer_frame`: `k/t/p/f/other/unresolved`;
- `inner_sequence`: zero or more visible components;
- `bench_or_pedestal`: yes/no/unresolved;
- `extension`: none/vertical/horizontal/both/unresolved;
- `execution`: compact motor chunk / separable strokes / unresolved.

No field is assigned a sound value in Phase 22. Long strokes may be phonetic
lengthening, abbreviation, emphasis or calligraphic extension; these remain
separate hypotheses.

## Data order

1. Use only existing TRAIN pages to define masks, geometry measurements and
   adjudication rules.
2. Freeze the algorithm, thresholds and exclusion rules.
3. Run once on existing VALIDATION pages. These pages are development-tainted,
   so the result is robustness evidence, not fresh confirmation.
4. Keep sealed final-test pages closed until a genuinely new directional
   prediction exists.

## Primary tests

### T1 — Geometry-to-transcriber robustness

Compare geometry-only boundaries against ZL3b, IT2a and GC2a paragraph markers.
Agreement with any single transcription is not a success criterion. The output
is the three-way agreement/disagreement matrix plus image adjudication.

### T2 — Decorated-initial enrichment

After geometry labels are frozen, compare direct gallows and bench-gallows
rates at `B1` versus matched `B0` line starts, stratified by page and
illustration class.

### T3 — Fixed de-ornamentation

Permit only transformations frozen on TRAIN, such as removing one outer frame
or decomposing one known `ckh/cth/cph/cfh` construction. Measure whether the
remaining token body has a non-initial counterpart more often than
frequency/length/page-matched random starts.

### T4 — Paragraph-final specificity

Compare visible units at:

- geometry-defined paragraph ends;
- ordinary physical line ends;
- line-internal token ends.

A punctuation/closure candidate must be paragraph-final across sections and
transcriptions, not only physical-line-final.

### T5 — Star-as-entry-marker

On class `S` pages, reveal star coordinates only after geometry labels are
frozen. Test one-to-one adjacency between stars and entry starts. Extra stars,
missing stars and ambiguous multi-line associations are reported explicitly.

## Kill rules

- If geometry-only paragraph agreement is not robust across image adjudication,
  do not use paragraph units in language attacks.
- If a decorated-initial effect disappears after page/section matching, do not
  call the gallows a capital or paragraph operator.
- If a proposed de-ornamentation requires token-specific exceptions, reject it.
- If a terminal candidate is equally enriched at ordinary line ends, classify
  it as line-final realization rather than punctuation.
- Do not add new transformations after viewing VALIDATION results.

## Licensed claims before image scoring

The transcriber scan may describe consensus and disagreement. It cannot certify
paragraphs, identify phonetic values, prove punctuation removal, or infer
semantic content.
