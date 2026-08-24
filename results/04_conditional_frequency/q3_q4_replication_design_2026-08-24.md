# Cross-quire qo replication design: Quire 3 and Quire 4

Date: 2026-08-24

## Why Quire 3 is the primary replication set

Quire 3 (folios 17–24) is a standard quire. The available page metadata consistently classify
its herbal text as Currier A / RZ A and LFD hand 1.

This makes Quire 3 a substantially cleaner test of the Quire-1/Quire-2 `qo` observations,
because a bifolio gradient cannot immediately be explained by a hand-1 vs hand-2 or
Currier-A vs Currier-B switch.

Reference:
https://voynich.nu/q03/index.html

## Why Quire 4 must be stratified

Quire 4 (folios 25–32) is a standard quire but contains a mixture of Currier A and B pages.
The documented hand classification also changes: e.g. f26/f31 material is associated with
Currier B / LFD hand 2, while several surrounding folios are Currier A / hand 1.

Therefore a raw comparison of B=1..4 in Quire 4 would confound:

- physical bifolio depth;
- Currier language/state;
- proposed scribal hand;
- potentially section/layout style.

Reference:
https://voynich.nu/q04/index.html

## Analysis rule introduced in v0.5

For every quire/bifolio result, record the distribution of:

- `$L` language/state metadata;
- `$H` proposed hand;
- `$B` physical bifolio index;
- page count;
- token count;
- EVA-letter count;
- `q` count;
- token-initial `q`;
- token-initial `qo`.

A bifolio comparison is marked **MIXED** if more than one `$L` or `$H` value occurs within
the compared strata.

## Primary hypothesis test

For clean quires:

    H0: qo rate is unrelated to physical bifolio depth.
    H1a: qo rate changes monotonically with depth.
    H1b: qo rate alternates by bifolio parity.
    H1c: qo follows a quire-specific non-monotonic state pattern.

The analysis must report effect sizes before any significance test.

## Important correction

The project will no longer interpret isolated EVA `q` as the primary candidate unit.
The first explicit block candidate is EVA `qo`, while preserving three competing models:

1. q and o are independent;
2. qo is one phonographic/motoric unit;
3. q is an operator that selects/modifies an o-initial class.

## Status

Exact Quire 3/4 counts require the complete RF1b-EVA file, not manually copied web excerpts.
The code in this version is prepared to run the full scan reproducibly once that file is
available locally.
