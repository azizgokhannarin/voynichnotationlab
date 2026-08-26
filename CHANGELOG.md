# Changelog

## v4.8.0 — 2026-08-26

- preregistered a single binary line-level latent state before viewing results;
- froze a 32 exact TRAIN-token plus `OTHER` vocabulary and visible line-position/line-length contexts;
- compared a 1,283-parameter `K=2` line-HMM against its 640-parameter `K=1` zero-state counterpart;
- generated 100 parameter-matched zero-state procedural TRAIN/VALIDATION pairs with unchanged geometry and fitting pipeline;
- observed zero-state held-out gain median -0.0413 and maximum/q99 -0.0269 bits/token, showing no synthetic false gain;
- recovered the injected persistent binary state with 0.5768 bits/token held-out gain, 0.5487 bits/token prequential gain and 99.02% label-swap-invariant Viterbi accuracy;
- passed every preregistered calibration gate before scoring real Voynich VALIDATION;
- found Voynich raw held-out gain of only 0.00432 bits/token with page-bootstrap 95% CI -0.02051 to 0.02827;
- found TRAIN-only prequential/MDL gain of -0.06020 bits/token, so added state complexity did not transfer;
- recorded high fitted self-transition probabilities as non-robust training structure rather than hidden-content evidence;
- detected no robust transferable binary line state under the frozen three-condition rule;
- did not authorize a larger state space, hypothesis ranking, final-test opening, language search or generator enrichment;
- selected a cross-phase synthesis and identifiability/stop-rule audit as the next stage;
- documented a terminal-summary-only hash-label erratum while preserving the preregistered instrument byte-for-byte.

## v4.7.0 — 2026-08-26

- preregistered residual selection entropy as a lossless held-out codelength and an upper bound on hidden-content bandwidth;
- froze four open-vocabulary bounded surface-code families using TRAIN-internal deterministic page selection;
- charged unseen strings through an ESC plus UTF-8 byte-bigram spelling code instead of a free UNK class;
- added deterministic low-capacity, hash-integrity, OOV and renderer fixture tests;
- built an aligned many-to-one heavy-suspension renderer from the exact frozen LatinISE source and Voynich TRAIN line geometry;
- passed the positive gate on 6,086 validation tokens, recovering 3.555 bits/token of known hidden onset information at permutation p = 0.000999;
- measured a positive-control residual upper bound of 3.978 bits/token after selecting `LAYOUT_OPEN`;
- measured Voynich VALIDATION only after certification and selected `UNIGRAM_OPEN` wholly inside TRAIN;
- obtained a Voynich residual-capacity upper bound of 12.372 bits/token with 95% bootstrap CI 12.174–12.574;
- did not reject content-rich H_C because the upper confidence bound is not below the preregistered 1 bit/token threshold;
- treated the large bound as compatible with content, procedural innovation, noise and model misspecification rather than as evidence for a hypothesis;
- kept H_C, H_D and H_G open and unranked and kept every final-test partition sealed;
- selected a small latent-state test with parameter-matched zero-state procedural calibration and secondary prequential/MDL reporting as the next stage.

## v4.6.0 — 2026-08-26

- preregistered structured-data calibration before parsing either control dataset into instrument results;
- froze UCI Online Retail and UCI Mushroom source URLs, DOIs, licences, payload hashes and deterministic selection rules;
- copied only Voynich VALIDATION page/line geometry into five 45-page / 1,024-line / 7,596-token controls;
- built paired ordered/unordered quantity-tally transaction surfaces with exact per-line inventory equality;
- built raw ordered/permuted and column-qualified fixed-schema table surfaces;
- ran the unchanged SHA-256-locked Phase-16 instrument with 2,000 permutations per null on all five controls;
- found one preregistered qualitative full-phenotype match: unordered transaction quantity tallies;
- showed through the paired ordered control that within-record order is separable from page/line allocation;
- recorded that the matching control's clustering magnitudes are far larger than Voynich's and made no quantitative-match claim;
- found that all three fixed-schema table encodings fail positive line-clustering conditions;
- concluded that recurrence/burstiness cannot reject broad H_D or identify content type;
- kept H_C, H_D and H_G open and unranked and kept all final-test pages sealed;
- selected residual information capacity with lossy-renderer positive calibration as the next stage.

## v4.5.0 — 2026-08-26

- froze an executable exact-token recurrence/burstiness instrument with no class induction or normalization;
- added document-, page- and line-level nested fixed-frequency permutation nulls;
- corrected the pre-Voynich 1,000-permutation Holm-resolution error by increasing all streams to 2,000 and excluding invariant metrics from each correction family;
- passed IID, page-cluster, adjacent-page-return and line-order synthetic calibration gates;
- calibrated on the known-content strong renderer and full-size CREMMA diplomatic control before opening Voynich VALIDATION;
- found distance-resolved avoidance/recurrence structure in both linguistic controls;
- found Voynich exact-token page repeat mass 1.372 times the document null and line repeat mass 2.265 times the document null;
- found no Holm-significant Voynich within-line identity-order effect once each physical line's token inventory was fixed;
- localized the Voynich signal to page/line allocation without assigning a content type;
- kept H_C, H_D and H_G open and unranked and kept all final-test partitions sealed;
- selected frozen-instrument structured-data controls as the next calibration stage.

## v4.4.1 — 2026-08-26

- froze exact Phase 15 source URLs, versions, commits, checksums, seeds, parsing rules and page-level splits;
- added the first archived executable Phase 15 instrument and deterministic regression tests;
- recovered and hash-verified the exact RF1b-EVA and LatinISE inputs used by the project;
- preregistered and ran a full-size 14th–15th-century CREMMA diplomatic control with 14 manuscripts, 4,422 non-empty lines and a sealed control final-test partition;
- passed the full-size power gate on 872 VALIDATION lines / 6,924 tokens;
- reproduced the v4.3 predictive decisions for line reset, distant-context null and line-local model advantage;
- found that ordinary diplomatic abbreviated Latin can also produce a line-local predictive advantage and negligible distant/cross-line gain;
- failed to reproduce the legacy Voynich class-MI lag-1 value with the newly archived class implementation and therefore marked legacy-vs-control class-MI comparison non-comparable;
- preserved v4.3 observations, performed no H_C/H_D/H_G ranking and authorized no generator/latent-state enrichment;
- kept both Voynich final-test pages and the CREMMA control final-test partition sealed.

## v4.4 — 2026-08-26

- paused generator augmentation to recalibrate the H_C/H_G measurement instrument;
- selected CREMMA Medii Aevi as a diplomatic, abbreviation-preserving medieval Latin control source;
- ran a 14th-century medical-Latin pilot on Phi_10a135 and demonstrated that the available four-page sample is underpowered;
- built a large known-content Latin strong-renderer stress test with bounded mixed granularity, homophony, null insertion, nomenclator coding and line-final realization;
- found that known hidden Latin reproduces the Voynich-like signature: very strong lag-1 induced-class order, weak/null lag-2+, line-local model win and no benefit from distant class context;
- revised the interpretation of v4.3: those class-space measurements describe the surface but do not discriminate autonomous generation from hidden content behind a strong renderer;
- retained the direct-language closure and all underlying surface observations;
- required a full-size real diplomatic negative control and a new raw-token/residual-capacity instrument before any latent-content claim;
- used no final-test manuscript pages.

## v4.3 — 2026-08-26

- tested line-reset behavior with TRAIN-learned, frozen distributional token classes;
- found no held-out predictive gain from the previous line's final class at the next line start;
- tested distant-context gain after local class, line-position and token-shape information;
- found that lags 2–4 slightly worsen held-out prediction;
- directly compared continuous language-like, line-local procedural and hybrid predictive models;
- found the line-local procedural model best on VALIDATION;
- fitted a TRAIN-only procedural generator and generated 200 validation-size surrogate corpora;
- found that the simple generator reproduces immediate class behavior but only 4/18 broader
  validation metrics;
- rejected both a plain continuous surface-language model and a simple first-order line-local
  generator as sufficient explanations;
- retained transformed natural-language, richer procedural generation and hybrid mechanisms;
- used no final-test manuscript pages.

## v4.2 — 2026-08-26

- preregistered Latin as a confirmation test rather than an exploratory language search;
- predicted a generic Voynich Latin-LM fit in the 6.5–9 z band with phrase order near the null band;
- calibrated the common attack on a matched known-Latin bounded-homophonic positive control;
- observed Voynich Latin LM z 7.72 with validation phrase bigram z 0.14 and trigram z 0.30;
- confirmed the cross-language convergence prediction;
- extended the common comparison to German, Italian, French, and Latin;
- closed direct language search at the frozen-unit / fixed-boundary / one-phonographic-unit level;
- retained natural-language-with-transformation and procedural/template-generation as the primary
  competing higher-level hypotheses;
- used no final-test manuscript pages.

## v4.1 — 2026-08-26

- tested whether mild wrong segmentation alone can reproduce the Voynich language-attack signature;
- showed that syllable-like and core+ending splits of genuine ReF/Italian preserve strong phrase-order signal;
- added language-agnostic, permutation-bias-corrected token mutual-information decay;
- added within-line versus across-line dependency diagnostics;
- added unsupervised distributional token classes and frozen-class shuffle testing;
- found strong Voynich adjacent class ordering but rapid decay beyond lag 1–2;
- found that Voynich sequential dependency is strongly line-local;
- narrowed the surviving natural-language hypothesis to a more substantial transformation layer;
- increased, but did not establish, the plausibility of a procedural/template-generated surface mechanism;
- used no final-test manuscript pages.

## v4.0 — 2026-08-26

- calibrated and executed the common bounded-homophonic attack on medieval French (BFM2022);
- confirmed strong recovery and phrase coherence on a matched known-French positive control;
- found strong French-LM / lexical fit for Voynich but no robust held-out French phrase-order lift;
- closed French at the frozen-unit/fixed-boundary bounded-homophonic level;
- compared German, Italian and French under the same calibrated objective;
- recorded three-language-family convergence as evidence against the shared single-phonographic-unit
  fixed-boundary model rather than as support for a particular language;
- used no final-test manuscript pages.

## v3.9 — 2026-08-26

- re-baselined ReF and ReN under the same continuous explicit-boundary objective used for Italian;
- accelerated the bounded-homophonic search without changing its statistical model;
- demonstrated strong recovery and phrase coherence on fresh ReF and ReN positive controls;
- reran Voynich TRAIN optimization and frozen VALIDATION for both German branches;
- confirmed that high LM/lexical fit does not transfer to strong German phrase order;
- retained the German closure under the common cross-language objective;
- added a German/Italian common-objective comparison table;
- used no final-test manuscript pages.

## v3.8 — 2026-08-25

- transferred the calibrated bounded-homophonic attack to historical Italian (DanteSearch);
- discovered on the positive control that the previous token-reset trigram objective could fit within-token phonotactics without reliably recovering Italian;
- corrected the objective before Voynich scoring to a continuous explicit-word-boundary PHONO-OIT trigram;
- recovered 91.9% of the known Italian source key and 98.8% of held-out control tokens;
- froze the Voynich TRAIN mapping and evaluated unchanged on VALIDATION;
- added explicit cross-language convergence tracking;
- used no final-test manuscript pages.

## v3.7 — 2026-08-25

- incorporated five independent cryptanalytic reviews before closing the German hypothesis;
- demonstrated that strict 37-source injectivity is mathematically impossible against the
  frozen 19-unit PHONO-WG target inventory;
- added label-invariant Step-0 entropy/frequency diagnostics;
- implemented full-key bounded-homophonic stochastic search with max multiplicity 3;
- calibrated the solver on genuine ReF and ReN passages encoded into matched 37-symbol ciphers;
- showed strong held-out phrase recovery on known German positive controls;
- applied the calibrated search separately to ReF and ReN on Voynich TRAIN and held-out VALIDATION;
- found thousands of German-looking lexical hits but no held-out German phrase-order lift above
  line-local shuffle;
- closed simple/bounded-homophonic German substitution at the frozen-unit/fixed-boundary level;
- used no final-test manuscript pages.

## v3.6 — 2026-08-25

- challenged the first attractive ReN anchor chains at phrase/context level;
- compared fixed `or->in`, `or->en`, and `or->am` mappings and their first propagation waves;
- measured attested historical ReN word-bigram coherence on TRAIN and held-out VALIDATION;
- normalized adjacency evidence against deterministic line-local token-order shuffles;
- found no phrase-level support for the visually attractive `or->in -> ol->ich` chain;
- retained `or->en` only as a weak exploratory alternative, not a promoted reading;
- explicitly prohibited further hand-tuning of these three anchors;
- used no final-test pages.

## v3.5 — 2026-08-25

- started a strict 1:1 anchor/partial-alphabet substitution attack;
- built historical short-word lexicons from the frozen ReF, ReN, BFM, Dante and LatinISE corpora;
- corrected a 4-unit-anchor ranking bias by restricting starting cribs to 1–3 frozen units;
- propagated short anchors into larger Voynich token families using TRAIN only;
- reported resulting lexical coherence on VALIDATION without changing mappings;
- identified a notable ReN candidate chain `or -> in`, with tentative propagation yielding `ol -> ich`, `ory -> inne`, `rol -> nich`, `orol -> innich`, and `yor -> eyn`;
- demonstrated that alternative anchors also generate plausible lexical families, so isolated word resemblance is insufficient;
- selected phrase/context coherence as the next falsification step;
- used no final-test pages.

## v3.4 — 2026-08-25

- opened a language-independent structural reassessment of possible surface-transformation rules;
- quantified same-core boundary-variant graphs on TRAIN and transferred them to VALIDATION;
- confirmed significant adjacency enrichment for first/final substitutions but not internal substitutions;
- showed that raw boundary-pair recurrence transfers strongly to held-out pages;
- showed that most held-out predictive power is explained by marginal boundary-unit frequency,
  while pair-specific operator lift is near chance;
- therefore did not promote QO↔o, r↔l, CH↔SH or similar pairs to decoding operators;
- used no final-test pages.

## v3.3 — 2026-08-25

- aligned production positive calibration with the preregistered approximately-37-symbol source inventory by activating exactly 37 deterministic aliases;
- froze a 1536-token per-branch production calibration protocol (1024 mapping-train / 512 validation), excluded from target-LM training;
- completed 500 selection-inclusive weak-null draws for every positive calibration; all five positives had zero null hits and `p=1/501`;
- matched negatives all reached the irreversible five-hit failure boundary and were not false positives;
- declared ReF, ReN, BFM, Dante and Latin calibration instruments VALID;
- froze raw calibration values SHA-256 `c18cf2e50527d8c49a50f8391a251c5596d72d6835180a1f32fbbd3647deb02e`;
- kept Voynich final-test pages sealed.

## v3.2 — 2026-08-25

- implemented deterministic Campaign-2 weak and independent-slot surrogate generators;
- implemented deterministic positive and matched-negative calibration generators;
- added synthetic invariants for exact layout, token-length and frequency preservation;
- added an end-to-end instrument fixture where the known positive must beat the matched negative;
- reran frozen mapping-engine, Numba-equivalence and Campaign-1 null regressions successfully;
- froze generator regression output SHA-256 `01d734b73cd837b0a5b451e22a880f50357ddc3343ff8d94a7ad0b049608f697`;
- ran no real Campaign-2 Voynich surrogate distribution and kept final-test pages sealed.

## v3.1 — 2026-08-25

- preregistered minimal Campaign 2 with one primary experiment and two controls;
- froze selection-inclusive weak and slot-grammar surrogate tests at N=500 each;
- froze positive/negative instrument calibration;
- computed a non-gating entropy-budget diagnostic;
- froze Holm family-level alpha=0.01 advancement criteria;
- explicitly abandoned Campaign-1 Null B/D repairs, further structural gates, new corpora,
  parameter sweeps, context rules and lexical exceptions;
- froze terminal failure rule: failed validation ends this historical-language phonographic
  test family and returns the project to pre-language assumptions;
- final-test pages remain sealed.

## v3.0 — 2026-08-25

- reproduced the frozen 38,462-token RF1b page manifest exactly and froze the real `C1-STRUCT-v1` stream hash;
- finalized full-corpus PHONO-WG/FR/OIT/LAT validation before the first real language score;
- corrected a pre-score LatinISE century-boundary filtering bug and froze 51 documents / 451,216 tokens;
- added fixed-random 200-token normalizer audits and rule regression tests;
- added a Numba accelerator proven exactly equivalent to the frozen reference mapping engine on the regression fixture;
- ran the first real Campaign-1 TRAIN+VALIDATION searches for ReF, ReN, BFM, DanteSearch and LatinISE;
- froze all five selected mappings and SHA-256 values without scoring final-test pages;
- identified exact Null-B degeneracy and Null-D relabeling symmetry under the frozen token-local scorer;
- triggered a methodological Campaign-1 stop before final-test access rather than changing null/scoring rules after validation results were visible.

## v2.9 — 2026-08-25

- froze the Campaign-1 primary mapping-search hypothesis class before real language scoring;
- implemented deterministic `C1-STRUCT-v1` serialization;
- froze trigram/add-0.25 target phonotactics, beam width 256, max two NULL units,
  and complexity lambda 0.015;
- implemented train-only beam pruning and validation-only complete-mapping selection;
- added exhaustive-search oracle regression on a small complete mapping space;
- verified beam optimum equals exhaustive optimum and mapping hashes are deterministic;
- implemented final-test freeze/mutation guard;
- reran all matched-null regression tests successfully;
- computed no real Voynich→historical-language score.

## v2.8 — 2026-08-25

- froze Campaign-1 matched null specification before any language mapping score;
- implemented deterministic Null A/B/C/D generators with master seed 20260825;
- added structural invariant and reproducibility regression tests;
- froze 1000 production replicates per null family and add-0.5 Null-C smoothing;
- froze held-out cross-entropy direction, empirical null p-value rule, and conservative
  minimum-Z null aggregation;
- generated a hashed synthetic expected-output fixture;
- ran no real Voynich-to-language mapping optimization.

## v2.7 — 2026-08-25

- froze ReF 1350–1500 and ReN 1300–1500 historical subsets with document manifests;
- recorded 1560656 ReF and 590864 ReN token occurrences in the frozen windows;
- validated PHONO-WG/FR/OIT/LAT v1 coverage against historical-corpus samples;
- froze auditable sample transformations and preserved the <=1% preregistered acceptance rule;
- ran no Voynich-to-language optimizer; West Slavic remains acquisition-blocked.

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
