# Null generator validation

Date: 2026-08-25

## Status

All frozen null-model invariant tests pass on synthetic fixtures.

The tests verify:

- deterministic independent replicate seeds;
- Null A token-length and global-unit-multiset preservation;
- Null B line-local token-multiset preservation;
- Null C exact layout/token-length preservation and train-inventory restriction;
- Null D bijective relabeling and exact inverse recovery.

Fixture expected-output SHA-256:

`6e068e0571abdc5fbb2eab3870ca538240f4270381f83f77227433219bd4c99e`

No historical-language mapping optimizer and no real candidate-language score was executed
during null development.

## Frozen production configuration

- master seed: `20260825`
- null generator version: `C1-NULL-v1`
- production replicates: `1000` per null family per candidate model
- Null C smoothing: add-0.5
- primary Null C mode: exact observed token-length vector + exact page/line skeleton
- primary null evidence: conservative minimum Z advantage across A/B/C/D
