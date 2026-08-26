# Phase 16 preregistration: exact-identity recurrence and burstiness

Freeze date: 2026-08-26

Status: frozen before opening any Phase-16 real-corpus result.

## Question

Does the exact identity of a surface token recur at distinctive page, line or
within-line distance scales after its fixed corpus frequency is controlled?

This is an instrument-calibration question. It is not a decipherment test and
does not authorize ranking H_C, H_D or H_G.

## Inputs and access lock

- Reuse the canonical Phase-15 line corpora without changing tokenization.
- Use `VALIDATION` records only.
- Keep Voynich and control `final_test` records sealed.
- Preserve token strings byte-for-byte after JSON decoding: no case folding,
  Unicode normalization, punctuation removal, abbreviation expansion, class
  induction or spelling normalization.
- Run in this order: synthetic fixtures, known-content strong renderer,
  diplomatic CREMMA control, Voynich.
- Do not open the later corpus until the preceding calibration gate passes.

## Frozen metrics

Eleven exact-identity descriptors are reported:

1. excess repeated-occurrence mass within pages;
2. excess repeated-occurrence mass within physical lines;
3. fraction of all within-document identical-token pairs captured within pages;
4. fraction captured within lines;
5. occurrence-weighted page-frequency Fano factor for types with count >= 4;
6. occurrence-weighted line-frequency Fano factor for types with count >= 4;
7. identical-token pair rate between adjacent pages;
8. identical-token pair rate between pages two to four positions apart;
9. within-line identical-token pair rate at gap 1;
10. the same rate pooled over gaps 2--4;
11. the same rate pooled over gaps 5--16.

Rates pool matching-pair numerators and eligible-pair denominators; they are not
unweighted averages of token types.

## Nested fixed-frequency nulls

Every shuffle preserves exact token identity, corpus frequency and all line and
page lengths.

- `document_shuffle`: shuffle validation tokens within each manuscript and put
  them back into the frozen pages/lines. This tests document-to-page clustering.
- `page_shuffle`: shuffle within each page and restore frozen line lengths. This
  tests page-to-line clustering while holding the page inventory fixed.
- `line_shuffle`: shuffle within each physical line. This tests local order while
  holding page and line inventories fixed.

The seed base is `20260826`. Each corpus/null stream receives a SHA-256-derived
64-bit seed. Increasing the permutation count preserves the old stream as an
exact prefix.

## Inference contract

- 2,000 permutations per corpus and null family;
- two-sided plus-one permutation p-values;
- z scores use sample standard deviation;
- Holm correction at family alpha `0.01`;
- only metrics that can change under a null enter that null's Holm family;
- retain null mean, variance and 0.5%, 2.5%, 50%, 97.5%, 99.5% quantiles;
- report ratios and profiles, not a single natural-language score.

## Synthetic gates

1. IID fixture: maximum absolute comparable z <= 3.5.
2. Page-cluster fixture: document-null page repeat-mass z >= 5.
3. Short-page-return fixture: document-null adjacent-page return z >= 5.
4. Line-order fixture: absolute line-null gap-1 z >= 5.
5. Holm resolution floor must be below 0.01.

## Real-control gate

Both the known-content strong renderer and CREMMA must retain at least 5,000
validation tokens, use no final-test records, and show at least one
Holm-significant distance-resolved descriptor. Otherwise Voynich is not opened.

## Interpretation lock

A calibrated difference may identify its scale--page allocation, line
allocation or local order--but cannot by itself identify content type. No
H_C/H_D/H_G ranking, new language search, generator enrichment, latent state or
semantic/illustration crib is permitted in Phase 16.

