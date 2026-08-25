# Anchor / Partial-Alphabet Propagation Attack v1

Date: 2026-08-25

Status: exploratory cryptanalytic attack, language identification not assumed.

## Central hypothesis

A historical natural-language text may have been written through a largely systematic
phonographic/substitution notation. If a short high-frequency source token is correctly anchored
to a short high-frequency historical word, the resulting partial alphabet should create
independent lexical constraints elsewhere in the manuscript.

A correct anchor is therefore expected to *propagate*. A visually attractive isolated word is
not evidence.

## Frozen v1 restrictions

The first attack uses the simplest hypothesis class possible:

- one frozen Voynich unit -> one target phonographic unit;
- mapped source units are deterministic;
- mapped target units are injective: no two active source units share one target unit;
- no NULL/silent units;
- no source unit -> digraph expansion;
- no context-sensitive rules;
- no word-specific exceptions;
- no semantic or illustration anchors;
- no final-test pages.

These restrictions deliberately test classical monoalphabetic-like substitution first.

## Source anchors

Candidate source anchors are selected from TRAIN only.

Requirements:
- token length 1..4 frozen units;
- occurrence >= 20;
- page dispersion >= 10 TRAIN pages.

Candidates are ranked by TRAIN frequency and page dispersion.

## Target anchors

Target words come from the frozen historical corpora themselves, not a modern hand-written list.

Requirements:
- normalized phonographic length equal to source anchor length;
- corpus frequency >= 10;
- length 1..4.

The most frequent original historical spelling associated with each normalized sequence is
retained for inspection.

This naturally surfaces articles, conjunctions, prepositions, pronouns and other common short
forms without manually forcing their identities.

## Pattern compatibility

A source anchor and target anchor are compatible only if they define a one-to-one partial
substitution. Thus repeated-symbol structure must agree.

Example:

    ABA cannot map to DER
    ABA can map to ANA

## Propagation evidence

After an anchor defines a partial alphabet, apply it to every source token.

Report, excluding the anchor itself:

1. `resolved_exact_occurrences`
   Occurrences of source tokens composed entirely of mapped units whose target sequence is an
   attested historical normalized word.

2. `resolved_exact_types`
   Independent source token types satisfying the same condition.

3. `unique_partial_types`
   Source types with at least two mapped positions for which exactly one lexicon sequence remains
   compatible with the current substitution constraints.

4. `extension_symbols`
   New source->target assignments implied by those unique lexical completions, when mutually
   consistent.

5. `conflicting_unique_types`
   Unique lexical completions whose implied assignments conflict with each other or the anchor.

The v1 scan does NOT automatically accept extensions. It identifies anchors capable of generating
a second wave of constraints. Automatic propagation is deferred until the top anchors can be
inspected.

## Ranking

Anchors are ranked using TRAIN only:

    score =
        resolved_exact_occurrences
        + 5 * resolved_exact_types
        + 3 * unique_partial_types
        + 2 * consistent_extension_symbols
        - 5 * conflicting_unique_types

The score is a search heuristic, not a statistical significance measure.

VALIDATION is never used for ranking. For the top TRAIN anchors, the frozen anchor mapping is
applied unchanged to VALIDATION and the same lexical-coherence diagnostics are reported.

## Breakthrough criterion

No numerical score alone constitutes a decipherment.

A branch becomes qualitatively interesting only if an anchor produces a chain such as:

    anchor
      -> multiple independent exact/near-exact lexical constraints
      -> mutually consistent new symbol assignments
      -> increased lexical resolution after expansion

with the same alphabet across many token families and held-out pages.

A few attractive strings such as `?ich`, `?et`, `?in` are explicitly insufficient.

## Failure interpretation

If no candidate language develops self-reinforcing propagation under this simple v1 model, the
result is evidence against simple one-to-one substitution at the frozen-unit level. It does not
exclude a natural underlying language; it would motivate reassessing unit granularity or a more
complex notation layer.
