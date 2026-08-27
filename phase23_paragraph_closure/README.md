# Phase 23 — Paragraph closure only

This phase tests one claim: a mandatory paragraph-ending mark may be fused with the final word and
may change visible form according to that word's final shape.

It deliberately excludes paragraph initials, stars, language identification and content claims.

Run from repository root:

```bash
python3 phase23_paragraph_closure/paragraph_closure_scan.py \
  --zl phase22_human_layout/sources/ZL3b-n.txt \
  --it phase22_human_layout/sources/IT2a-n.txt \
  --split phase5/voynich_page_split_manifest.csv \
  --permutations 1000 \
  --out phase23_paragraph_closure/results/PARAGRAPH_CLOSURE_TRAIN_v1.json
```
