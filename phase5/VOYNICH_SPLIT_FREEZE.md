# Voynich Page Split Freeze — Campaign 1

Date frozen: 2026-08-25

Seed: `20260825`

Atomic split unit: **page**

Total pages: 227

- train: 136 (59.9%)
- validation: 45 (19.8%)
- test: 46 (20.3%)

Approximate stratification variables:
- Currier/language metadata `L`
- hand `H`
- illustration/section metadata `I`
- page token-density quartile

Manifest:
`phase5/voynich_page_split_manifest.csv`

The test pages may not be used to select mappings, normalizer rules, beam-search parameters,
or representation changes.
