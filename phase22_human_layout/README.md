# Phase 22 — Human layout, paragraph and boundary analysis

This phase replaces unrestricted surface-model expansion with a bounded,
historically human-executable question: how did the writer visibly divide
thoughts and entries on the page?

## Current evidence state

- ZL3b, IT2a and GC2a retain transcriber-proposed `<%>`/`<$>` boundaries.
- RF1b-EVA does not retain these markers.
- Transcriber boundaries are exploratory annotations, not ground truth.
- The user-supplied crop is consistent with a composite gallows/bench motor
  chunk containing ordinary-sized interior marks.
- Earlier held-out results support gallows compositionality but do not assign
  sounds or prove that the forms are capitals.

## Run the exploratory transcription scan

```bash
python3 phase22_human_layout/paragraph_scan.py \
  --zl phase22_human_layout/sources/ZL3b-n.txt \
  --it phase22_human_layout/sources/IT2a-n.txt \
  --gc phase22_human_layout/sources/GC2a-n.txt \
  --rf phase22_human_layout/sources/RF1b-e.txt \
  --quire20-stars phase22_human_layout/sources/QUIRE20_STAR_COUNTS_v1.json \
  --out phase22_human_layout/results/TRANSCRIBER_BOUNDARY_SCAN_v1.json
```

## Scope boundary

No language mapping, sound assignment or semantic crib is authorized. The next
implementation step is the TRAIN-only image geometry extractor described in
`PARAGRAPH_GEOMETRY_PREREGISTRATION.md`.
