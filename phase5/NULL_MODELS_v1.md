# Campaign 1 — Frozen Null Model Specification v1

Date frozen: 2026-08-25

Status: **FROZEN BEFORE ANY VOYNICH→LANGUAGE MAPPING SEARCH**

This document defines the matched null generators used by Campaign 1.

The nulls are deliberately different because they destroy different kinds of structure.

---

# 1. Seed policy

Master seed:

    20260825

Each null replicate derives an independent seed as:

    SHA256("C1-NULL-v1|<null_id>|<replicate>|20260825")

The first 64 bits of that digest are converted to an unsigned integer.

Therefore every replicate is deterministic and independent of execution order.

Primary null count:

    1000 replicates per null family per candidate-language model

Development/test runs may use fewer replicates but may not be reported as Campaign-1 evidence.

---

# 2. Input representation

Null generators operate on the **frozen structural token stream**, not raw visual glyphs.

The primary representation preserves:

- manuscript page identity;
- physical line identity;
- visible token boundaries;
- promoted `QO` block;
- promoted `DA` block;
- non-indivisible `DY`;
- frozen terminal representation rules.

No null may alter the train/validation/test page manifest.

---

# 3. Null A — within-token unit shuffle

Purpose:

Destroy internal phonographic order while preserving token-level gross statistics.

For each token independently:

1. preserve the exact multiset of structural units;
2. uniformly shuffle their order;
3. preserve token length;
4. preserve token position, page, line, and visible boundaries.

Preserved:
- token count;
- token lengths;
- global unit counts;
- page/line layout;
- boundary locations.

Destroyed:
- onset/rime order;
- local within-token phonotactics;
- terminal position;
- ordered core structure.

Special constraint:
- one-unit tokens are unchanged.

This is a stringent null for testing whether ordered within-token structure matters.

---

# 4. Null B — token-order shuffle

Purpose:

Preserve word/token internal structure while destroying local syntactic/sequential structure.

Within each physical manuscript line:

1. retain the exact token multiset;
2. uniformly permute token order;
3. do not move tokens between pages or lines.

Preserved:
- all token spellings/structural-unit sequences;
- token frequency;
- line token count;
- page/line membership;
- within-token phonotactics.

Destroyed:
- local token bigrams/trigrams;
- short-token contextual organization;
- sequential syntax-like information.

Why line-local rather than corpus-global:
A corpus-global shuffle would also destroy layout/section structure already known to exist.

---

# 5. Null C — matched synthetic generative corpus

Purpose:

Create pseudo-Voynich that matches low-order observable statistics without copying real tokens.

The frozen generator is a first-order structural-unit Markov model with separate:

- token-start distribution;
- internal unit-transition distribution;
- token-length distribution.

Training is performed **only on the corresponding Voynich training pages**.

Generation procedure:

1. sample a token length from the empirical training token-length distribution;
2. sample first unit from empirical token-start distribution;
3. sample each next unit from the add-0.5-smoothed transition distribution;
4. if a context has no outgoing transition, back off to the global unit distribution;
5. preserve the original page/line/token-count layout when producing a synthetic replicate;
6. generate a new token sequence for every token position.

Preserved approximately:
- unit unigram distribution;
- first-order transition tendencies;
- token-length distribution;
- exact page/line token-count structure.

Destroyed:
- higher-order token identity;
- recurrent stem families;
- long-range morphology;
- lexical repetition;
- syntax-like token sequence dependencies.

Important:
The synthetic generator is fit on TRAIN only. Validation/test synthetic streams are generated
from the frozen train-derived model and the observed layout skeleton only.

---

# 6. Null D — global unit-label permutation

Purpose:

Test whether a candidate-language score depends on meaningful structural-unit identity rather
than merely inventory size and frequency ranks.

For each replicate:

1. create one bijective random permutation over the frozen structural-unit inventory;
2. apply the same permutation to every occurrence in train, validation and test;
3. preserve token boundaries, order, frequency spectrum, recurrence, morphology, and layout.

Preserved:
- all abstract combinatorial structure;
- exact frequency distribution;
- token identity equivalence classes under relabeling;
- syntax/layout.

Destroyed:
- correspondence between a particular Voynich unit and a particular learned phonographic value.

Critical rule:
The mapping optimizer must be rerun from scratch for every label-permutation replicate.

Otherwise Null D would not test the full optimization pipeline.

---

# 7. Required invariants

Every generator must self-check the following.

## Null A
- same number of pages, lines, tokens;
- exact token lengths preserved position-by-position;
- exact corpus-wide unit multiset preserved.

## Null B
- same number of pages, lines, tokens;
- exact token multiset preserved within each line.

## Null C
- same number of pages, lines, token positions;
- exact token-length vector preserved position-by-position in primary mode;
- every generated unit belongs to the frozen inventory.

Note:
Although the preregistration said "sample token length", Campaign 1 v1 fixes the stricter
matched-layout implementation: the observed token length at each position is retained.
This is frozen before language scoring and gives the null *more*, not less, structural matching.

## Null D
- one-to-one inventory relabeling;
- exact structural equality after inverse permutation.

---

# 8. Null-standardized score

For candidate language L and test statistic S:

    Z_L = (S_real - mean(S_null)) / sd(S_null)

The sign convention of S must be frozen by the scoring engine.

If lower is better (for example cross entropy), the reported standardized advantage is:

    Z_adv = (mean(null_loss) - real_loss) / sd(null_loss)

so positive values always mean real Voynich outperforms its nulls.

Primary family aggregation uses these standardized advantages, never raw entropy values from
different target languages.

---

# 9. Empirical tail probability

For N null replicates:

    p_emp = (1 + number(null >= real advantage)) / (N + 1)

For a loss metric, comparisons are transformed to the common "advantage" direction first.

With N=1000 the minimum reportable empirical p-value is:

    1 / 1001 ≈ 0.000999

No Gaussian extrapolation below the empirical resolution is permitted.

---

# 10. Multiple testing

Primary family-level p-values must be corrected across the active Campaign-1 candidate zones.

If West Slavic remains acquisition-blocked, the primary active set is:

- West Germanic
- Romance
- Latin

The blocked family is reported as **NOT TESTED**, not as a failed candidate.

Campaign 1 uses Holm correction for the primary family comparison.

---

# 11. Anti-adaptation rule

After real language scores are visible, the following are prohibited:

- changing null type;
- changing null replicate count downward;
- changing seed;
- changing smoothing;
- changing layout preservation;
- selecting only the weakest null family.

Every reported candidate must be shown against **all four null families**.

---

# 12. Search-lock consequence

Completion of this specification and passing the generator invariants unlocks implementation
of the fixed-complexity mapping optimizer.

It does not itself authorize interpretation of lexical-looking outputs.
