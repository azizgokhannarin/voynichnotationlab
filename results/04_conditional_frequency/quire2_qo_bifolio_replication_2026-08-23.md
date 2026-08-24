# Quire 2 replication: EVA q / qo by physical bifolio

Date: 2026-08-23

## Purpose

Version 0.3 found a strong monotonic D1/EVA-q increase from the outer to the inner bifolio of Quire 1.

This experiment asks whether that pattern is a general quire-level property.

## Source

RF1b full EVA transliteration, IVTFF 2.0.

Official transliteration resources and documentation:
https://www.voynich.nu/transcr.html

Public RF1b-e mirror used for the replication sample:
https://github.com/Workwrite-Niidome/voynich-manuscript-analysis/blob/master/archive/data/RF1b-e.txt

## Quire 2 physical structure used

Bifolio index is taken directly from IVTFF `$B`.

- B=1: f9 + f16
- B=2: f10 + f15
- B=3: f11 + f14
- B=4: surviving f13 material only in RF1b; the quire is physically incomplete

## Result

| Bifolio | Pages in surviving sample | EVA letters | Tokens | q | q / 1000 letters | q / 100 tokens |
|---:|---|---:|---:|---:|---:|---:|
| 1 | f9r,f9v,f16r,f16v | 1529 | 310 | 22 | 14.39 | 7.10 |
| 2 | f10r,f10v,f15r,f15v | 1439 | 299 | 35 | 24.32 | 11.71 |
| 3 | f11r,f11v,f14r,f14v | 1139 | 245 | 17 | 14.93 | 6.94 |
| 4 | f13r,f13v | 640 | 136 | 16 | 25.00 | 11.76 |

The sequence is therefore approximately:

    low -> high -> low -> high

rather than the monotonic outer -> inner rise observed in Quire 1.

Spearman correlation between bifolio index and q-per-token rate:

    rho = 0.40
    nominal p = 0.60

With only four bifolio layers, and with B=4 incomplete, this is descriptive only.

## q is almost entirely a qo-initial phenomenon

Across the surviving Quire 2 sample:

- q occurrences: 90
- q-containing tokens: 90
- q at token start: 89
- token-start q followed immediately by o: 89 / 89
- internal q: 1

Thus the varying quantity is overwhelmingly the frequency of the **qo- initial block**, not free use of q in arbitrary positions.

This reproduces a long-known Voynich property independently in our working sample.

## Consequence for H02 (notation evolution)

The Quire 1 D1 gradient does **not** replicate as a universal outer-to-inner pattern in Quire 2.

Therefore the interpretation:

    "q becomes more frequent because the writer is learning/inventing q as the quire progresses"

is substantially weakened.

It remains possible that Quire 1 reflects a local developmental phase, but the simpler alternatives now deserve more weight:

1. lexical/grammatical construction frequency;
2. local text state or dialect;
3. content allocation;
4. production-order effects not equivalent to bifolio depth.

## Consequence for H01/H03 sound-unit work

For segmentation experiments, EVA `q` should not initially be treated as an independent phonetic candidate.

A better provisional unit is:

    QO = EVA `qo`

We will compare models in which:

- q and o are independent;
- qo is a single block;
- q is a structural operator selecting an o-initial class.

No sound value is assigned yet.

## New question

Why does qo frequency alternate strongly across Quire 2 bifolios?

Odd B (1+3):
- q / token = 7.03%

Even B (2+4):
- q / token = 11.72%

Naive token-level Fisher exact:
- odds ratio ~1.76
- nominal p ~0.014

Again, tokens are dependent, so this p-value is exploratory only.

The alternating pattern may be more informative than the failed monotonic gradient and should be tested on other quires.
