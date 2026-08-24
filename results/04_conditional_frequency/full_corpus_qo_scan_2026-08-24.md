# Full-corpus `qo` scan and Quire 3/4 replication

Date: 2026-08-24

## Input

- File: `RF1b-e.txt`
- IVTFF header: `#=IVTFF Eva- 2.0 D 9`
- Lines: 5613
- SHA-256: `e7d3238e35743e06c63367a933909ec37b1e2de7ada3a1b449447eafa1918782`
- The corpus file is **not vendored** in this repository.

## Global `q/qo` structure

Parsed corpus totals:

- tokens: 38462
- EVA lowercase letters: 190521
- literal `q` characters: 5435
- token-initial `q`: 5396
- token-initial literal `qo`: 5258
- non-initial/additional `q`: 39

Therefore:

- 99.28% of literal `q` occurrences correspond to a token-initial q;
- 97.44% of token-initial q tokens begin with literal `qo`.

This strongly supports treating `qo` as an explicit segmentation candidate, while not proving
that it is one phonetic unit.

## Clean replication: Quire 3 (`$Q=C`)

All four bifolio layers are `$L=A`, `$H=1`, `$I=H`.

| B | Tokens | qo-start | qo / 100 tokens |
|---:|---:|---:|---:|
| 1 | 403 | 32 | 7.94 |
| 2 | 341 | 44 | 12.90 |
| 3 | 330 | 37 | 11.21 |
| 4 | 318 | 33 | 10.38 |

Sequence:

    7.94 -> 12.90 -> 11.21 -> 10.38

This is neither the Quire-1 monotonic pattern nor the Quire-2 low/high alternation.

Exact four-layer Spearman permutation test:

- rho = 0.20
- two-sided exact p = 0.917

With only four physical layers, this is descriptive.

## Confounded replication: Quire 4 (`$Q=D`)

| B | L | H | Tokens | qo-start | qo / 100 tokens |
|---:|---|---|---:|---:|---:|
| 1 | A | 1 | 260 | 29 | 11.15 |
| 2 | B | 2 | 383 | 43 | 11.23 |
| 3 | A | 1 | 303 | 16 | 5.28 |
| 4 | A | 1 | 290 | 30 | 10.34 |

B2 is Currier/RZ state B and proposed hand 2, while B1/B3/B4 are A / hand 1.
No raw physical-layer interpretation is permitted.

## Reassessment of Quire 1

Using the same full-EVA parser, Quire 1 `qo` rates are:

| B | Tokens | qo-start | qo / 100 tokens |
|---:|---:|---:|---:|
| 1 | 558 | 5 | 0.90 |
| 2 | 291 | 19 | 6.53 |
| 3 | 389 | 35 | 9.00 |
| 4 | 239 | 25 | 10.46 |

Sequence:

    0.90 -> 6.53 -> 9.00 -> 10.46

This is perfectly monotonic at the four aggregated bifolio layers (rho=1.00), but
with only four layers the exact two-sided permutation p-value is 0.083. This replaces
the earlier, over-optimistic unit-level significance calculation.

The **effect size**, not the small-sample p-value, is the interesting observation:
the inner B4 rate is 11.67x the outer B1 rate.

## Stronger localized anomaly: Quire-1 outer bifolio

The three herbal (`I=H`) pages in Q1/B1 are:

- f8v: 1/118 = 0.85% (rank 1 of 95 comparable H/A/hand-1 pages)
- f1v: 1/86 = 1.16% (rank 2 of 95 comparable H/A/hand-1 pages)
- f8r: 3/145 = 2.07% (rank 4 of 95 comparable H/A/hand-1 pages)

f1r is `I=T` rather than `I=H`, so it is excluded from that page-rank control; separately,
it contains zero literal q in the parsed transcription.

Thus the low-q/qo property is not confined to f1r: the physically paired outer-bifolio
herbal pages f1v/f8r/f8v are also unusually low.

## Cross-quire interpretation

Quire 1's monotonic outer->inner pattern does **not** generalize to Q2 or clean Q3.
This weakens a generic "bifolio depth controls qo" model.

At the same time, Q1's outer bifolio remains a localized anomaly under the same
Currier-A / hand-1 herbal comparison.

Current competing explanations:

1. local notation-development / early production state;
2. local lexical or phonological content;
3. an unmodeled subtype within Currier A;
4. planning/copying order unrelated to physical bifolio depth;
5. a structural operator whose triggering construction is rare on Q1/B1.

No phonetic value is assigned.

## Next discriminating tests

1. Compare the **followers after `qo`** on Q1/B1 versus later A/hand-1 herbal pages.
2. Compare other token-initial blocks (`ok`, `ot`, `ch`, `sh`) on the same pages to ask
   whether Q1/B1 is specifically `qo`-poor or globally shifted in prefix structure.
3. Run a page-level matched model within A/hand-1 herbal pages.
4. Only then return to a phonographic interpretation.
