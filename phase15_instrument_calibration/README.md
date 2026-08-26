# Phase 15 executable controls

This directory preserves the legacy v4.4 result artifacts and the first archived executable
reproduction/checkpoint implementation.

## Inputs

Download and verify RF1b-EVA:

```bash
curl -L -o RF1b-e.txt https://www.voynich.nu/data/RF1b-e.txt
sha256sum RF1b-e.txt
```

Expected SHA-256:

`e7d3238e35743e06c63367a933909ec37b1e2de7ada3a1b449447eafa1918782`

Download and verify LatinISE:

```bash
curl -L -o latin14.txt \
  https://lindat.mff.cuni.cz/repository/server/api/core/bitstreams/a72b4260-d274-4ab6-952b-d9b3d4b7172d/content
sha256sum latin14.txt
```

Expected SHA-256:

`74553e781f8b0fc43b5a35d76d315932f5323ae9cfd9903f3cc69c8fcd494388`

Acquire the CREMMA source lock without image payloads:

```bash
git clone --filter=blob:none --no-checkout --depth 1 --branch 0.1.0 \
  https://github.com/HTR-United/CREMMA-Medieval-LAT.git CREMMA-Medieval-LAT
git -C CREMMA-Medieval-LAT sparse-checkout init --no-cone
git -C CREMMA-Medieval-LAT sparse-checkout set \
  '/README.md' '/CITATION.cff' '/data-registry.csv' '/htr-united.yml' \
  '/data/**/*.xml'
git -C CREMMA-Medieval-LAT checkout
```

Expected commit:

`e681b1077cddafebb51018a19cce503431139e4f`

Every source is checked again by the build command. Full provenance and licence information is in
`SOURCE_PROVENANCE_v1.json`.

## Build canonical line corpora

From the repository root:

```bash
python3 phase15_instrument_calibration/phase15_reproducibility.py build voynich \
  --repo . --source RF1b-e.txt --out voynich_phase15.json

python3 phase15_instrument_calibration/phase15_reproducibility.py build cremma \
  --repo . --source CREMMA-Medieval-LAT --out cremma_phase15.json

python3 phase15_instrument_calibration/phase15_reproducibility.py build strong-renderer \
  --repo . --source latin14.txt --voynich-corpus voynich_phase15.json \
  --out renderer_phase15.json
```

## Run the frozen instrument

```bash
python3 phase15_instrument_calibration/phase15_reproducibility.py analyze \
  --corpus voynich_phase15.json --out voynich_result.json
python3 phase15_instrument_calibration/phase15_reproducibility.py analyze \
  --corpus renderer_phase15.json --out renderer_result.json
python3 phase15_instrument_calibration/phase15_reproducibility.py analyze \
  --corpus cremma_phase15.json --out cremma_result.json
```

Run deterministic unit tests:

```bash
python3 phase15_instrument_calibration/test_phase15_reproducibility.py
```

The generated canonical line corpora are local analysis artifacts. Their expected canonical hashes
and the committed result JSON files provide the audit lock; the large external source payloads are
not vendored.

