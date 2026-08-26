# Phase 20 cross-phase synthesis and identifiability audit

Date: 2026-08-26  
New Voynich model fitted: **NO**  
Voynich final-test pages used: **NO**  
Hypothesis ranking performed: **NO**

## Executive decision

The frozen audit returns:

> `CONTINUE_BOUNDED_ONLY`

The exact prior `STOP_INTERNAL_EVIDENCE` condition is not satisfied, but no
current model is eligible for `OPEN_FINAL_TEST`. One narrow continuation is
authorized: the deferred Phase-14 generator ladder containing only line-final
realization, copy/modify adjacency and productive vocabulary innovation. No new
latent state, unrestricted model search, language search or semantic crib is
authorized.

## Cross-phase evidence

| Phase | Calibrated result | What it closes | What remains open |
|---|---|---|---|
| 13 | Four language attacks converge on LM fit without phrase-order recovery | Direct fixed-unit/fixed-boundary bounded-homophony mapping | Strong renderer H_C, H_D, H_G |
| 14 | Simple line-reset generator matches only 4/18 metrics | Simple first-order H_G subclass | Bounded copy/modify/innovation H_G, H_C, H_D |
| 15 | Strong-rendered known Latin and full diplomatic Latin reproduce line-local diagnostics | Class-locality and line-local advantage as content-type discriminators | H_C, H_D, H_G |
| 16 | Exact identities cluster by page/line, not by within-line order | No content class | Cause of allocation structure |
| 17 | Unordered real transaction/tally data reproduces the qualitative phenotype at much larger scale | Using that phenotype to reject broad H_D | Quantitative/medieval H_D match, H_C, H_G |
| 18 | Certified capacity upper bound is 12.372 bits/token | Low-bandwidth rejection of H_C does not trigger | H_C, H_D, H_G |
| 19 | Binary line-HMM gain is not bootstrap/prequential robust | Frozen robust binary-state subclass | Other mechanisms; broad H_C/H_D/H_G |

The accumulated evidence establishes a strongly constrained, layout-sensitive
surface with page/line allocation structure. It does not identify what, if
anything, supplies the remaining token choices.

## Hypothesis audit

### H_C — linguistic content behind a strong renderer

State: **OPEN, UNRANKED**.

The direct fixed-boundary/low-homophony subclass is closed. The stronger
many-to-one, mixed-granularity and layout-sensitive renderer subclass survives:
known language under such a renderer defeated the earlier class-space
discriminator, and Phase 18 found ample residual upper-bound capacity. The lack
of a robust binary line state does not reject content.

### H_D — structured non-linguistic content

State: **OPEN, UNRANKED**.

Phase 17 supplies an existence proof for the qualitative recurrence phenotype,
not a quantitative or historical mechanism match. No test has shown that
Voynich token transitions align with a value ordering, increment relation,
record schema or attested medieval data genre. This discriminator remains open.

### H_G — autonomous procedural generation

State: **OPEN, UNRANKED**.

The simple first-order line-reset generator is rejected, and the binary
line-state extension does not transfer robustly. But the specific surface
mechanisms already observed before recalibration—copy/modify adjacency,
line-final realization and vocabulary innovation—have never been combined in a
bounded generator and tested against the calibrated recurrence battery. The
broad hypothesis therefore cannot be closed.

### H_T — transcription/palaeography/production confound

State: **OPEN CONFOUND**.

Layout, abbreviation, production chronology, scribal variation and
transcription choices can generate several measured effects. Phase 20 does not
attempt to rank or absorb H_T into another class.

## Four-part STOP-rule audit

| Required component | Status | Evidence |
|---|---|---|
| Pipeline certified on controls | **Met** | Full-size CREMMA, strong/lossy renderer, structured data, synthetic recurrence and latent-state controls |
| Bounded copy/modify generator matches full held-out battery | **Not met** | Only the simple generator was tested; it matched 4/18 metrics |
| Residual capacity below text bandwidth | **Not met** | Upper bound 12.372 bits/token; preregistered threshold 1 bit/token |
| Quantitative match to an attested non-linguistic record genre | **Not met** | Phase-17 match was qualitative and used modern transaction/tally data |

Only one of four components is satisfied. Therefore the prior STOP rule cannot
license the statement that content versus generation is internally undecidable
and exhausted. Conversely, three missing components do not license arbitrary
model expansion.

## Why final-test remains sealed

The final 46 pages are a one-shot resource. No current model makes a new,
directional prediction on a metric that was not already used for Validation
selection or description. Opening final-test now would merely repeat known
statistics and convert the sealed partition into another exploratory set.

A future final-test request must identify in advance:

1. one frozen representation and parameter set;
2. a directional primary prediction not tuned on Validation;
3. a calibrated effect-size or likelihood threshold;
4. a single interpretation for pass, fail and indeterminate outcomes;
5. no post-access model revision inside the same confirmatory claim.

## Authorized next experiment

Phase 21 may implement the already deferred bounded generator ladder:

1. frozen Phase-14 simple generator baseline;
2. line-final realization only;
3. copy/modify adjacency only;
4. productive vocabulary innovation only;
5. one combination containing exactly those three modules.

Each module must have a fixed parameter budget and be fitted on TRAIN only. The
primary held-out battery must include the original 18 Phase-14 metrics and the
frozen Phase-16 raw-token recurrence profile. Parameter-matched zero-mechanism
and known-mechanism controls must precede Voynich interpretation. The binary or
larger latent-state module is excluded.

If every bounded model fails transferable metrics, the tested enriched H_G
subclass can be closed. If one succeeds, H_G remains possible but is not proven;
H_C and H_D can render similar surface mechanisms. In either case final-test
does not open automatically.

## Current safe conclusion

Voynich token production is strongly constrained, productive and sensitive to
page/line allocation. Direct simple language mapping, a simple first-order
generator and a robust binary line-state explanation are individually
insufficient at their frozen scopes. Strong-renderer content, structured data
and a bounded copy/modify/innovation generator remain observationally open.
The project has narrowed its next step to one pre-existing falsifier rather than
reaching either a decipherment or an identifiability STOP.

