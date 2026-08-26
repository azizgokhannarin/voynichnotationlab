# Phase 17: structured-data control calibration

Date: 2026-08-26

Voynich final-test pages used: **NO**.

Voynich token identities used to build controls: **NO**.

H_C / H_D / H_G ranking performed: **NO**.

## Outcome first

One of five known structured-data controls, the unordered quantity-tally retail
surface, satisfied all four preregistered qualitative conditions of the Voynich
allocation-without-order phenotype:

1. positive document-null page clustering;
2. positive document-null line clustering;
3. positive page-null line clustering;
4. no Holm-significant line-shuffle gap effect.

This means the Phase-16 phenotype cannot reject broad H_D. It does **not** mean
that Voynich is a retail ledger, tally system or other structured-data record.
The matching control's clustering magnitudes are much larger than Voynich's, so
no quantitative match or hypothesis preference is claimed.

## Sources and frozen geometry

The controls use two independently sourced, known non-linguistic datasets:

- UCI Online Retail, DOI `10.24432/C5BW33`: transaction/invoice records;
- UCI Mushroom, DOI `10.24432/C5959T`: 8,124 fixed-schema categorical rows.

Source payloads, parsers, filters, selected-row/invoice digests and surface
encodings are frozen in the provenance/build files. Each control copies only
the Voynich VALIDATION geometry:

| pages | lines | tokens |
|---:|---:|---:|
| 45 | 1,024 | 7,596 |

No Voynich token identity or final-test information contributes to the
controls. The Phase-16 executable was used unchanged at SHA-256
`f4cb1b8e970f6982cbc1a539292ffb188c7f8aa714ad0a437f100aa455a946a4`.

## Frozen comparison profile

The first three columns below are observed/null ratios. `Line-order` reports
whether any of the three within-line gap metrics survives Holm alpha 0.01.

| corpus | page/doc | line/doc | line/page | line-order | full qualitative match |
|---|---:|---:|---:|---|---|
| Voynich VALIDATION | 1.372 | 2.265 | 1.220 | none | target |
| Retail tally ordered | 3.109 | 60.143 | 9.862 | present | no |
| Retail tally unordered | 3.110 | 60.397 | 9.859 | none | **yes** |
| Mushroom raw ordered | 1.005 | 0.661 | 0.650 | none | no |
| Mushroom raw permuted | 1.005 | 0.662 | 0.649 | none | no |
| Mushroom qualified ordered | 1.030 | 0.035 | 0.035 | present | no |

The unordered retail surface is a sign/significance-pattern match, not an
effect-size match: its line clustering is roughly 60 times its document null,
versus 2.27 for Voynich, and roughly 9.86 times its page null, versus 1.22 for
Voynich.

## Paired order ablations

### Retail quantity tally

The ordered and unordered variants contain exactly the same token multiset in
every physical line and page. Their page/line allocation descriptors are
therefore identical before Monte Carlo variation.

Ordered line-shuffle profile:

- gap 1 ratio `2.399`, `z = 85.64`, Holm-significant;
- gaps 2--4 ratio `0.977`, not Holm-significant;
- gaps 5--16 ratio `0.005`, `z = -72.92`, Holm-significant.

Unordered line-shuffle profile:

- gap 1 ratio `1.009`, not significant;
- gaps 2--4 ratio `1.007`, not significant;
- gaps 5--16 ratio `0.981`, not significant.

Thus the frozen instrument correctly separates identical record allocation
from record-order realization. An unordered multiset/tally record can have
strong page/line identity clustering with no recoverable within-line distance
rule.

### Mushroom fixed-schema table

Both raw-code variants lack positive line clustering: line repeat mass is about
0.65 of the page null. Permuting field order removes the small order deviations
but cannot change this allocation failure. Column-qualified codes suppress
within-line exact repetition even further. Fixed-schema categorical rows under
these three bounded encodings therefore do not reproduce the Voynich profile.

## Decision and limits

1. The structured-data source, geometry, power, paired-inventory and frozen-
   instrument gates passed.
2. A genuine unordered transaction/tally control reproduces the qualitative
   allocation-without-order pattern.
3. Its effect sizes are far larger than Voynich's; it is not a quantitative
   model of the manuscript.
4. The three fixed-schema table encodings do not reproduce positive line
   clustering.
5. Phase-16 recurrence/burstiness alone cannot identify content type or exclude
   broad H_D.
6. H_C, H_D and H_G remain open and unranked.
7. No new language search, semantic crib, generator enrichment, latent-state
   fit or final-test access is authorized.

The next frozen stage is residual information capacity. It must first pass a
lossy-renderer positive calibration and measure information remaining after the
best bounded surface-only predictor; latent-state testing remains later.

