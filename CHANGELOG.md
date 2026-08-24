# Changelog

## v0.7 — 2026-08-24

- tested the proposed f78r "şarap otu" reading as a falsifiable semantic anchor;
- found transcription-boundary ambiguity (`dar` + `al...`) and a critical `darall` astronomical-star-label counterexample;
- strongly weakened `daral = şarap` without discarding the local phonetic idea;
- quantified EVA `d`, `da`, and `dy` on the complete RF1b-EVA corpus;
- found `da` strongly onset-associated and `dy` overwhelmingly token-final/standalone;
- opened H05 (borrowed technical labels) and H06 (`da` as a sibilant+vowel candidate);
- added `analyze_phonetic_block.py` and a blind second-opinion prompt.

## v0.6 — 2026-08-24

- analyzed the complete uploaded RF1b-EVA corpus (5613 lines; SHA-256 recorded);
- replicated `qo` bifolio analysis on clean Quire 3;
- confirmed Quire 3 does not reproduce the Quire-1 monotonic gradient;
- quantified Quire 4 while preserving its A/hand-1 vs B/hand-2 confound;
- identified Q1's outer bifolio as a localized `qo`-poor anomaly;
- replaced pseudo-replicated unit-level significance with exact four-layer permutation context;
- added full cross-quire and page-level CSV outputs;
- added H04 (`qo` block candidate);
- added a blind second-opinion protocol and first neutral review prompt.

## v0.5 — 2026-08-24

- selected Quire 3 as the next clean `qo` bifolio replication set;
- identified Quire 4 as confounded by Currier language/state and proposed hand;
- added a cross-quire confound rule to the methodology;
- added `analyze_all_quires_qo.py` to scan q/qo while reporting `$Q/$B/$L/$H`;
- prohibited raw bifolio-gradient interpretation when hand/language strata are mixed.

## v0.4 — 2026-08-23

- replicated the bifolio-frequency test on Quire 2 using RF1b EVA;
- falsified a universal monotonic outer-to-inner q gradient;
- found a low-high-low-high q pattern across surviving Quire 2 bifolios;
- confirmed 89/90 q occurrences are token-initial and all token-initial q are `qo`;
- promoted `qo` to the first explicit multi-glyph segmentation candidate;
- added `analyze_eva_qo_bifolio.py`.

## v0.3 — 2026-08-23

- weakened the B4-late-introduction interpretation using a stationary-frequency null;
- discovered a strong D1 / EVA-q gradient across Quire 1 physical bifolio layers;
- added control-glyph comparisons and statistical caveats;
- added `analyze_bifolio_gradient.py`;
- defined cross-quire replication as the next falsification test.

