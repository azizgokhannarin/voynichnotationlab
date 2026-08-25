# Campaign 1 — Null Scoring Contract v1

Status: frozen before real mapping search.

## Direction

The mapping engine's primary raw metric will be **held-out cross entropy in bits per target
phonographic symbol**.

Lower is better.

For any candidate L and null family N:

    advantage(L,N) = mean(null_loss(L,N)) - real_loss(L)

Positive advantage means real Voynich beats the null.

Standardized advantage:

    Z_adv(L,N) = advantage(L,N) / sd(null_loss(L,N))

## Required reporting

For each candidate subcorpus:

- real validation loss;
- real final-test loss;
- mean/std/quantiles for all four null families;
- empirical p for each null family;
- Z_adv for each null family;
- mapping complexity cost;
- complexity-adjusted score.

Primary candidate evidence uses the **weakest (minimum) standardized advantage over the four
null families**, not the strongest one:

    Z_conservative(L) = min_N Z_adv(L,N)

This rule is frozen now to prevent choosing whichever null is easiest to beat.

## Family aggregation

First convert each branch to its conservative null-standardized advantage.

Then:

- West Germanic = mean(ReF, ReN)
- Romance = mean(BFM, Dante)
- Latin = LatinISE

No raw cross-language cross-entropy averaging.

## Multiple testing

Holm correction over the active primary families.

West Slavic is NOT TESTED while acquisition-blocked.
