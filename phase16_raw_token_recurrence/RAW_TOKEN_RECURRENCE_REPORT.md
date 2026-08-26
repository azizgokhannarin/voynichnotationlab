# Phase 16: exact-identity recurrence and burstiness

Date: 2026-08-26

Voynich final-test pages used: **NO**.

Control final-test records used: **NO**.

H_C / H_D / H_G ranking performed: **NO**.

## Outcome first

The calibrated instrument finds that exact Voynich token identities are
strongly allocated to particular validation pages and physical lines. Once the
inventory of each line is fixed, however, shuffling token order inside those
lines produces no Holm-significant difference at gaps 1, 2--4 or 5--16.

The signal is therefore primarily **where token identities are allocated**, not
a simple adjacent-copy or fixed-distance recurrence rule. This is a structural
localization result, not an identification of content type.

## Reproducibility and calibration

The executable uses exact case-sensitive token strings and 2,000 permutations
for each of three nested nulls. It performs no Unicode normalization, class
compression, abbreviation expansion or language-dependent preprocessing.

The first 1,000-permutation control exposed an unreachable Holm threshold:
`11/1001 > 0.01`. The pre-Voynich erratum increased all streams to 2,000 and
restricted each Holm family to metrics that can vary under its null. The same
seeds preserve the first 1,000 draws as an exact prefix.

Synthetic calibration passed:

| gate | result |
|---|---:|
| IID maximum absolute z | 2.64 |
| page-cluster repeat-mass z | 45.82 |
| adjacent-page return z | 112.25 |
| line-order gap-1 z | -35.77 |

The IID fixture did not generate a frequency-driven false positive, while the
three intended clustering scales were detected.

## Real controls

### Known-content strong renderer

The 8,961-token validation surface contains known medieval Latin content behind
the frozen renderer.

- page repeat mass was 14.5% above the document null (`z = 15.25`);
- exact adjacent recurrence was completely suppressed (`z = -7.94` against the
  within-line shuffle);
- gap 2--4 recurrence was 27.0% above the within-line null (`z = 3.89`,
  Holm-significant);
- gap 5--16 was not Holm-significant after the line inventory was fixed.

### Full-size CREMMA diplomatic control

The 6,924-token validation split retains original manuscript lineation and
abbreviation signs.

- gap-1 recurrence was 81.2% below the within-line null (`z = -5.17`);
- gap 2--4 was 39.7% above it (`z = 4.63`);
- gap 5--16 was not different after line inventory was fixed;
- physical-line repeat mass remained above both document and page nulls.

Thus known linguistic content does not produce a scalar "more repetition"
signature. It produces avoidance and recurrence at different scales, so a
distance profile is required.

## Voynich VALIDATION

The run used 45 validation pages, 1,024 physical lines and 7,596 exact tokens.
All 46 final-test pages remained sealed.

### Allocation scale

| descriptor | observed/null | z | Holm p |
|---|---:|---:|---:|
| page repeat mass vs document shuffle | 1.372 | 32.95 | 0.00550 |
| line repeat mass vs document shuffle | 2.265 | 14.08 | 0.00550 |
| line repeat mass vs page shuffle | 1.220 | 3.55 | 0.00600 |

Exact identities are therefore strongly clustered into particular pages and,
within those pages, into particular physical lines.

### Order after line inventory is fixed

| distance | observed/null | z | Holm p | decision |
|---|---:|---:|---:|---|
| gap 1 | 1.189 | 1.58 | 0.2469 | not significant |
| gaps 2--4 | 1.054 | 0.82 | 0.4298 | not significant |
| gaps 5--16 | 0.816 | -2.36 | 0.0540 | not significant |

None survives the frozen Holm alpha of 0.01. The apparent distance effects under
the broader document null are explained by which tokens were assigned to the
same page and line, not by their order inside a fixed line inventory.

## Decision and limits

1. The raw-token instrument passed synthetic and real-control calibration.
2. Voynich exact-token recurrence is strongly page- and line-clustered.
3. There is no calibrated evidence here for a fixed within-line copy distance.
4. The profile differs from both linguistic controls, which retain significant
   within-line distance structure.
5. That difference cannot by itself decide whether Voynich carries language,
   structured non-linguistic data or autonomous procedural output.
6. H_C, H_D and H_G remain open and unranked.
7. No new language attack, semantic crib, generator enrichment, latent-state
   fit or final-test access is authorized.

The next step is a preregistered structured-data control battery. It must use the
same frozen instrument and determine whether record/table/list-like content can
produce the observed allocation-without-order profile before any hypothesis
comparison is attempted.

