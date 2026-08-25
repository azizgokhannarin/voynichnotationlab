# Campaign 2 — Production Calibration Protocol v1

Frozen before production calibration results: 2026-08-25.

## Historical sample

Per branch, reserve 1536 normalized historical tokens using the deterministic seed:

    SHA256("C2|calibration-production-v1|<branch>|20260825")

- first 1024 reserved tokens: invented-script source TRAIN;
- next 512: invented-script source VALIDATION;
- all 1536 are excluded from the calibration target-LM training corpus.

The split size is fixed for computational tractability and identical across branches.

## Invented source inventory

The active invented source inventory is exactly 37 units, matching the frozen Voynich source
inventory size.

Every target class observed in calibration TRAIN receives at least one invented-source alias.
Remaining aliases are assigned deterministically to sufficiently frequent target classes.
Occurrences are deterministically cycled through a class's aliases, forcing all 37 source units
to occur in calibration TRAIN whenever the corpus contains sufficient observations (required
invariant).

Thus the positive calibration must recover a real many-to-one 37-source-unit mapping rather than
a trivially smaller 18–19-symbol substitution.

Validation may contain no invented source symbol unseen in calibration TRAIN.

## Negative calibration

Starting from the positive invented-script corpus:

- preserve the exact token-length vector;
- preserve the exact 37-unit global source-frequency multiset;
- globally shuffle source-unit occurrences and repartition by the original token lengths.

This destroys historical token-internal conditional organization while retaining source size,
marginals and lengths.

## Weak-surrogate calibration test

For positive and negative calibration separately, the production weak-null budget is N=500.
Every null replicate performs within-token shuffle and reruns the complete frozen mapping optimizer.

One-sided empirical p:

    p = (1 + count(J_null <= J_real)) / 501

Calibration-positive threshold:

    p < 0.01

### Irreversible early-failure optimization

A run may stop early only when PASS has become mathematically impossible at N=500.
Since p<0.01 permits at most 4 null draws with J_null <= J_real, observation of the fifth such
null draw irrevocably implies FAIL. This shortcut can never create a PASS; PASS still requires all
500 replicates.

## Instrument validity

For every active branch:

- positive calibration must PASS;
- matched negative must NOT PASS.

The first positive failure is sufficient to trigger the preregistered instrument-invalid stop.
The first negative false positive likewise triggers instrument-invalid stop.

No Campaign-2 Voynich surrogate validation is run unless calibration is valid.

## Engineering disclosure

Before this production protocol was frozen, runtime benchmarking exposed Dante positive objectives
under two non-production calibration sizes/seeds. Those values are engineering diagnostics only.
The production seed namespace above is distinct and was not scored before this protocol was frozen.

## Deterministic branch execution order

If an instrument-invalid stop is triggered, remaining branches need not be run. The frozen order is:

1. ReF
2. ReN
3. BFM
4. Dante
5. Latin
