# Structural follow-up: `da`, `dy`, and the `aiin` rime family

Date: 2026-08-24

## 1. Correcting the `dy` interpretation

EVA `y` is itself strongly position-sensitive in the complete RF1b-EVA parse:

- total `y`: 17,512
- token-final: 14,985 (85.57%)
- token-initial: 1,718
- medial: 599
- standalone: 210

Therefore the fact that `dy` is usually final cannot by itself establish `dy` as a
two-sound syllable.

### But `d+y` is still a real association

Among 14,985 y-final tokens:

- 4,870 have `d` immediately before final `y`.

Across all tokens of length >=2, `d` occupies the penultimate position only ~13.47%
of the time. A 2x2 positional comparison gives an exploratory odds ratio of ~69.68
for `d` preceding final `y` versus `d` preceding non-y finals.

Thus:

    terminal preference of y != full explanation of dy

The `dy` pair is genuinely over-associated at token endings.

## 2. `d+a` is also strongly associated at token onset

Among 3,110 tokens beginning with EVA `d`:

- 1,952 (62.77%) continue with `a`.

Compared with all other token-initial glyphs, the exploratory onset odds ratio for
`d -> a` is ~40.12.

Initial continuation entropy for `d` is 1.92 bits. For comparison:

- EVA `q`: 0.21 bits, dominated by `qo`
- EVA `c`: 0.75 bits, dominated by `ch`
- EVA `s`: 1.34 bits, dominated by `sh`
- EVA `d`: 1.92 bits, dominated by `da`

This supports `da` as a structural onset pair, though not yet as a phonetic syllable.

## 3. A recurring rime family

The corpus contains a conspicuous family in which different initial glyphs attach to
the same endings.

Selected counts:

| suffix/rime | bare | d+ | s+ | k+ | t+ |
|---|---:|---:|---:|---:|---:|
| `aiin` | 634 | 721 | 125 | 74 | 46 |
| `ain`  | 149 | 173 | 67 | 49 | 14 |
| `air`  | 95  | 93  | 26 | 15 | 12 |
| `ar`   | 449 | 287 | 77 | 58 | 43 |
| `al`   | 311 | 190 | 48 | 30 | 24 |
| `am`   | 115 | 59  | 13 | 5  | 4 |

The same onset substitutions recur over multiple rimes. This is compatible with:

- consonant-like onset substitution in a phonographic system;
- templatic morphology;
- a generative positional grammar.

It is not, by itself, evidence for a specific natural language.

## 4. West Germanic probe — deliberately exploratory

One pattern is sufficiently familiar to record, but not to accept:

    aiin
    daiin
    saiin
    kaiin
    taiin

Their counts are:

- `aiin`: 634
- `daiin`: 721
- `saiin`: 125
- `kaiin`: 74
- `taiin`: 46

If the common rime represented something near /ain/ or /ein/, these can be compared
experimentally with the West Germanic family:

    ein
    sein
    mein
    kein
    dein

The only partially independent phonetic clue currently available is the external proposal
that the 8-like EVA `d` belongs to an S/Ş-like sibilant class. Under an S-like reading,
`daiin -> sein` is therefore a legitimate candidate probe.

Historical Germanic relevance:

- Middle High German has `ein` as article/numeral.
- Middle High German has possessive `mîn`, `dîn`, `sîn`.
- Middle High German has `kein`.
- southeastern German long-i diphthongization toward `ei` began well before the fifteenth
  century, making mein/dein/sein-like phonetics historically possible in some regions.
- Middle Dutch / Middle Low German preserve closely related mijn/dijn/sijn or mîn/dîn/sîn
  families, so any real match would initially indicate West Germanic rather than uniquely German.

## 5. First falsification controls — important problems

The resemblance does **not** yet survive as a lexical identification.

### Currier-state rates per 10,000 tokens

| token | A | B |
|---|---:|---:|
| `aiin` | 128.7 | 186.5 |
| `daiin` | 379.2 | 110.0 |
| `saiin` | 30.0 | 35.5 |
| `kaiin` | 11.5 | 24.7 |
| `taiin` | 13.2 | 13.0 |

`daiin` changes strongly between A and B while `aiin` changes in the opposite direction.

### Line-initial rates

| token | line-initial |
|---|---:|
| `aiin` | 1.7% |
| `daiin` | 20.2% |
| `saiin` | 42.4% |
| `kaiin` | 4.1% |
| `taiin` | 26.1% |

These very different positional behaviors are hard to reconcile with a naive
"same German determiner paradigm, only first consonant changes" model.

### Extra members

The Voynich `-aiin` family also includes frequent forms such as:

- `qokaiin`: 255
- `okaiin`: 201
- `otaiin`: 150
- `raiin`: 56
- `olaiin`: 54
- many others

A Germanic hypothesis must explain these without arbitrary one-off mappings.

## Current status

### Supported structurally

- `da` is a strongly preferred token-onset pair.
- `dy` is a strongly preferred token-final pair even after controlling for the final
  tendency of `y`.
- replaceable-onset / common-rime families are real.

### Open

- EVA `d` may belong to an S/Š-like phonetic class.
- `aiin` may encode a familiar /ain/, /ein/, /i:n/ or related rime.

### Not accepted

- `daiin = sein`
- `aiin = ein`
- German / Dutch / Low German identification

The West Germanic resemblance is retained as a falsifiable probe, not as a decipherment.

## Next test

1. Infer a language-neutral rime inventory (`aiin`, `ain`, `air`, `ar`, `al`, `am`, ...).
2. Measure which onsets can substitute before each rime.
3. Build candidate phoneme classes from distribution alone.
4. Only then score historical language families against the resulting sound skeleton.
