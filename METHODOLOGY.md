# Methodology

## Current interpretation lock (v4.4.1)

Until the full-size control and the new raw-token control calibration are complete, H_C, H_D and
H_G are retained as open hypothesis classes and are not ranked. Class-space measurements whose
archived implementation fails regression may be preserved as historical observations but may not
be transferred across corpora. No new language search, semantic/illustration crib, Voynich
generator enrichment or latent-state addition is permitted during this lock.

## Evidence levels

Every note should be classified as one of:

- **O — Observation:** directly visible/measurable feature.
- **I — Interpretation:** plausible explanation of an observation.
- **H — Hypothesis:** a general explanation that produces testable predictions.
- **R — Result:** output of a defined experiment.
- **C — Conclusion:** inference supported by multiple results.

Example:

> O: Glyph X occurs predominantly at token endings.
>
> I: X may have a terminal function.
>
> H: X is a phonological or structural terminator rather than an ordinary consonant.
>
> Test: compare X position distribution with control glyphs and across manuscript regions.

## Anti-confirmation-bias rules

- Record counterexamples before interpreting a pattern.
- Use controls wherever possible.
- Prefer conditional distributions over anecdotal examples.
- Do not treat visual resemblance as identity.
- Do not treat modern EVA character names as phonetic evidence.
- Distinguish manuscript folio order from production chronology.
- When possible, compare within the same proposed scribal hand.

## Chronology problem

A page appearing earlier in the bound manuscript does not prove it was produced earlier. Chronological experiments should therefore record:

- folio
- quire
- proposed scribal hand
- section
- pigment/ink evidence if available
- glyph morphology
- first known occurrence in the chosen transcription

## Reproducibility

Each quantitative experiment should document:

- data source and version
- transcription system
- normalization rules
- excluded tokens
- code version
- exact command
- generated tables/plots

## Interpretation discipline

A statistical association between a motif and a visual context does **not** by itself establish semantic meaning. It only establishes that the motif is context-sensitive.


## Cross-quire confound rule

Any frequency comparison by physical bifolio must report proposed hand and
Currier/RZ language state. A physical-layer effect is not interpreted as
notation evolution when the same layer contrast also changes hand or text state.

Clean replication sets are preferred before mixed sets.
