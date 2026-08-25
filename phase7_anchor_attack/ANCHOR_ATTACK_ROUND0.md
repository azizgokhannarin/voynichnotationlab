# Anchor attack v1 — Round 0 and first propagation wave

Date: 2026-08-25

Status: **EXPLORATORY CRYPTANALYSIS — NO DECIPHERMENT CLAIM**

Final-test pages used: **NO**

## Why this attack exists

The earlier global phonotactic campaigns tested whether an optimized whole-alphabet mapping fits
historical languages statistically. This phase asks a different, much more classical cryptanalytic
question:

> If one short Voynich token is a common historical word, does the resulting partial substitution
> force additional words and then begin to grow by constraint propagation?

The attack starts with the simplest possible model: strict one-to-one unit substitution, no nulls,
no digraph expansion, no contextual rules, and no lexical exceptions.

## Important implementation correction

An initial scan allowed 4-unit anchors. Those anchors mechanically dominated because they reveal
more target symbols at once. That ranking was discarded as a search bias.

The actual Round-0 anchor scan is restricted to **1–3 frozen units**. Longer tokens are propagation
targets, not starting cribs.

## Main Round-0 lesson

Isolated lexical matches are extremely easy to manufacture. Several branches and several anchors
produce plausible historical words. Therefore a candidate is interesting only when it creates a
self-reinforcing chain under the same alphabet.

## First notable chain: ReN / Middle Low German

Start with the candidate anchor:

    Voynich `or` -> historical `in`

This gives only:

    o -> I
    r -> N

Under that partial alphabet, two TRAIN token types have unique compatible historical completions:

    ory  -> INE   (`inne`)    => y -> E
    orol -> INIX  (`innich`)  => l -> X / historical `ch`

Accepting those two assignments tentatively gives:

    o -> I
    r -> N
    y -> E
    l -> X (`ch` under PHONO-WG-v1)

Without using them to define the anchor, several other source types then become historical forms:

| Voynich | Normalized output | Historical example | TRAIN occ. | VALIDATION occ. |
|---|---|---|---:|---:|
| `ol` | I X | `ich` | 373 | 119 |
| `or` | I N | `in` | 247 | 74 |
| `ory` | I N E | `inne` | 11 | 4 |
| `rol` | N I X | `nich` | 11 | 2 |
| `orol` | I N I X | `innich` | 9 | 3 |
| `ry` | N E | `ne` | 6 | 0 |
| `yor` | E I N | `eyn` | 1 | 1 |

This is the first result in the project that looks like the desired
**anchor -> new letters -> independent recognizable words** mechanism.

It is particularly notable that the very frequent `ol` token becomes `ich` only *after* `l -> ch`
is proposed by another token family. `ol -> ich` was not the starting crib.

### Why this is still not a breakthrough

The same attack also generates other visually convincing chains from other anchors.

For example, ReN `or -> en` with one inferred symbol yields families such as:

    ol   -> er
    olor -> eren
    orol -> ener
    oro  -> ene
    olo  -> ere

And ReN `or -> am` can produce forms including:

    ol     -> al
    CHy    -> we
    oly    -> alle
    oDAr   -> arm
    CHoDAr -> warm

Therefore the lexicon and the repetitive Voynich token families provide enough combinatorial
opportunity that **word-level plausibility alone is not discriminative**.

The ReN `or -> in` chain is a candidate, not a reading.

## Other useful Round-0 observations

### BFM / Medieval French

A simple anchor:

    ol -> de

has a conflict-free first partial step and, after tentative extension, produces forms including:

    lo      -> et
    olr     -> des
    kair    -> mors
    olkain  -> demora
    olkaiin -> demor(r)a

The number of exact lexical types grows on both TRAIN and VALIDATION, but this again may be a
lexicon-fitting effect rather than true language recovery.

### Latin and Old Italian

Plausible function anchors exist, notably:

    Latin:       ol -> et
    Old Italian: or -> il

but their first unique-completion sets contain many mutually incompatible extension assignments.
They are therefore less clean than their attractive isolated words suggest.

## What the attack taught us

The proposed attack is viable: a short anchor really can propagate into larger token families.
But we have also empirically demonstrated the central danger: many wrong anchors can do this at the
single-word level.

The next discriminator must therefore be **contextual coherence**, not more dictionary hits.

For a surviving candidate alphabet we should inspect adjacent token sequences and ask:

1. Do independently resolved words form attested historical bigrams/trigrams?
2. Does a candidate function word occupy the same syntactic neighborhoods as its proposed target?
3. Does extending the alphabet increase phrase-level coherence rather than merely the count of
   isolated dictionary words?
4. Does the same behavior persist on VALIDATION pages without changing the mapping?

The ReN `or -> in -> {ich, inne, nich, innich, eyn...}` chain should be the first candidate subjected
to that test, alongside matched alternative anchors such as `or -> en` and `or -> am` so that human
pattern preference cannot decide the outcome.

## Current conclusion

We have **not decoded Voynich**, but this attack has reached a qualitatively different stage from
the global mapping experiments: we now have explicit partial alphabets whose consequences can be
read and falsified token by token.

The next phase should not enlarge the substitution model. It should test whether the best candidate
chains produce coherent historical **phrases and contexts** under the same frozen partial alphabet.
