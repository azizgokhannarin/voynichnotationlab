# Phase 17 preregistration: structured-data controls

Freeze date: 2026-08-26

Status: frozen after source/hash verification and before parsing either control
dataset into an instrument result.

## Purpose

Phase 16 localized the Voynich VALIDATION exact-identity signal primarily to
page and line allocation. Phase 17 asks whether known non-linguistic structured
records can produce the same bounded phenotype under the unchanged Phase-16
instrument.

This is a calibration of H_D examples, not an H_C/H_D/H_G ranking. A matching
control establishes possibility, not identity or likelihood. A non-match closes
only the exact encodings tested here.

## Frozen instrument

- executable: `../phase16_raw_token_recurrence/raw_token_recurrence.py`;
- required SHA-256:
  `f4cb1b8e970f6982cbc1a539292ffb188c7f8aa714ad0a437f100aa455a946a4`;
- 2,000 permutations per document/page/line null;
- Holm family alpha `0.01`;
- exact case-sensitive token identity;
- no normalization, induced classes, language model or semantic information;
- no modification to the Phase-16 metrics, seeds, nulls or decision thresholds.

## Source controls

### Transaction baskets: UCI Online Retail

Known content: retail invoices containing product identities and positive
quantities. Exclude cancellations, non-positive quantities, empty product codes
and malformed dates. Sort invoices by timestamp and invoice identifier.

For a requested physical-line length `n`, select the next chronological invoice
whose capped quantity-tally stream has at least `n` tokens. Each product code is
repeated `min(quantity, 4)` times; the first `n` tokens form the record surface.

Two paired surfaces use exactly the same line inventories:

1. `RETAIL_TALLY_ORDERED`: identical products remain grouped in source item
   order;
2. `RETAIL_TALLY_UNORDERED`: deterministically shuffle each completed line with
   seed derived from `20260826`, the control name and line id.

This pair isolates record allocation from within-record order.

### Fixed-schema table: UCI Mushroom

Known content: 8,124 categorical records with one class and 22 attributes.
Rows remain in source order. Each target line begins with the next source row;
the 11 target lines longer than 23 fields append fields from the following row.

Three surfaces are frozen:

1. `MUSHROOM_RAW_ORDERED`: retain one-character source codes in fixed column
   order, allowing the same surface code to mean values in different columns;
2. `MUSHROOM_RAW_PERMUTED`: deterministically shuffle the exact completed-line
   inventory;
3. `MUSHROOM_QUALIFIED_ORDERED`: encode each value as `Fnn:value`, retaining
   fixed schema and disambiguating columns.

The ordered/permuted raw-code pair is an exact line-inventory ablation. The
qualified surface tests an explicit-field notation rather than an overloaded
compact code.

## Geometry match and target firewall

All five controls copy only these attributes from the canonical Voynich
VALIDATION layout:

- physical page grouping;
- physical line count and order;
- token count required for each line.

They copy no Voynich token identity, frequency, spelling, neighborhood or
illustration/section label. The canonical Voynich corpus must have SHA-256
`5fdf577932f21b6da59b7ae12f5bb5451d9bb5b574d81c1affd8b646364b9997`.
Only its `validation` records may contribute geometry. All 46 final-test pages
remain excluded from every derived control and analysis.

Every control therefore has exactly 45 pages, 1,024 physical lines and 7,596
tokens. This matches geometry and power while leaving identities entirely
source-derived.

## Power and integrity gates

Before interpretation, every corpus must satisfy:

1. source payload SHA-256 equals the provenance freeze;
2. frozen Phase-16 executable SHA-256 matches;
3. 45 pages, 1,024 lines and 7,596 tokens;
4. exact page/line/token-length geometry equals Voynich VALIDATION;
5. no final-test record or token contributed to a control or result;
6. paired ordered/permuted variants have identical token multisets for every
   line, page and corpus;
7. all five Phase-16 runs complete with 2,000 permutations.

## Primary phenotype comparison

The previously observed Voynich phenotype is frozen as four Boolean conditions:

1. document-null page repeat mass is positive and Holm-significant;
2. document-null line repeat mass is positive and Holm-significant;
3. page-null line repeat mass is positive and Holm-significant;
4. none of the three line-shuffle identity-gap metrics is Holm-significant.

A structured control is a `FULL_PHENOTYPE_MATCH` only if all four conditions
hold. No threshold is tuned to a control result and no nearest-control score is
used as a hypothesis probability.

Secondary reporting records all exact ratios, z scores and Holm decisions and
compares the paired order ablations. It may explain the scale of a difference,
but cannot rank H_C, H_D or H_G.

## Decision rules

- If at least one control fully matches, broad H_D cannot be rejected by the
  Phase-16 allocation-without-order phenotype.
- If no control matches, only these five bounded structured encodings fail; H_D
  remains open.
- Regardless of outcome, do not open final-test pages, add a Voynich generator,
  fit latent states, resume language search or use semantic/illustration cribs.
- The next frozen stage remains residual information capacity, with its own
  lossy-renderer positive calibration, only after this checkpoint is archived.
