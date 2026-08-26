# Phase 21 preregistration — transcription and palaeography robustness

Date frozen: 2026-08-26  
New Voynich model fitting authorized: **NO**  
Challenger VALIDATION scoring authorized by this document: **NO**  
Voynich final-test access: **NO**  
Hypothesis ranking: **NO**

## 1. Purpose

The project currently has four exact-surface claims whose invariance to an
independent transcription is unknown. Phase 21 asks whether those properties
belong robustly to the manuscript or depend materially on the chosen
transliteration/token-boundary decisions.

This is an `H_T` gate. It is not a decipherment, language attack, generator
test, content classifier or hypothesis-ranking phase.

## 2. Why the generator ladder is cancelled

The Phase-20 ladder proposed line-final realization, copy/modify adjacency and
productive vocabulary innovation after those deficits had already been
observed on the repeatedly reused VALIDATION pages. Evaluating repaired models
on the same target battery would measure engineered sufficiency, not an
independent discriminator. The ladder is therefore cancelled as an evidential
experiment.

## 3. Source independence

The current canonical `RF1b-e` reference is an automatically produced
combination of ZL and GC. Therefore:

- `IT2a` (Takeshi Takahashi lineage) is the primary independent challenger;
- `ZL3b` and `GC2a` are component-sensitivity controls only;
- neither ZL nor GC may be counted as an independent replication of RF;
- Yale Beinecke MS 408 images are the adjudication authority.

Exact payload hashes remain pending. No challenger VALIDATION metric may be
computed until a second, pre-analysis freeze records those hashes.

## 4. Frozen page policy

- Existing TRAIN and VALIDATION page membership remains unchanged.
- The 46 Campaign-1 final-test pages may not be emitted by the Phase-21 parser,
  scored, aligned for content analysis or used to set any rule.
- Source readers must apply the page allowlist before returning token text and
  must record zero final-test tokens emitted.
- The older Gate-C boundary study used all 227 pages before the Campaign-1
  final-test contract existed. Its AUC is historical/development evidence and
  cannot provide a new confirmatory final-test claim.

## 5. Frozen target claims

Only four pre-existing claims may be evaluated:

1. document-null page exact-token repeat mass is above null;
2. document-null physical-line exact-token repeat mass is above null;
3. EVA `m` is strongly enriched at physical line ends relative to internal
   occurrences under the frozen stem/layout comparison;
4. visible spaces occur at distinguishable glyph-statistical environments
   relative to internal cuts.

No new metric may be promoted to replace a failed target claim.

## 6. Boundary policies

Two policies must be frozen before challenger VALIDATION scoring:

- `DEFINITE_ONLY`: definite spaces are boundaries; uncertain spaces are
  joined;
- `INCLUSIVE_UNCERTAIN`: definite and explicitly uncertain spaces are treated
  as boundaries.

The primary policy must be selected using documentation and TRAIN-only image
adjudication, not by which one better preserves the RF VALIDATION result. The
other policy is a mandatory sensitivity result and cannot rescue a primary
failure.

## 7. Two-stage analysis freeze

### Stage A — authorized now

1. Acquire exact IT2a, ZL3b and GC2a payloads.
2. Record URL, version, retrieval date, byte count, line count, header and
   SHA-256.
3. Implement format parsers and locus alignment using TRAIN pages only.
4. Freeze the common basic-EVA/STA projection using source documentation and
   TRAIN only.
5. Freeze an image-adjudication sample and a structured decision form without
   computing downstream metric changes.
6. Estimate transcription measurement error and equivalence tolerances using
   TRAIN only.
7. Freeze all code, seeds, tolerances, coverage gates and interpretation in
   `PHASE21_ANALYSIS_FREEZE_v2.json`.

### Stage B — not authorized by v4.9.1

Only after Stage A passes and v2 is hash-locked may the primary IT2a challenger
be scored on VALIDATION. ZL/GC component sensitivities must be reported but do
not count as independent replications.

## 8. Image adjudication

The adjudication protocol must distinguish:

- glyph-identity disagreement;
- definite versus uncertain boundary disagreement;
- physical line-end disagreement;
- unreadable/damaged/intruded text;
- locus-alignment error.

Adjudicators must not see downstream metric changes. If two independent human
readers cannot be obtained, the checkpoint must state `ADJUDICATION_LIMITED`
and may not claim palaeographic ground truth; it may report only
cross-transcription sensitivity.

## 9. Global decision rule framework

Exact equivalence tolerances will be derived and frozen from TRAIN-only
adjudication/control variability. Arbitrary percentages are prohibited.

For each target claim, Stage-A v2 must define:

- directional invariance;
- an effect-scale equivalence interval;
- minimum aligned coverage;
- page/bootstrap unit;
- treatment of missing or uncertain loci.

The global outcome is frozen as:

- `PASS_STRONG`: all four claims pass directional and equivalence gates;
- `PASS_REVISED`: exactly one claim fails and is permanently withdrawn; the
  other three pass without changing their rules;
- `FAIL_H_T`: two or more claims fail;
- `INDETERMINATE`: acquisition, coverage, harmonization, power or adjudication
  gates fail.

No outcome authorizes hypothesis ranking.

## 10. Outcome-contingent actions

### `FAIL_H_T`

- stop exact-token surface-model expansion;
- withdraw failed claims;
- pivot to palaeographic/transcription work;
- no generator, language, capacity, latent-state or final-test work.

### `PASS_REVISED` or `PASS_STRONG`

- freeze and publish only the surviving transcription-robust surface
  characterization;
- do not automatically authorize Phase-21 generator fitting;
- continue internal inference only if an independently attested historical
  mechanism supplies a finite model and a genuinely unused directional
  prediction.

### `INDETERMINATE`

- report the gate as unresolved;
- fix only the named acquisition/alignment/adjudication defect;
- no Voynich mechanism expansion is permitted.

## 11. Program-level STOP rule

The former four-part conjunction is withdrawn. The replacement is:

> After the robustness gate, internal surface-statistical expansion stops
> unless an independently attested historical mechanism, fixed without new
> Voynich metric inspection, supplies one directional unused prediction, one
> proper-score/likelihood decision and an irrevocable outcome interpretation.

“A broader model remains untested” is not authorization to continue.

## 12. Final-test rule

Final-test remains sealed. Passing transcription robustness or improving a
generator fit is insufficient.

Opening requires a separately frozen, historically constrained mechanism with
an exact preprocessing lock, parameter set, code hash, direction, effect
threshold and pass/fail/indeterminate interpretation. The test is run once and
all outcomes terminate that confirmatory claim.

