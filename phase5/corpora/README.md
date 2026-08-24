# Campaign-1 Corpus Acquisition Checkpoint

`CORPUS_MANIFEST_SHA256.csv` is authoritative for acquisition status.

## Rule

`local_sha256` MUST remain empty until the exact payload has actually been obtained locally.

A repository-published MD5/SHA checksum belongs in `published_checksum`; it must never be
copied into `local_sha256`.

## Search lock

The language-mapping search is blocked until all primary rows are either:

- `FROZEN_LOCAL`, with filename, byte size, SHA-256 and filtered token count; or
- explicitly `DATA_ACQUISITION_BLOCKED`.

A blocked primary corpus cannot be silently replaced.

## Current checkpoint

The manifest has been created, but historical corpus payload acquisition is not yet complete.
This is intentional: provenance is frozen before search, and unavailable binary payloads are
reported as unavailable rather than guessed.
