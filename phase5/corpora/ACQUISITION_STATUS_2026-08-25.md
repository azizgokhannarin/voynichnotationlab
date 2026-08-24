# Campaign-1 Historical Corpus Acquisition Status

Date: 2026-08-25

## Completed in this checkpoint

- concrete manifest schema created;
- official source/version identifiers frozen;
- ReN v1.1 TEI archive's repository-published MD5 recorded separately;
- LatinISE current pre-search release frozen as v6;
- local SHA-256 policy made explicit;
- reproducible local hashing/freezing utility added;
- Old Czech remains explicitly blocked until a stable bulk payload is obtained.

## Important limitation

The execution environment used for this checkpoint could verify public repository metadata
but could not materialize the required historical-corpus binary payloads into the working
filesystem. Therefore no `local_sha256` has been fabricated.

Campaign 1 mapping search remains locked.

## Unlock condition

For every non-blocked primary corpus:

1. acquire exact official payload;
2. verify any repository-published checksum;
3. filter to the preregistered historical window;
4. record usable token count;
5. compute local SHA-256;
6. set status to `FROZEN_LOCAL`.

Only then may null generation and mapping optimization start.
