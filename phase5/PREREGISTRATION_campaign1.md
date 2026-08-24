# Phase 5 Preregistration — Constrained Historical-Language Campaign 1

Date frozen: 2026-08-25

Status: **PRE-REGISTERED BEFORE LANGUAGE SEARCH**

This document defines the first constrained historical-language search over the
Voynich-Notation-Lab frozen structural representation.

The goal is not to find isolated words that look plausible. The goal is to test whether
one historically plausible language family explains held-out Voynich structure better than
competing families and matched null models under a fixed-complexity phonographic mapping.

No segmentation, latent-unit inventory, terminal interpretation, or scoring rule may be
changed during Campaign 1 merely because a candidate language performs poorly.

## 1. Primary research question

Does there exist a low-complexity fixed phonographic mapping from the frozen Voynich
representation to a historically attested European natural language such that:

1. phonotactic likelihood improves on held-out Voynich pages;
2. the mapping transfers without manual adjustment;
3. the real-corpus score exceeds matched nulls;
4. the result is not driven by a few memorized token families;
5. multiple independent structural observations remain compatible with the same mapping;
6. the winning family survives multiple-comparison correction?

Campaign 1 is a **language-family discrimination experiment**, not a decipherment claim.

## 2. Frozen structural representation

The representation in `FROZEN_REPRESENTATION_v1.md` is fixed.

### 2.1 Boundaries
Visible spaces are treated as **meaningful generative boundaries**, not automatically as
modern orthographic word boundaries.

### 2.2 Units
- `QO`: promoted block candidate.
- `DA`: promoted onset/block candidate.
- `DY`: not an indivisible unit.
- final `y`: productive terminal feature.
- `ch`, `sh`: retained at EVA glyph level; linguistic atomicity remains unresolved.
- gallows `k/t/p/f`: atomic at token-segmentation level; internal graphic/functional
  components may be auxiliary features only.

### 2.3 Terminal layer
The terminal system is modeled as:

    CORE / RIME
      -> preferred terminal-profile class
      + possible grammatical modulation
      + layout / manuscript-state realization

Residual profile zones:
- L/R-like
- N-like
- Y-like

EVA `m` has a strong physical-line-final realization component.

### 2.4 Functional short-token evidence
`or / s / r` is a stable functional-paradigm candidate. No semantic label is assigned.

### 2.5 Representation lock
If a structural change becomes necessary, Campaign 1 stops. A new preregistered campaign
must be created rather than changing the representation to improve a language fit.

## 3. Working assumptions under test

1. The manuscript encodes a historically known natural language.
2. The writer uses a non-standard alphabet / graphic representation.
3. A substantial part of the representation is phonographic.
4. Writer-specific notation features may be layered over the spoken-language representation.
5. Surface Voynich tokens need not correspond one-to-one with modern orthographic words.

Failure does not imply an extraterrestrial or unknown-civilization language. It weakens one
or more of the above assumptions.

## 4. Primary candidate language families

Campaign 1 compares:

1. **West Germanic**
2. **Romance**
3. **West Slavic**
4. **Latin** as a separate learned-language baseline

The experiment compares historical language zones, not modern spellings.

## 5. Historical time window

Primary target:

    approximately 1300–1500 CE

Broader or modern corpora may be used only as documented robustness/background controls.

## 6. Candidate-language representation

Candidate corpora must be normalized to phoneme sequences or a documented historically
defensible phonographic representation.

Preferred forms:
- IPA-like phonemes;
- historical phonological normalization;
- historically appropriate grapheme-to-phoneme mappings;
- conservative phoneme classes where exact historical values are uncertain.

Modern orthographic string similarity is not a primary score.

## 7. Voynich-to-phoneme mapping class

### Allowed
- one Voynich unit -> one phoneme;
- one unit -> one predefined small phoneme class;
- limited many-to-one mappings;
- at most **2 silent/null units**;
- at most **2 context-sensitive rules**.

### Forbidden
- per-word remapping;
- per-page remapping;
- arbitrary syllabic values invented per occurrence;
- lexical exceptions added after inspecting output;
- manual correction of held-out material;
- choosing phonetic values from manuscript illustrations.

The same mapping must apply throughout the evaluation.

## 8. Complexity penalty

Model selection uses:

    SCORE =
      held-out phonotactic / sequence likelihood
      - mapping complexity
      - exception complexity

Complexity rises for:
- silent units;
- many-to-one collapses;
- context-sensitive mappings;
- explicit exceptions;
- additional transformation rules.

A more flexible mapping advances only if held-out improvement exceeds its added complexity.

## 9. Data split

### Primary split
Whole manuscript pages are the split unit:

- 60% train
- 20% validation
- 20% final test

### Stratification
Where feasible preserve approximate representation across:
- Currier A/B;
- major manuscript sections;
- hands / metadata states;
- text density.

The final test set remains untouched until mapping and hyperparameters are frozen.

### Secondary robustness
Currier A -> B and B -> A transfer may be reported separately, but is not the primary split.

## 10. Primary scoring

Primary metrics:
1. held-out phoneme-sequence log likelihood;
2. per-symbol cross entropy;
3. phonotactic sequence likelihood;
4. transfer to unseen Voynich pages;
5. improvement over matched nulls;
6. section-wise stability.

Secondary metrics:
- compatibility with attested lexical forms;
- morphological plausibility;
- syntactic consistency;
- topic coherence.

Dictionary hits and visually attractive words are not primary evidence.

## 11. Required null models

### Null A — within-token unit shuffle
Preserve token lengths and boundaries while destroying internal order.

### Null B — token-order shuffle
Preserve token inventory and within-token structure while destroying local syntax.

### Null C — matched synthetic generative corpus
Match:
- token-length distribution;
- unit unigram frequencies;
- approximate local n-gram structure;
- boundary rate.

### Null D — Voynich unit-label permutation
Randomly permute unit identities before running the same optimization pipeline.

A candidate is not interesting unless real Voynich performance exceeds the corresponding
null envelope.

## 12. Multiple-language correction

Campaign 1 must:
- report every tested family;
- report every required null;
- correct tail probabilities / p-values for the number of candidate families;
- retain negative results.

The winning language alone may not be reported in isolation.

## 13. Advancement criteria

A family advances only if all required criteria hold:

1. held-out score exceeds matched nulls;
2. improvement is distributed across many held-out pages;
3. mapping complexity stays within preregistered limits;
4. the same mapping transfers across manuscript sections;
5. no manual remapping is required;
6. performance is not dominated by a few high-frequency token families.

Strong additional evidence:
- the fixed mapping also explains at least two independent structural phenomena such as
  onset families, core/rime classes, terminal profiles, short functional paradigms, or
  gallows substitutions.

## 14. Rejection criteria

A family is rejected for Campaign 1 if:
- validation gains disappear on final test;
- performance lies inside the null envelope;
- repeated ad-hoc exceptions are required;
- held-out performance requires a post-hoc representation change.

## 15. "Interesting" is not "deciphered"

A successful Campaign 1 permits only a conclusion such as:

> Under the frozen representation and preregistered mapping constraints, candidate family X
> explains held-out phonographic statistics better than the tested alternatives and nulls.

It does not justify:
- claiming full decipherment;
- translating arbitrary passages;
- identifying the author;
- assigning meanings from illustrations.

## 16. Search order

1. freeze representation;
2. freeze historical corpora and phonological normalizers;
3. freeze page split manifest;
4. freeze null generators;
5. freeze mapping grammar and complexity penalty;
6. optimize only on train;
7. choose hyperparameters on validation;
8. freeze mapping;
9. evaluate final test once;
10. report all candidates and nulls.

The final test set may not become a development set.

## 17. Required outputs for every candidate family

- corpus provenance;
- historical date range;
- phonological normalization;
- mapping table;
- complexity cost;
- train score;
- validation score;
- final test score;
- null distribution;
- section-wise scores;
- major failure modes;
- silent/context-sensitive-rule ablation;
- reproducibility seed and command.

## 18. Campaign stopping rules

Campaign 1 ends after:
1. all four primary families complete;
2. all required nulls complete;
3. final test scores are frozen;
4. multiple-comparison correction is applied.

No new language family may be added after final-test inspection. A new candidate requires
a separately preregistered campaign.

## 19. Pre-registered interpretation matrix

### Outcome A — one family clearly wins
If one low-complexity family beats nulls and alternatives and transfers across held-out pages,
it becomes the priority for Campaign 2.

### Outcome B — several families tie
Conclude only that the frozen representation is compatible with a broader typological /
phonological region. Campaign 2 must introduce independent discriminatory constraints.

### Outcome C — all primary families fail
The known-language phonographic model is weakened. Future work may revisit notation-layer
strength, phonemic vs syllabic units, multilingual models, or the frozen segmentation — but
only in a new preregistered campaign.

## 20. Explicit anti-overfitting commitments

The following have zero evidential status by themselves:
- isolated word resemblance;
- a famous-looking label;
- a handful of plausible translations;
- phonetic values selected after seeing a candidate word;
- a page-specific mapping;
- illustration-driven phonetic assignments;
- a solution requiring large numbers of syllabic exceptions.

The unit of evidence is:

    **held-out generative performance under one fixed low-complexity mapping**

## 21. Frozen decision

Committing this document preregisters Campaign 1.

Any change to representation, candidate-family set, split logic, mapping flexibility,
complexity penalty, nulls, scoring, or advancement thresholds requires a new preregistration
before the modified search is run.
