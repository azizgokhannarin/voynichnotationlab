# Phonetic anchor test 001 — `daral*`, EVA `d+a`, and EVA `d+y`

Date: 2026-08-24

## Research question

A proposed reading of the f78r illustration label interprets its beginning as a sound
similar to Turkish `şa-`. The broader reading "şarap otu" is not assumed here.

We separate two hypotheses:

- **H-A semantic anchor:** a `daral...`-like sequence means *şarap* / wine.
- **H-B phonetic anchor:** the visual 8-like EVA `d`, especially the block `da`,
  may encode an /s/- or /ʃ/-family sound followed by a vowel.

H-B can survive even if H-A fails.

## Exact input

- `RF1b-e.txt`
- SHA-256: `e7d3238e35743e06c63367a933909ec37b1e2de7ada3a1b449447eafa1918782`
- parsed tokens: 38462

## Test 1 — Is `daral` semantically stable?

The cleaned RF1b-EVA corpus contains 11 tokens containing `daral`:

| Page | Locus | Section (`$I`) | Currier (`$L`) | Hand | Token |
|---|---|---|---|---|---|
| f20r | `f20r.3,+P0` | H | A | 1 | `daral` |
| f68r3 | `f68r3.20,=Ls` | A | None | 4 | `darall` |
| f68v1 | `f68v1.6,@Ro` | A | None | 4 | `okechdaral` |
| f73r | `f73r.5,@Cc` | Z | None | 4 | `daraly` |
| f78r | `f78r.44,@Lt` | B | B | 2 | `daralocphy` |
| f79v | `f79v.42,+P0` | B | B | 2 | `daral` |
| f84r | `f84r.34,+P0` | B | B | 2 | `daraly` |
| fRos | `fRos.19,@L0` | C | B | 4 | `daraldy` |
| fRos | `fRos.69,@L0` | C | B | 4 | `daral` |
| f88v | `f88v.10,+P0` | P | A | 1 | `daraly` |
| f90r1 | `f90r1.2,+P0` | H | A | 1 | `darala` |

Exact/near forms include:

- `daral`: 3
- `darall`: 1
- `daraly`: 3
- `darala`: 1
- `daraldy`: 1

The corpus also contains:

- exact `dar`: 287
- exact `al`: 311
- same-locus `dar` followed by an `al...` token: 10 cases

Therefore a visual sequence resembling `daral` can arise from the adjacency `dar + al...`;
word-boundary uncertainty is not a minor issue.

### Critical counterexample

On f68r3, `darall` is an astronomical **star label** (X.9 in the standard interlinear
description), not a botanical label.

This is difficult to reconcile with a stable literal meaning "wine" unless one introduces
additional homonymy/polysemy or rejects the astronomical-label interpretation.

### Result for H-A

**Weakened strongly.**

`daral = şarap` is not a reliable semantic anchor at present.

The f78r label itself also has historical transcription disagreement over whether it is
one word or `dar` + `alocfhy`, so the proposed root boundary is not secure.

## Test 2 — Does the 8-like EVA `d` form constrained blocks?

Literal EVA `d` occurrences: 10492

Immediate followers of `d`:

| follower | count | share of all d |
|---|---:|---:|
| `y` | 5009 | 47.74% |
| `a` | 3450 | 32.88% |
| `<END>` | 734 | 7.00% |
| `o` | 453 | 4.32% |
| `c` | 351 | 3.35% |
| `s` | 164 | 1.56% |
| `e` | 121 | 1.15% |
| `l` | 86 | 0.82% |

The two dominant followers are:

    d+y = 5009 occurrences
    d+a = 3450 occurrences

Together they account for 80.62% of all EVA-d occurrences.

### `da`

Token-initial d words: 3163
Token-initial `da...`: 1952 (61.71% of d-initial tokens)

`da` positional occurrences:

- whole token: 6
- token-initial in longer token: 1946
- medial: 1487
- token-final: 11

Token-initial `da` PMI relative to the corpus second-character baseline:

    PMI(da at token start) = 2.79 bits

Thus `da` is a genuine structural preference, not just a visually selected anecdote.

### `dy`

`dy` positional occurrences:

- whole token: 205
- token-initial in longer token: 62
- medial: 77
- token-final: 4665

Token-initial PMI:

    PMI(dy at token start) = 2.80 bits

The striking feature is not its initial use but its terminal behavior:
the overwhelming majority of `dy` occurrences are token-final or constitute the entire token.

## Interpretation

The semantic "şarap" anchor does not survive well.

However, the **phonographic-block idea survives and becomes more interesting**:

- `d+a` is strongly favored at token onset;
- `d+y` is strongly favored at token termination / as a short complete token;
- the same 8-like base glyph participates in sharply different positional constructions.

This is compatible with several models:

1. `d` is a consonant-like phoneme and `a/y` are vowel/ending signs;
2. `da` and `dy` are independent syllabic blocks;
3. `d` is a structural operator whose function changes with the following sign;
4. the forms are morphological rather than phonetic.

The statistics do **not** identify `/ʃ/` specifically.

## Language-search consequence

Do not compare candidate languages using modern spellings. Compare **phoneme sequences**.

For example, a /ʃ/ sound can be represented in European orthographies by `sch`, `ch`,
`sz`, `š`, `s`, etc. A private notation could use one sign or a two-sign block regardless
of conventional spelling.

The next stage should jointly infer:

    glyph/block segmentation <-> candidate phoneme values <-> candidate language score

rather than fixing an alphabet first and identifying the language afterwards.

## Status

- `daral = şarap`: **strongly weakened**
- `daralocphy = şarap otu`: **not accepted as an anchor**
- EVA `da` as a meaningful block: **supported structurally**
- EVA `da = /şa/`: **open**
- EVA `dy` as a positional block: **strongly supported structurally**
