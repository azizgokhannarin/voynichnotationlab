# D1 / EVA-q bifolio-layer gradient in Quire 1

Date: 2026-08-23

## Why this test was added

The first-pass novelty scan identified B4 / EVA-g as a late first appearance relative to f1r/f1v. A stationary-frequency null model shows that B4's delay is not by itself surprising:

- RF1b B4 count: 165 / 157250 STA units
- stationary rate: ~0.00105
- units before the first B4 at f3r.1: ~1643
- probability of waiting at least this long under an independent stationary model: ~0.18

Therefore B4's first appearance alone is **weak evidence** for notation evolution.

During the same check, D1 / EVA-q showed a much stronger early-page gradient.

## Physical quire structure

Quire 1 consists of four nested bifolios:

1. outer: f1 + f8
2. second: f2 + f7
3. third: f3 + f6
4. inner: f4 + f5

RF1b records the same bifolio index in metadata (`$B=1..4`).

## D1 counts

| Bifolio layer | Pages | STA units | D1 count | D1 rate |
|---|---|---:|---:|---:|
| outer | f1r,f1v,f8r,f8v | 2010 | 5 | 0.249% |
| second | f2r,f2v,f7r,f7v | 1089 | 20 | 1.837% |
| third | f3r,f3v,f6r,f6v | 1452 | 36 | 2.479% |
| inner | f4r,f4v,f5r,f5v | 919 | 26 | 2.829% |

The inner/outer rate ratio is approximately **11.37×**.

A unit-level Cochran-Armitage trend calculation gives approximately:

- Z = 6.055
- nominal two-sided p = 1.4e-9

Outer versus inner Fisher exact:

- nominal p = 1.9e-9

### Important statistical warning

STA units are **not independent Bernoulli trials**. They occur in words, lines and pages with strong local dependence. The p-values above are therefore descriptive signal-strength indicators only and must **not** be treated as confirmatory significance.

A future analysis should use page/bifolio-level permutation or a hierarchical model.

## Control glyphs

Rates across outer -> inner bifolios:

| STA | outer | second | third | inner | inner/outer |
|---|---:|---:|---:|---:|---:|
| D1 / EVA-q | 0.25% | 1.84% | 2.48% | 2.83% | 11.37× |
| A1 / EVA-o | 16.62% | 17.91% | 21.49% | 21.33% | 1.28× |
| B1 / EVA-d | 7.51% | 8.82% | 4.75% | 6.86% | 0.91× |
| Q1 / EVA-k | 4.78% | 4.32% | 4.27% | 3.48% | 0.73× |
| K1 / EVA-ch | 10.25% | 11.75% | 10.74% | 10.23% | 1.00× |
| A2 / EVA-y | 9.60% | 11.39% | 7.85% | 10.66% | 1.11× |

D1 therefore has a much larger monotonic effect than these simple controls, although A1 also changes.

## Interpretation

### Compatible with notation-development hypothesis

If Quire 1 was written bifolio-by-bifolio from the outer sheet inward, the gradient is compatible with D1 becoming progressively more available/frequent in the writer's notation.

### Competing explanations

1. **Content allocation:** different lexical/phonetic content may have been intentionally assigned to different bifolios.
2. **Dialect/state change:** the encoded language/notational state may differ systematically across sheets.
3. **Production chronology differs:** bound/collated bifolio layer need not equal writing order.
4. **Transcription effect:** RF1b decisions may affect counts, although the magnitude makes this worth checking against ZL/GC.
5. **Structural role:** D1 may be a word-initial operator/prefix rather than a phoneme, so its rate can track grammatical construction rather than sound inventory.

## New prediction

Run the same D1-vs-bifolio-layer analysis independently on other standard quires.

- If the same outer -> inner rise repeats widely, a quire-layout or structural explanation becomes more likely.
- If the gradient is specific to Quire 1, local notation development or local content becomes more plausible.
- If other quires show unrelated gradients, manuscript-wide chronology must be reconstructed before interpreting Q1.

## Current conclusion

This is the strongest quantitative observation in the project so far.

It does **not** prove that D1 was invented during Quire 1 production. It does show that the first quire is highly non-stationary with respect to D1, and that the non-stationarity aligns with the physical bifolio layers rather than merely the reading order.
