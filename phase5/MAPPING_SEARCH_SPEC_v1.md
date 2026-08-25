# Campaign 1 — Mapping Search Specification v1

Frozen: 2026-08-25, before any real Voynich→language score.

## Primary hypothesis class

A frozen Voynich structural unit maps to exactly one target phonographic class or `NULL`.

- context-free primary mapping;
- at most 2 `NULL` source units;
- many-to-one mappings allowed;
- lexical/page/word-specific exceptions prohibited;
- the preregistered allowance of up to two context-sensitive rules is reserved for a later
  secondary robustness pass and is disabled in the primary search.

## Complexity

For a complete mapping:

    N_null  = number of source units mapped to NULL
    C_merge = sum_y max(0, n_y - 1)

where `n_y` is the number of source units mapped to target class `y`.

Primary complexity:

    C = 2.0*N_null + 0.5*C_merge

Reserved secondary costs:

    +3.0 per context-sensitive rule
    +10.0 per lexical exception

Lexical exceptions remain prohibited.

Complexity-adjusted objective:

    J = H + 0.015*C

The coefficient `0.015` is frozen before real scoring.

## Target phonotactic model

- token trigram model;
- explicit BOS/EOS token boundaries;
- add-0.25 smoothing;
- target model fitted only to the historical-language training corpus;
- no Voynich observations are used to fit target phonotactics.

Primary loss:

    H = total negative log2 probability / emitted target symbols

A zero-emission mapping has infinite loss.

Raw loss, emitted-symbol coverage, complexity, and adjusted loss must all be reported.

## Beam search

Source-unit order:
1. descending Voynich TRAIN frequency;
2. lexical unit label as deterministic tie-break.

Beam width:

    256

For partial mappings, unassigned units temporarily emit `<UNK>`.

Beam pruning proxy:

    J_proxy = H_train_proxy + 0.015*C_partial

Only TRAIN pages are used for pruning.

After every source unit is assigned, all surviving mappings are evaluated on VALIDATION.
The complete mapping with minimum validation `J` is frozen.

No score-dependent early stopping exists.

## Validation usage

Validation is used exactly once per complete beam survivor for model selection.
It is not used for beam pruning, target-LM fitting, representation changes, or normalizer tuning.

## Final-test guard

Final-test pages cannot be scored until the selected mapping is serialized and SHA-256 frozen.
After freeze, a changed mapping must be rejected.

Final test is scored once.

## Correctness test

Optimizer correctness is tested on a deliberately small synthetic problem where the entire
mapping space can be exhaustively enumerated.

Required invariant:

    beam optimum == exhaustive optimum

including:
- mapping dictionary;
- adjusted validation objective;
- deterministic mapping SHA-256.

This is preferable to requiring recovery of a human-designated "planted" mapping, because a
phonotactic objective can legitimately prefer an observationally equivalent or many-to-one
mapping. The regression test therefore validates the optimizer, not an assumption of
identifiability.

## Frozen anti-adaptation parameters

- trigram order: 3
- smoothing alpha: 0.25
- beam width: 256
- max NULL source units: 2
- lambda: 0.015
- NULL cost: 2.0
- merge cost: 0.5
- primary context rules: 0
- lexical exceptions: 0

Changing any of these after real candidate scores are visible requires a new campaign.
