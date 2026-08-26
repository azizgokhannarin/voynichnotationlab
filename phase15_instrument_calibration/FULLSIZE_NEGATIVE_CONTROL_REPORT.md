# Full-size diplomatic negative-control checkpoint

Date: 2026-08-26

Voynich final-test pages used: **NO**.

Control final-test pages used: **NO**.

H_C / H_D / H_G ranking performed: **NO**.

## Outcome first

The full-size control corpus was acquired, provenance-locked, split and run. The preregistered
power gate passed. The predictive part of the executable instrument is usable; the induced-class
MI comparison is blocked because the newly archived class implementation did not reproduce the
legacy v4.3 Voynich lag-1 result.

This is a reproducibility checkpoint, not a decipherment or hypothesis-ranking result.

## Corpus

Frozen source:

- CREMMA Medii Aevi `0.1.0`;
- commit `e681b1077cddafebb51018a19cce503431139e4f`;
- 14 Latin manuscripts dated 1300–1499;
- 90 ALTO-XML files;
- 4,422 non-empty physical manuscript lines;
- abbreviation characters and original lineation preserved.

Split results:

| split | pages | lines | tokens | manuscripts |
|---|---:|---:|---:|---:|
| TRAIN | 52 | 2,614 | 22,315 | 14 |
| VALIDATION | 18 | 872 | 6,924 | 14 |
| sealed control final test | 19 | 936 | 7,449 | 14 |

Canonical derived-corpus SHA-256:

`d0ba0dc9c95070d3dd3eae9e38ce24e849b4bed6e810018c945e828cdded8878`

All four preregistered power checks passed.

## Executable instrument regression

The archived v4.4 package contained final JSON/report artifacts but not the original script.
The new executable v2 implementation was therefore run first on the frozen Voynich TRAIN /
VALIDATION data.

### Components that reproduced the legacy qualitative/numerical behavior

| diagnostic | legacy v4.3 | executable v2 | status |
|---|---:|---:|---|
| line-local minus continuous | 0.0581 | 0.0692 bits/token | PASS |
| distant-context gain | -0.0165 | -0.0029 bits/token | PASS: no held-out benefit |
| cross-line gain | -0.0140 | -0.0358 bits/start | PASS: no held-out benefit |
| hybrid minus line-local | -0.0010 | -0.0023 bits/token | PASS |

The exact losses differ because the original class implementation is missing, but the frozen
predictive decisions and signs survive.

### Component that failed regression

Legacy Voynich class-MI shuffle z at lags 1–5:

`30.62, 2.36, -0.32, -1.17, -1.27`

Executable v2 Voynich class-MI shuffle z:

`1.24, -1.09, -0.50, -0.50, 0.48`

Therefore the v2 distributional classes are not the same effective measurement as the missing
legacy implementation. The class-MI branch is marked **NON-COMPARABLE**. It may not be used to
compare CREMMA with the legacy Voynich profile.

## Known-content strong-renderer reproduction v2

The exact LatinISE input was recovered and verified:

- `latin14.txt` bytes: 226,954,460;
- SHA-256: `74553e781f8b0fc43b5a35d76d315932f5323ae9cfd9903f3cc69c8fcd494388`;
- MD5: `15aba54f63333f86a580ec5b7a0de724`.

The new frozen renderer produced 4,200 lines and 45,197 surface tokens. This is not numerically
identical to the legacy transient renderer's 49,353 tokens, so the result is correctly versioned
as reproduction v2.

It still reproduced the core predictive content-blindness result:

- line-local minus continuous: **0.1186 bits/token**;
- hybrid minus line-local: **-0.0006 bits/token**;
- distant lags 2–4 gain: **0.0058 bits/token**;
- cross-line gain CI includes zero.

Known natural-language content can therefore still produce a strongly line-local predictive
surface under the fully executable renderer. This preserves the v4.4 interpretation correction.

## Full-size CREMMA observations

### Predictive diagnostics

| model | VALIDATION bits/token | accuracy |
|---|---:|---:|
| Position | 1.9856 | 55.65% |
| Continuous | 1.9897 | 57.97% |
| Line-local | 1.9020 | 58.20% |
| Hybrid | 1.8994 | 58.58% |

- line-local minus continuous: **0.0877 bits/token**;
- hybrid minus line-local: **0.0026 bits/token**;
- local plus lags 2–4 gain: **0.00117 bits/token**;
- cross-line gain: **-0.00497 bits/start**;
- cross-line bootstrap 95% CI: **[-0.0290, 0.0171]**.

Thus ordinary diplomatic abbreviated Latin can also look line-local under this predictive
instrument. This is a control observation, not an H_C/H_D/H_G ranking.

### Class-MI diagnostic, recorded but non-comparable

CREMMA v2 class-MI shuffle z:

`24.18, 2.04, -0.56, -0.05, -2.03`

Its shape resembles the legacy Voynich vector, but comparison is prohibited because the same v2
class implementation failed the Voynich regression. The resemblance is recorded only to prevent
selective reporting.

## Decision

1. The four-page/112-line pilot is superseded for power by the full-size corpus.
2. The full-size source, split and predictive control are complete.
3. The legacy class-MI implementation remains unrecoverable from v4.4 artifacts; its branch is
   excluded from further inference rather than silently approximated.
4. v4.3 observations remain archived and valid as historical measurements; the executable v2
   failure does not retroactively falsify them.
5. H_C, H_D and H_G remain open, unranked hypothesis classes.
6. No generator enrichment, latent-state addition, new language attack or semantic crib is
   authorized.
7. The next instrument is raw-token identity distance-resolved recurrence/burstiness, calibrated
   on controls before Voynich interpretation.

