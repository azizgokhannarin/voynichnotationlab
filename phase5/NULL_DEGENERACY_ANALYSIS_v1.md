# Campaign 1 — null-model degeneracy analysis

Date: 2026-08-25

Status: discovered **after train/validation mappings were frozen but before final-test scoring**.

This is an experiment-design result, not a language result.

## 1. Null B is exactly invisible to the frozen scorer

Null B permutes token order within each physical line while preserving every token internally.

The frozen target scorer evaluates each token independently:

    score(M) = sum_token NLL_LM( M(token) ) / emitted_symbols

Every token receives its own BOS/BOS and EOS markers. There is no cross-token transition in the
primary score.

Therefore a permutation of token order leaves, for **every mapping M**:

- the multiset of mapped token sequences unchanged;
- total negative log likelihood unchanged;
- emitted-symbol count unchanged;
- mapping complexity unchanged.

Hence:

    J(Null-B, M) = J(real, M)

for every possible mapping, and consequently the optimized score is exactly the same.

Frozen token-bag audit:

- TRAIN token-type bag SHA-256: `59dd343ba061de31c6801a2df00a14572e0e33c765ec367f72684e02c26f6c23`
- VALIDATION token-type bag SHA-256: `8fa89062871f6c97dd644ed3857d049bded95bfd1aedbecb79894e0a00976a66`

Running 1000 Null-B permutations would therefore produce a point mass, not an empirical null
distribution.

## 2. Null D is a relabeling symmetry when the optimizer is rerun

Null D applies a global bijection `pi` to Voynich source-unit labels and then, by the frozen rule,
reruns the mapping optimizer from scratch.

For any original mapping `f`, define a mapping on the relabeled source inventory:

    f_pi = f o pi^{-1}

For every token:

    f_pi( pi(token) ) = f(token)

Thus mapped target sequences are identical. The complexity function depends only on NULL count
and target-class multiplicities, both of which are also preserved.

Under exhaustive optimization, Null D is therefore mathematically isomorphic to the real search.

The Campaign-1 TRAIN inventory has 37 source units and **37 distinct training frequencies**, so
frequency-based source ordering is also carried through the relabeling without a frequency tie.

### Real ReF diagnostic, D replicate 0

Real ReF validation:

- raw loss: `6.431761512169654`
- adjusted objective: `6.566761512169654`

Null-D replicate 0 with a full optimizer rerun:

- raw loss: `6.431761512169664`
- adjusted objective: `6.566761512169664`

Difference is approximately `1e-14`, i.e. floating-point noise.

The mapping SHA-256 changes because source labels change, but the scored sequence solution does not.

## 3. Consequence for the frozen Campaign-1 scoring contract

The scoring contract requires, for each candidate, all four null families and defines primary
evidence using the minimum standardized advantage across A/B/C/D.

For Null B, and ideally for Null D:

    sd(null_loss) = 0

so the preregistered standardized score

    Z_adv = (mean(null_loss) - real_loss) / sd(null_loss)

is undefined.

This is not evidence against any candidate language. It means the primary Campaign-1 null
standardization is **not identifiable under its own frozen scorer**.

## 4. Stop decision

Campaign 1 must stop before final-test scoring rather than silently:

- dropping B or D;
- changing their definitions;
- changing the scorer to make B matter;
- keeping D but not rerunning the optimizer;
- redefining the conservative aggregation rule after seeing validation results.

Any such correction belongs to a new preregistered campaign.

## 5. Secondary diagnostic

Null A and Null C remain structurally meaningful for a token-local phonotactic scorer, but they
cannot repair the already-frozen primary four-null aggregation rule inside Campaign 1.

They may be reused or revised transparently in Campaign 2 after a new preregistration.
