# Gate A — What conditions terminal choice: grammar, layout, or notation state?

Date: 2026-08-24

## Motivation

An external blind second-opinion suggested that the key distinction is not merely whether
terminal forms are structured, but **what predicts their choice**.

If `n/m/y/r/l/s/Ø` are ordinary grammatical endings, terminal choice should primarily track
linguistic context. If some are writer-specific notation features, physical layout or
manuscript/text state may remain predictive even after the stem is held fixed.

## Dataset and control

Only productive stems are included:

- stem occurs >=10 times;
- on >=3 pages;
- with >=2 terminal alternatives;
- second-most-common alternative occurs >=2 times.

This yields:

- 325 cross-page productive stems;
- 25288 token occurrences.

All prediction is five-fold **whole-page held-out**.

The baseline predicts terminal choice from the stem alone. Every added feature is therefore
tested **conditional on stem identity**.

## 1. Held-out predictive information

Lower bits/occurrence is better.

| feature            |   bits_per_occurrence |   gain_vs_stem |
|:-------------------|----------------------:|---------------:|
| CURRIER_L          |                1.2093 |         0.0724 |
| PARAGRAPH_MARKER   |                1.2102 |         0.0715 |
| INTRALINE_GAP      |                1.2141 |         0.0676 |
| LINE_POSITION      |                1.2142 |         0.0675 |
| NEXT_FUNCTION_ROLE |                1.2236 |         0.0581 |
| PREV_FUNCTION_ROLE |                1.2268 |         0.0549 |
| LINE_LENGTH        |                1.2292 |         0.0524 |
| PAGE_VERTICAL      |                1.2442 |         0.0375 |
| STEM_ONLY          |                1.2817 |         0      |

The strongest low-dimensional signals are not purely lexical.

At alpha=20 smoothing:

- stem only: **1.2817 bits/occurrence**
- Currier A/B state: **1.2093**
- line position: **1.2142**
- next functional-role proxy: **1.2236**

Thus terminal selection contains measurable information about both text/notational state and
line geometry even after the lexical stem has been controlled.

## 2. Residual competition

| model                            |   bits_per_occurrence |   gain_vs_stem |
|:---------------------------------|----------------------:|---------------:|
| CURRIER_L+LINE_POSITION          |                1.1911 |         0.0906 |
| CURRIER_L+NEXT_FUNCTION_ROLE     |                1.2081 |         0.0736 |
| CURRIER_L                        |                1.2093 |         0.0724 |
| LINE_POSITION+NEXT_FUNCTION_ROLE |                1.2115 |         0.0702 |

Most important comparison:

- Currier state alone: 1.2093
- Currier + line position: 1.1911
- Currier + next functional role: 1.2081

Line position still improves prediction after Currier state is already known.
The local grammar proxy adds little residual information after Currier state under this
conservative model.

This is **evidence for a notation/layout layer**, not proof that terminals are non-linguistic.

## 3. Page-level robustness

| comparison                                |   pages |   mean_page_gain_bits |   ci95_low |   ci95_high |
|:------------------------------------------|--------:|----------------------:|-----------:|------------:|
| STEM_ONLY -> CURRIER_L                    |     227 |                0.0629 |     0.0555 |      0.0701 |
| STEM_ONLY -> LINE_POSITION                |     227 |                0.0564 |     0.0497 |      0.0632 |
| STEM_ONLY -> NEXT_FUNCTION_ROLE           |     227 |                0.0477 |     0.0419 |      0.0532 |
| CURRIER_L -> CURRIER_L+LINE_POSITION      |     227 |                0.0114 |     0.0065 |      0.0163 |
| CURRIER_L -> CURRIER_L+NEXT_FUNCTION_ROLE |     227 |               -0.002  |    -0.0065 |      0.0022 |

The line-position gain remains positive in whole-page bootstrap resampling even after Currier
state is included.

## 4. The decisive line-final effect

The same stem was stratified, so differences cannot be explained merely by different words
appearing at line endings.

| ending   |   line_final_observed |   line_final_expected_within_stem |   z_within_stem |   MH_OR_line_final |   MH_OR_Currier_A_vs_B |
|:---------|----------------------:|----------------------------------:|----------------:|-------------------:|-----------------------:|
| m        |                   456 |                          132.422  |         35.7855 |            16.9022 |                 1.8943 |
| y        |                   863 |                          766.416  |          8.9566 |             2.2588 |                 0.9427 |
| n        |                   390 |                          363.185  |          3.9955 |             1.719  |                 1.1181 |
| s        |                    52 |                           54.3719 |         -0.3897 |             0.9429 |                 1.2098 |
| l        |                   380 |                          480.442  |         -6.5171 |             0.6467 |                 0.753  |
| Ø        |                   184 |                          269.566  |         -8.143  |             0.4523 |                 1.1374 |
| r        |                   284 |                          542.598  |        -16.0894 |             0.3293 |                 1.0471 |

The outstanding result is EVA `m`:

- within-stem expected line-final `m` count under the no-layout null:
  **132.4**
- observed:
  **456**
- stratified z:
  **35.8**
- Mantel-Haenszel line-final odds ratio:
  **16.9**

This is far too large to treat `m` as an ordinary terminal variant without explicitly
modelling line position.

`r` and `l` move in the opposite direction, while `y` and `n` have weaker positive
line-final enrichment.

## 5. `m` participates in the same stem families as `r/l`

Among productive stems, 92.4% of all observed `m` occurrences belong to stems that
also have substantial `r` or `l` alternatives under the conservative family threshold.

In those shared families:

- `m` occurrences at line end: **66.2%**
- corresponding `r/l` occurrences at line end: **8.0%**

Selected examples:

| stem    |   m_count |   r_l_count |   m_line_final_pct |   r_l_line_final_pct | endings                                    |
|:--------|----------:|------------:|-------------------:|---------------------:|:-------------------------------------------|
| a       |       115 |         760 |            68.6957 |              10.2632 | r:449; l:311; m:115; n:9; Ø:7; s:5; y:2    |
| d·a     |        59 |         477 |            66.1017 |              17.8197 | r:287; l:190; m:59; n:17; Ø:6; s:3         |
| o·t·a   |        44 |         282 |            59.0909 |               5.6738 | r:150; l:132; m:44; n:3; s:3; Ø:2          |
| q·o·k·a |        24 |         329 |            83.3333 |               4.8632 | l:183; r:146; m:24; n:8; s:3; y:2          |
| ch·a    |        24 |         138 |            58.3333 |               9.4203 | r:79; l:59; m:24; n:10; Ø:2; s:2           |
| o·k·a   |        23 |         277 |            60.8696 |               5.7762 | l:147; r:130; m:23; n:5; s:2; Ø:1; y:1     |
| o       |        20 |         978 |            70      |               6.4417 | l:588; r:390; Ø:114; s:27; m:20; y:12; n:1 |
| ch·o    |        15 |         582 |            26.6667 |               1.89   | l:367; r:215; Ø:77; s:42; y:23; m:15; n:1  |
| a·r·a   |        14 |          28 |            71.4286 |              35.7143 | l:20; m:14; r:8; n:1                       |
| s·a     |        13 |         125 |            84.6154 |              21.6    | r:77; l:48; m:13; Ø:2; n:2; y:1; s:1       |
| q·o·t·a |        12 |         128 |            83.3333 |               9.375  | r:64; l:64; m:12; n:2; s:2; y:1            |
| y·t·a   |        12 |          46 |            50      |               8.6957 | r:27; l:19; m:12                           |
| r·a     |        12 |          31 |            91.6667 |              32.2581 | l:16; r:15; m:12                           |
| o·l·k·a |        12 |          31 |            75      |              12.9032 | r:19; m:12; l:12                           |
| o·r·a   |        10 |          15 |            90      |              33.3333 | m:10; l:8; r:7; n:2; Ø:1                   |

This strongly suggests that at least part of the `m` contrast is a **line-conditioned
notational/graphic alternative** within a family, rather than a normal grammatical suffix.

It does not yet establish that `m` is literally an allograph of `r` or `l`.

## 6. Currier/text-state effect

The same stems can also change terminal distribution substantially between Currier A and B:

| stem      |   A_n |   B_n |   TV_A_B | A_top             | B_top              |
|:----------|------:|------:|---------:|:------------------|:-------------------|
| q·o       |    36 |   200 |   0.5711 | Ø:17; r:7; y:5    | l:142; Ø:33; r:15  |
| o·k·e·e·o |    20 |    21 |   0.4619 | l:9; r:4; Ø:2     | Ø:10; r:6; l:2     |
| sh·a      |    20 |    44 |   0.35   | r:10; n:5; Ø:2    | r:23; l:14; m:6    |
| o·t·e·o   |    23 |    33 |   0.2806 | l:13; s:5; r:3    | l:16; Ø:7; r:5     |
| t·o       |    39 |    28 |   0.2784 | l:17; r:11; y:4   | l:20; r:6; y:1     |
| q·o·k·e·o |    58 |    34 |   0.2606 | l:33; r:11; s:4   | l:13; r:9; Ø:6     |
| s·o       |    44 |    73 |   0.2438 | r:17; l:16; s:5   | l:44; r:24; Ø:3    |
| s·a       |    37 |    84 |   0.2407 | l:15; r:14; m:6   | r:51; l:26; m:4    |
| o·t·o     |    56 |    66 |   0.2294 | l:40; r:14; y:1   | l:32; r:17; y:9    |
| sh·o      |   291 |   100 |   0.2286 | l:112; Ø:99; r:63 | l:55; r:28; Ø:13   |
| o·k·e·o   |    61 |    30 |   0.212  | l:36; r:13; m:4   | l:18; y:5; Ø:4     |
| ch·e·o    |   163 |   183 |   0.2015 | l:65; r:49; Ø:26  | l:88; Ø:43; r:25   |
| o·k·a     |    53 |   226 |   0.2005 | l:32; r:14; m:4   | r:103; l:101; m:17 |
| o·t·a     |    38 |   267 |   0.1974 | l:20; r:11; m:6   | r:125; l:100; m:35 |
| q·o·t·o   |    42 |    36 |   0.1944 | l:21; r:16; Ø:3   | l:23; r:8; Ø:2     |

This may represent:

- notation convention differences;
- dialect/register differences;
- section/content differences;
- hand differences correlated with Currier state.

The experiment does not choose among these yet. It shows that the terminal system is not
stationary across manuscript state.

## Gate-A verdict

### Strongly supported

1. The terminal system is **mixed**, not a single ordinary suffix inventory.
2. Line geometry predicts ending choice after controlling stem.
3. Currier/text state predicts ending choice strongly.
4. EVA `m` is exceptionally line-final-conditioned.
5. The earlier `STEM + TERMINAL` decomposition remains useful, but its terminals must now
   carry separate layout/state features.

### Still open

1. `y/n/r/l/s` may contain genuine phonological or grammatical information.
2. A subset of the terminal variation may still be inflectional morphology.
3. Local grammar proxies are informative in isolation, but their independent contribution
   is smaller once text state is controlled.

## Updated representation

Do **not** use:

    STEM + one homogeneous grammatical terminal

Use:

    STEM
      + terminal identity
      + layout feature
      + text/notational-state feature

with `m` provisionally marked as a high-priority line-conditioned terminal.

## Consequence for Gate B

The planned stem × terminal paradigm test must be layout-conditioned.

Otherwise a cluster such as:

    stem+r / stem+l / stem+m

could be falsely interpreted as a grammatical paradigm when `m` is partly selected because
the token occurs at the end of a manuscript line.

Therefore Gate B will:

1. model/remove the line-final `m` effect;
2. compare terminal distributions within matched non-line-final contexts;
3. only then search for residual stem × terminal block structure compatible with morphology.

This is a major correction to the roadmap and directly reduces false-positive risk.
