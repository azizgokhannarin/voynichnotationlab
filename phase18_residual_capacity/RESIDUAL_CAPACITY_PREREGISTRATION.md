# Phase 18 residual information-capacity preregistration

Date frozen: 2026-08-26  
Voynich final-test pages used: **NO**

## Question and estimand

After the best bounded surface-only mechanism is frozen on TRAIN, how many
lossless code bits remain per observed token and physical line on VALIDATION?

The primary estimand is the held-out residual selection codelength in
bits/token. It is a conservative upper bound on any hidden-content bandwidth:
unexplained surface choice may carry content, procedural innovation, noise or
model misspecification. A large value is therefore **not** evidence of content.

## Frozen open-vocabulary code

Every candidate is a lossless two-part code. TRAIN types occurring at least
twice receive dictionary symbols. All other strings use an ESC symbol followed
by a byte-bigram spelling code, including an explicit end symbol. No VALIDATION
token is collapsed into an uncosted UNK class.

Four nested surface-only candidate families are compared:

1. `UNIGRAM_OPEN` — exact token identity only;
2. `LAYOUT_OPEN` — line-position and line-length buckets;
3. `PREV_SHAPE_LAYOUT_OPEN` — layout plus previous-token length, first and last
   codepoint;
4. `PREV_ID_LAYOUT_OPEN` — the preceding features plus exact previous-token
   identity.

The hierarchy uses fixed concentration 8.0, Jeffreys 0.5 base smoothing, five
position buckets and four line-length buckets. Candidate selection uses a
deterministic 80/20 page partition wholly inside TRAIN (seed `20260826`). The
winner is refit on all TRAIN records and scored once on VALIDATION. Final-test
records are neither fitted nor scored.

Primary reporting:

- total residual bits and bits/token;
- line-weighted bootstrap 95% CI for bits/token (2,000 replicates);
- mean, median and 95th-percentile residual bits/line;
- dictionary escape rate and all TRAIN-selection candidate losses.

## Known-content lossy-renderer positive control

The exact frozen LatinISE source from Phase 15 is reused. Selected 1300–1500
Latin words retain their order and are laid out with Voynich TRAIN line lengths.
Each normalized word is heavily suspended to its first normalized unit plus a
generic suspension mark; the final item of each line receives a visible
line-final variant. This is deterministic, many-to-one, short-token rendering
with substantial homography. The aligned hidden word and hidden onset are
archived for calibration only.

The positive gate passes only if all conditions hold:

1. validation contains at least 5,000 surface tokens;
2. a TRAIN-fitted onset probe gains at least **1.0 bit/token** from exact surface
   identity over layout alone;
3. a 1,000-permutation validation-label null gives one-sided `p <= 0.01`;
4. the residual-capacity estimate is no smaller than the recoverable onset
   information lower bound (numerical tolerance `1e-9`);
5. neither positive-control nor Voynich final-test records are used.

If the positive gate fails, Voynich is not opened and the estimator is
uncertified.

## Voynich decision rule

Only after the positive gate passes is frozen RF1b C1-STRUCT VALIDATION scored.

- If the 95% bootstrap **upper** bound is below `1.0 bit/token`, content-rich
  `H_C` is rejected at this representation level.
- Otherwise Phase 18 does not reject `H_C`.
- A large bound does not favor `H_C`, `H_D` or `H_G`; those classes remain open
  and unranked.

No language/key search, semantic or illustration crib, generator enrichment,
representation change or latent-state fitting is authorized in this phase.

