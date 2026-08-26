# Phase 21 decision report — external-review pivot

Date: 2026-08-26

## Decision

Five external model reviews independently rejected running the current Phase
21 generator ladder and agreed that VALIDATION now functions as a development
set. The project therefore replaces `CONTINUE_BOUNDED_ONLY` with:

> `AUTHORIZE_TRANSCRIPTION_ROBUSTNESS_PREREGISTRATION_ONLY`

No new Voynich model was fitted and no challenger transcription was scored.

## Evidence-status corrections

1. Legacy class-MI is retired as historical/unreproducible, not merely marked
   non-comparable.
2. Phase-18 residual capacity is a weak model-specific one-sided bound. Its
   positive control has zero escape while Voynich has 22.92% final escape, so
   low-bandwidth power in the Voynich regime was not certified.
3. Phase-19 retains only its exact frozen-model negative; no weak-effect power
   claim is added.
4. Phase-16 exact-token allocation remains a surface description pending an
   independent-transcription robustness test.
5. The Phase-20 conjunctive STOP rule is withdrawn because it can perpetuate
   testing across competing explanation branches.

## Source decision

The existing RF reference is generated from ZL and GC. They are sensitivity
controls, not independent replications. IT2a/Takahashi is the primary
independent challenger and Yale MS 408 images are the adjudication authority.

## Current authorization boundary

v4.9.1 authorizes source acquisition, parsing/alignment development on TRAIN,
image-adjudication design and a second hash freeze. It does not authorize
challenger VALIDATION scoring.

H_C, H_D and H_G remain open and unranked. H_T is the active confound under
test. All final-test pages remain sealed.

