# Gallows composition test — visual hypothesis vs corpus structure

Date: 2026-08-24

## Trigger

Several manually selected manuscript glyphs were noticed to look like carefully repeated
"clef-like" composite signs rather than atomic characters.

The standard EVA inventory calls the four common tall forms:

    k  t  p  f

the **gallows** characters.

Independent analytical transcription work already decomposes these shapes into smaller
stroke families. This makes the user's visual-composition hypothesis directly testable.

## Existing analytical precedent

René Zandbergen's analytical alignment alphabet (`aaa`) explicitly represents common
Voynich glyphs as combinations of stroke/minim families rather than assuming every EVA
character is atomic.

Examples from the published analytical table include:

- EVA `k` -> `l2:p1`
- EVA `t` -> `q2:p1`
- EVA `cth` -> `c2:q3:p3:c1`
- EVA `ckh` -> `c2:l3:p3:c1`
- EVA `cph` -> `c2:q3:x1:c1`
- EVA `cfh` -> `c0:l3:x1:c1`

Thus the idea "a decorated gallows can be 2–4 coordinated sub-strokes" is not ad hoc.

## Corpus test 1 — Are k/t/p/f substitutable inside the same token frames?

The complete RF1b-EVA corpus contains many token families whose only important difference
is which gallows member occupies the same structural slot.

High-frequency examples:

| Skeleton | Variants |
|---|---|
| `qoG eey` | `qokeey` 366, `qoteey` 63 |
| `oGaiin` | `okaiin` 201, `otaiin` 150, `opaiin` 12, `ofaiin` 4 |
| `oGeey` | `okeey` 197, `oteey` 160 |
| `qoGaiin` | `qokaiin` 255, `qotaiin` 83, `qopaiin` 7, `qofaiin` 1 |
| `qoGain` | `qokain` 272, `qotain` 62, `qofain` 1 |
| `oGar` | `otar` 151, `okar` 130, `opar` 13, `ofar` 6 |
| `oGal` | `okal` 147, `otal` 132, `opal` 11, `ofal` 3 |
| `qoGeedy` | `qokeedy` 221, `qoteedy` 56 |
| `qoGy` | `qoky` 138, `qoty` 84, `qopy` 6 |
| `oGy` | `oty` 114, `oky` 103, `opy` 8, `ofy` 3 |

This is a strong paradigmatic signal: the four gallows are not scattered arbitrarily.
They occupy many of the **same internal slots**.

## Corpus test 2 — Pedestalled / bench forms show the same substitution family

The common "bench + gallows" forms also form parallel variants.

Example:

    chckhy  146
    chcthy   85
    chcphy   11
    chcfhy    2

and shorter related forms include:

    cthy 100
    ckhy  38
    cphy  14
    cfhy   7

The gallows choice changes while much of the surrounding structure remains fixed.

This is exactly what one would expect if a larger visible form is assembled from:

    shared frame + variable gallows component

rather than being four unrelated decorative letters.

## Important interpretation

This evidence supports **compositionality of the writing system**, but does not yet tell
us the linguistic level of each component.

At least four models remain:

### P1 — phoneme composition

Sub-strokes correspond to sound features or phonemes; a gallows glyph is a compact ligature
for a multi-sound unit.

### P2 — syllabic composition

A gallows or bench-gallows combination represents a syllable or onset cluster as one
learned motor chunk.

### P3 — operator + payload

One sub-component modifies the reading/function of another, analogous to a diacritic,
abbreviation mark, or mode operator.

### P4 — graphic allography

The apparent components are primarily scribal/graphic variants and do not decompose
linguistically.

## Relation to the user's "confident execution" observation

The shapes are written fluently enough to be compatible with learned motor chunks.
That is consistent with a writer who had practiced the system.

However, fluent repetition alone does **not** prove:

- that the writer invented the system;
- that each visible sub-stroke had an independent sound;
- formal linguistic training;
- deliberate borrowing from Greek, Arabic, Latin or numerals.

Those are separate hypotheses.

## Cross-script resemblance

Some Voynich glyphs visually resemble forms from Latin manuscript abbreviation,
Greek-like, Arabic-like, numeral-like, or notational repertoires. Medieval scribes were
surrounded by ligatures and abbreviations, so mixed visual inspiration is historically
possible.

But shape resemblance has a high false-positive rate. A limited pen-stroke repertoire
naturally creates accidental similarities across scripts.

Therefore the project will treat such resemblances as **hypothesis generators only**.

## Key consequence for decipherment

We should no longer assume:

    one EVA glyph = one sound

The working model becomes:

    primitive strokes
        -> graphic compounds / learned chunks
        -> functional or phonographic units
        -> token/rime structure
        -> candidate language

This is compatible with the previously observed:

- `qo` block;
- onset-like `da`;
- terminal `dy`;
- replaceable-onset rime families (`aiin`, `ain`, `air`, ...);
- gallows substitution families.

## Next quantitative step

Before scoring candidate European languages, build a **latent unit inventory**:

1. decompose known composite gallows with the analytical alphabet;
2. compare contexts of the primitive/shared components;
3. identify which compounds behave as indivisible units;
4. compare an atomic-EVA model against a decomposed-stroke model using predictive
   likelihood / MDL-like compression;
5. carry only statistically supported units into phoneme/language scoring.

## Current conclusion

The user's visual hypothesis that the clef-like gallows are composite is **supported at the
graphic/structural level**.

This does not yet show that "two symbols combine into a third sound," but it makes that
model substantially more plausible and testable.
