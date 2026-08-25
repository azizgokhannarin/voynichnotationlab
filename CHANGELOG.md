# Changelog

## v2.6 — 2026-08-25

- locally froze the LatinISE v6 Campaign-1 payload;
- verified `latin14.txt` against the published LINDAT MD5;
- computed local ZIP and payload SHA-256 values;
- parsed LatinISE `<doc>` metadata and applied the preregistered 1300–1500 date-overlap filter;
- recorded 61 selected documents and 667715 vertical token lines;
- added the frozen LatinISE historical-window manifest without running any Voynich-language search.

## v2.5 — 2026-08-25

- locally froze BFM2022 and DanteSearch official Campaign-1 payloads;
- computed local SHA-256 and verified DanteSearch's published MD5;
- verified selected BFM TEI payloads against NAKALA per-file SHA-1 metadata;
- applied the preregistered 1300–1500 BFM date filter and recorded 2570561 selected tokens;
- froze the preregistered Dante vernacular work subset and recorded 260897 tokens;
- added per-document filtered manifests without running any Voynich-language mapping search.

## v2.4 — 2026-08-25

- created the authoritative Campaign-1 historical corpus acquisition manifest;
- separated published repository checksums from local SHA-256 provenance;
- recorded the official ReN v1.1 TEI MD5 and source payload;
- froze LatinISE version 6 as the pre-search Latin release;
- added local corpus hashing/freezing and checksum-verification utilities;
- explicitly marked Old Czech bulk acquisition blocked rather than substituting modern data;
- kept Campaign 1 mapping search locked until exact local payload hashes and filtered token counts exist.

## v2.3 — 2026-08-25

- froze concrete Campaign-1 historical corpora before language mapping search;
- selected ReF + ReN for West Germanic, BFM2022 + DanteSearch for Romance,
  Old Czech Text Bank 1.1.27 for West Slavic, and LatinISE for Latin;
- designated Corpus Corporum as a Latin robustness resource only;
- froze family aggregation rules to prevent dialect cherry-picking;
- froze coarse historical phonographic normalizers PHONO-*-v1;
- generated the deterministic page-level 60/20/20 Voynich split manifest.

## v2.2 — 2026-08-25

- preregistered Phase 5 constrained historical-language Campaign 1 before language search;
- froze West Germanic, Romance, West Slavic, and Latin as primary candidate zones;
- froze the 1300–1500 CE primary historical window;
- defined whole-page 60/20/20 train-validation-test discipline;
- defined mapping flexibility, complexity penalties, null models, stopping rules, and
  advancement/rejection criteria;
- explicitly prohibited post-hoc representation changes, per-word remapping, and held-out
  manual adjustment.

## v2.1 — 2026-08-24

- implemented Gate C with visible spaces hidden from the statistical model;
- treated each line as a continuous glyph stream and scored all possible cuts;
- used whole-page holdout plus page-level AUC bootstrap;
- found above-chance recovery of visible manuscript spaces from glyph statistics alone;
- opened H19 and retained visible spaces as meaningful generative boundaries;
- froze structural representation v1 before constrained historical-language search.

## v2.0 — 2026-08-24

- implemented Gate B2 with transparent held-out categorical likelihood models;
- compared core-internal, external-context and manuscript-state predictors;
- added whole-stem holdout to require transfer to previously unseen stems;
- found stronger transferable terminal information in core/rime shape than in local external context;
- retained smaller residual context/state effects;
- opened H18 and made Gate C the final structural gate before freezing the representation.

## v1.9 — 2026-08-24

- implemented Gate B using only non-line-final token occurrences;
- tested stem-terminal dependence against a Currier and local-context conditioned permutation null;
- found strong residual stem-specific terminal structure after layout normalization;
- quantified low-dimensional terminal-profile classes;
- reran subject/ending analysis with line-final successors excluded and found no clean person agreement;
- opened H17 and split the next question into phonographic-vs-syntactic terminal prediction.

## v1.8 — 2026-08-24

- implemented Gate A inspired by a blind external second opinion: ask what predicts terminal choice;
- compared stem-conditioned layout, local functional-context and Currier-state predictors with whole-page holdout;
- found strong residual line-position and manuscript-state information;
- found EVA `m` extraordinarily enriched at line endings within the same stems;
- showed `m` commonly alternates in families that also contain `r/l`, but with radically different line-final rates;
- opened H16 and changed the terminal model from a homogeneous suffix class to a mixed linguistic/notational layer;
- made layout-conditioned terminal normalization mandatory before Gate-B morphology clustering.

## v1.7 — 2026-08-24

- decomposed tokens into stem + provisional terminal feature (`n/m/y/r/l/s/Ø`);
- quantified vocabulary collapse and productive multi-ending stem families;
- added a non-terminal suffix-stripping control and one-terminal ablations;
- showed the `or/s/r` functional paradigm survives stem normalization;
- added direct subject-candidate × terminal-distribution tests;
- opened H15 and defined the stem × terminal × functional-class matrix as the next step.

## v1.6 — 2026-08-24

- tested EVA `y` as a productive terminal feature against multiple final-glyph controls;
- measured X/Xy base recurrence, alternate endings and contextual similarity;
- added line-final and Currier-state controls;
- demoted `DY` as an indivisible unit and promoted `Y_final` as a terminal feature;
- opened H14 and defined y-stripped stem-family reconstruction as the next test.

## v1.5 — 2026-08-24

- applied the first conservative latent-unit segmentation (`QO`, `CH`, `SH`, `DA`, `DY`);
- kept gallows atomic at token level while retaining modifier interpretation separately;
- recomputed short-token repertoire and functional classes in latent units;
- reran `or/s/r` predicate-family similarity using latent endings;
- reran repeated subject-candidate × ending contrasts;
- added H13 and a required one-unit-at-a-time ablation plan.

## v1.4 — 2026-08-24

- inferred conservative suffixal predicate/morphological stem families from EVA alone;
- compared short-token candidates by the stem families that immediately follow them;
- added the first direct subject-candidate × predicate-ending agreement probe;
- found meaningful predicate-family overlap and isolated ending preferences;
- did not find a clean repeated person-agreement paradigm;
- made latent-unit resegmentation the required next control before stronger grammatical claims.

## v1.3 — 2026-08-24

- added an explicit-subject / personal-pronoun distributional probe;
- compared short-token predecessor and +1/+2 successor distributions;
- searched for non-trivial short-token paradigms rather than spelling matches;
- added H12 and a pro-drop vs non-pro-drop discrimination plan;
- separated grammatical-gender testing from illustration-driven semantic guessing.

## v1.2 — 2026-08-24

- reduced frequent 1–3 EVA-glyph tokens to behavioural edge/context classes;
- quantified short-vocabulary concentration;
- tested right-edge candidates for 1–6-token lexical selectivity;
- tested joined/separated surface correspondences inspired by German separable particles;
- weakened that explanation for the current high-frequency candidates;
- opened H11 and made latent-unit resegmentation the next simplification test.

## v1.1 — 2026-08-24

- compared atomic EVA, gallows-factor, unique-split and analytical-stroke representations
  with whole-page five-fold held-out prediction;
- found no robust global compression winner: best atomic and full analytical models are
  effectively tied;
- showed shared gallows components outperform a trivial unique-split control at matched
  context order;
- tested all distinct 2x2 gallows factorisations and found the published graphic pairing
  best/tied-best;
- found the `p/f` component strongly enriched at token/line starts while the other
  gallows component is more Currier-state sensitive;
- upgraded H09 to moderate functional-compositional support while leaving phonetic
  decomposition open;
- added H10: a hybrid latent-unit inventory as the primary representation model.

## v1.0 — 2026-08-24

- incorporated the user-observed clef-like/gallows composite-glyph hypothesis;
- connected it to the independent analytical alignment alphabet;
- demonstrated large k/t/p/f substitution families in RF1b-EVA;
- demonstrated parallel pedestalled ckh/cth/cph/cfh substitution families;
- opened H09 for graphic vs linguistic gallows compositionality;
- changed the decipherment pipeline to infer latent units before language scoring.

## v0.9 — 2026-08-24

- corrected `dy` analysis for the strong independent terminal bias of EVA `y`;
- showed `dy` remains highly over-associated at token ends after positional control;
- quantified the strong token-onset `d+a` association;
- identified replaceable-onset/common-rime families around `aiin`, `ain`, `air`, `ar`, `al`, and `am`;
- recorded a deliberately low-confidence West Germanic `ein/sein/mein/kein/dein` probe;
- immediately subjected that probe to Currier-state, line-position, and extra-family controls;
- added `probe_rime_family.py` and an `aiin` family CSV.

## v0.8 — 2026-08-24

- visually confirmed the user-highlighted f78r two-glyph token as standalone EVA `dy`;
- linked the image location to RF1b-EVA locus f78r.13;
- quantified standalone `dy` line position;
- found strong line-final enrichment specific to standalone `dy`, while most uses remain line-medial;
- showed that general `-dy` suffix tokens are not line-final enriched;
- opened H07 for `dy` as a terminal/short-word block.

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

