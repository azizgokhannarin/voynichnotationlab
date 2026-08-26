# Instrument recalibration: content-blindness stress test

Date: 2026-08-26

Final-test Voynich pages used: **NO**.

## Why this phase exists

The v4.3 generation-vs-latent-content checkpoint used induced distributional token classes,
line-reset tests, distant-context prediction and a line-local-vs-continuous model competition.
Independent adversarial reviews identified a serious calibration gap:

> the same pipeline had not been shown to retain evidence of known hidden content after a strong
> layout-sensitive rendering transformation.

This phase therefore tests the instrument before fitting any richer Voynich generator.

## A. Real abbreviated-manuscript negative-control pilot

A real four-page sample was assembled from:

**Philadelphia, College of Physicians, 10a 135 — Tractatus de Sterilitate**, 14th-century medical
Latin, from CREMMA Medii Aevi.

The CREMMA transcription is graphemic/diplomatic, preserves abbreviation signs and original
manuscript lineation.

Pilot size:

- 112 manuscript lines
- 1,202 surface tokens
- 34 held-out lines / 308 held-out tokens

The induced-class lag test was inconclusive. Crucially, when the exact same small-sample regime
was applied to a matched 112-line Voynich sample, Voynich's known full-corpus strong lag-1 class
signal also disappeared.

**Decision:** this negative-control pilot is underpowered and is not used to compare Voynich with
ordinary abbreviated Latin. A full-size diplomatic control remains required.

## B. Known-content strong-renderer positive control

A large sequence of genuine normalized medieval Latin was taken from LatinISE. The hidden content
is therefore known to be ordinary natural language.

A bounded stress-test renderer was frozen before evaluation. It combines mechanisms historically
attested separately in medieval/early-Renaissance abbreviation and cipher practice, without
claiming that this exact combination is one attested historical system:

- top 8% frequent word types receive nomenclator-style single codes;
- other words become one or two deterministic syllabary-like chunks;
- each chunk has 1–3 homophonic surface forms;
- 20% null-token insertion after content chunks;
- an explicit line-final surface variant;
- Voynich TRAIN line-length distribution is used only as layout scaffolding.

The renderer generated:

- 4,200 lines
- 49,353 surface tokens

The plaintext is indisputably Latin throughout.

### Class-order result

Frozen surface classes, tested against line-local shuffle:

| lag | z |
|---:|---:|
| 1 | 55.79 |
| 2 | 1.79 |
| 3 | -1.12 |
| 4 | -0.87 |
| 5 | 0.59 |

This is strikingly similar in *shape* to the v4.3 Voynich class result:

- Voynich: approximately **30.6, 2.36, -0.32, -1.17, -1.27**
- known-content rendered Latin: **55.79, 1.79, -1.12, -0.87, 0.59**

Both show very strong lag 1, weak lag 2 and essentially no reliable longer-range class-order
signal.

### Model competition

Held-out surface loss:

| model | bits/token |
|---|---:|
| Position | 1.9962 |
| Continuous class context | 1.9468 |
| **Line-local** | **1.9032** |
| Hybrid line-local + distant | 1.9068 |

The line-local model beats the continuous-class model by:

**0.0436 bits/token**

For comparison, the analogous v4.3 Voynich gain was approximately **0.0581 bits/token**.

Adding distant context to the rendered-Latin line-local model also fails to help.

## Calibration conclusion

This is a decisive calibration result about the *instrument*, not about Voynich content.

A text known with certainty to contain natural-language content can, after a bounded strong
line-aware mixed renderer, reproduce the same diagnostic pattern that v4.3 had tentatively read
as evidence for a locally generated surface:

1. very strong induced-class lag 1;
2. weak/null lag 2+;
3. line-local predictor beating continuous class context;
4. distant context adding no held-out benefit.

Therefore these measurements are **not discriminative between**:

- autonomous procedural generation, and
- hidden natural-language content behind a sufficiently strong line-aware renderer.

The v4.3 observations themselves remain valid, but the interpretation must be weakened.

## What is still robust

The following conclusions survive recalibration:

1. Direct frozen-unit phonographic substitution with fixed word-like boundaries is unsupported.
2. Voynich surface structure is highly constrained and productive.
3. Visible boundaries and line position carry real surface information.
4. A simple first-order generator is insufficient to reproduce all held-out Voynich statistics.

The following conclusion does **not** survive as a discriminator:

> "line-local class dependency / no distant class gain favors autonomous generation over hidden
> content."

The strong-renderer positive control falsifies that inference.

## Revised hypothesis space

- **H_C:** linguistic content behind a strong mixed-granularity/layout-sensitive renderer.
- **H_D:** structured non-linguistic content (records, tables, enumerative or quantitative data)
  behind a renderer.
- **H_G:** autonomous procedural generation.
- **H_T:** transcription/palaeographic/production artifacts as a confound.

At present the calibrated class-space instrument cannot rank H_C against H_G.

## Required next calibration

Before returning to mechanism fitting:

1. acquire a substantially larger real diplomatic, abbreviation-preserving medieval control with
   original lineation;
2. run the full v4.3 pipeline unchanged on it;
3. replace class-only long-range diagnostics with raw-token identity recurrence/burstiness and
   residual-capacity measurements;
4. calibrate those new measurements on the known-content strong renderer before applying them to
   Voynich.

No latent-state necessity claim should be made until an instrument can demonstrably detect known
hidden content in the positive control.
