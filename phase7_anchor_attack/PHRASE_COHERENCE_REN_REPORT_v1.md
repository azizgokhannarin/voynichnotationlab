# ReN anchor attack — phrase-coherence challenge v1

Date: 2026-08-25

Status: exploratory cryptanalytic challenge; **no final-test pages used**.

## Question

The Round-0 anchor attack produced an attractive chain under Middle Low German / ReN:

- `or -> in` gives `o -> I`, `r -> N`;
- independent TRAIN completions suggested `y -> E`, `l -> X` (`X` = frozen WG `ch` class);
- the resulting mapping makes the frequent, non-anchor token `ol -> IX`, corresponding to historical `ich` under `PHONO-WG-v1`.

This probe asks whether that apparent lexical breakthrough propagates to **historically attested adjacent word sequences**, rather than merely isolated dictionary words.

Matched alternatives from the same source token are challenged in parallel:

- `or -> in`
- `or -> en`
- `or -> am`

Both the two-symbol base anchor and the fixed first propagation wave are tested. No additional letters are learned during this probe.

## Method

1. Build ordered normalized ReN word sequences from the frozen historical corpus.
2. Build an attested historical word-bigram table without crossing document boundaries.
3. Apply each fixed partial alphabet to Voynich TRAIN and VALIDATION separately.
4. Retain adjacent Voynich token pairs only when both tokens are fully resolved and both outputs are attested ReN word types.
5. Measure:
   - how many decoded pairs are attested historical ReN bigrams;
   - mean smoothed ReN word-bigram log probability.
6. Compare each observation with 100 deterministic line-local Voynich token-order shuffles.

The shuffle preserves line membership, decoded-token inventory, lexical coverage, and mapping; it removes only actual neighbor order.

This is an exploratory challenge, not a significance campaign. The purpose is to reject visually attractive anchors that do not produce sequence coherence.

## Results

| Mapping | Split | Decoded lexical pairs | Attested ReN bigrams | Bigram-count z | Empirical p | Bigram-logP z | Empirical p |
|---|---|---:|---:|---:|---:|---:|---:|
| `or->in` base | TRAIN | 13 | 7 | -0.05 | 0.584 | 0.62 | 0.198 |
| `or->in` base | VALIDATION | 5 | 3 | 0.33 | 0.495 | 0.09 | 0.480 |
| `or->in` + `y=E,l=X` | TRAIN | 59 | 9 | 0.48 | 0.396 | -0.18 | 0.614 |
| `or->in` + `y=E,l=X` | VALIDATION | 17 | 3 | 0.01 | 0.604 | 0.04 | 0.475 |
| `or->en` base | TRAIN | 13 | 5 | -0.24 | 0.683 | 0.43 | 0.356 |
| `or->en` base | VALIDATION | 7 | 4 | 1.23 | 0.198 | 0.02 | 0.485 |
| `or->en` + `l=R` | TRAIN | 71 | 22 | 0.82 | 0.277 | -0.13 | 0.535 |
| `or->en` + `l=R` | VALIDATION | 29 | 11 | 1.84 | 0.089 | 0.70 | 0.257 |
| `or->am` base | TRAIN | 13 | 2 | -0.58 | 0.812 | -0.33 | 0.594 |
| `or->am` base | VALIDATION | 5 | 0 | -0.78 | 1.000 | -0.69 | 0.762 |
| `or->am` wave 1 | TRAIN | 151 | 8 | -0.92 | 0.881 | -0.85 | 0.812 |
| `or->am` wave 1 | VALIDATION | 50 | 2 | -0.48 | 0.802 | -0.73 | 0.772 |

## Result

The attractive `or -> in -> ol -> ich` chain **does not acquire phrase-level support**.

In particular, after adding the independently suggested `y=E,l=X` wave:

- TRAIN historical-bigram enrichment is essentially null (`z=0.48`);
- VALIDATION is exactly near null (`z=0.01`);
- target-bigram log probability is also near the shuffled baseline in both splits.

Therefore `ol -> ich` must currently be treated as an attractive lexical coincidence, not as a breakthrough.

The alternative `or -> en` produces the strongest held-out bigram-count signal (`z=1.84`, empirical `p≈0.089`) but:

- the effect is modest;
- it is not reproduced on TRAIN (`z=0.82`);
- bigram log-probability provides weak support (`z=0.70` on VALIDATION).

It is therefore not promoted either.

`or -> am` is clearly disfavored at sequence level.

## Interpretation

This is an important falsification of the first visually compelling anchor chain.

The Round-0 attack demonstrated why isolated historical-word hits are dangerous in a repetitive source corpus and a large historical lexicon. A genuine simple-substitution foothold should not stop at words such as `in`, `ich`, `inne`, or `nich`; it should improve the order-sensitive coherence of neighboring decoded words. That did not occur here.

The anchor-propagation strategy itself is **not rejected** by this one challenge. Instead, the first candidate chain is rejected as insufficient.

## Next rule

Do not hand-tune `or -> in`, `or -> en`, or `or -> am` further.

The next search should apply this phrase-coherence challenge automatically to the strongest independent Round-0 anchors across all historical branches. An anchor survives only if:

1. lexical propagation creates new constraints on TRAIN;
2. the fixed mapping retains lexical support on VALIDATION;
3. actual adjacent decoded words show order-sensitive historical phrase coherence beyond a line-local shuffle baseline.

Only after those three properties coincide should manual reading be attempted.
