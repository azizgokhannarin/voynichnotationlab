# Full-size diplomatic abbreviated medieval negative control

Date preregistered: 2026-08-26

Results inspected before freeze: **NO**.

Voynich final-test pages used: **NO**.

Control final-test pages used: **NO**.

## Question

How does ordinary content-bearing, graphemically transcribed, abbreviation-preserving medieval
Latin behave under the frozen Phase 15 class-space and line-locality instrument?

This control is descriptive. It does not rank H_C, H_D or H_G.

## Frozen source and inclusion rule

Source: CREMMA Medii Aevi, tag `0.1.0`, commit
`e681b1077cddafebb51018a19cce503431139e4f`.

Include every available ALTO-XML transcription page from the frozen repository whose manuscript
is dated wholly or principally from 1300 through 1499 and whose transcribed language is Latin.
The resulting frozen directory list is recorded in `SOURCE_PROVENANCE_v1.json`.

The selection contains 14 manuscripts and 90 ALTO-XML files across medical, scholastic,
literary, grammatical and ecclesiastical material. It is not selected for resemblance to
Voynich.

## Parsing freeze

- process files in canonical path order;
- process `TextLine` and descendant `String` nodes in XML document order;
- join multiple non-empty `String/@CONTENT` values in the same line with one space;
- split surface tokens on Unicode whitespace only;
- preserve case, punctuation attached to tokens, abbreviation characters and combining marks;
- preserve Unicode code points as provided; do not NFC-normalize;
- discard empty HTR segmentation lines only;
- preserve original lineation and page/manuscript identifiers.

## Split freeze

- atomic unit: ALTO-XML page/file;
- stratification unit: manuscript directory;
- within each manuscript, order pages by SHA-256 of `20260826:<relative path>`;
- allocate approximately 60% TRAIN, 20% VALIDATION and 20% sealed control final test;
- for three or more pages, every partition receives at least one page;
- no line from a page may cross partitions.

## Power gate

The control is FULL-SIZE only if:

- at least 3,000 non-empty physical lines exist in TRAIN+VALIDATION;
- VALIDATION contains at least 5,000 tokens;
- VALIDATION contains at least 500 physical lines;
- at least eight manuscripts contribute to TRAIN and VALIDATION jointly.

If any requirement fails, no H_C/H_D/H_G inference is allowed and the control must be enlarged
without inspecting the sealed control final test.

## Frozen outputs

Report, without hypothesis ranking:

- corpus/page/line/token counts and canonical corpus SHA-256;
- induced-class MI shuffle z at lags 1–5;
- line-reset cross-line gain;
- local versus distant-context held-out loss;
- position, continuous, line-local and hybrid model held-out loss;
- comparison to the stored Voynich v4.3 descriptors and the executable strong-renderer control;
- explicit statement that similarity or difference alone does not identify content status.
