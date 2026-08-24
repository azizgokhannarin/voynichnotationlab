# Experiment 03 — Glyph and sound-block candidates

Determine whether the data are modeled more efficiently using single visual glyphs, recurring multi-glyph blocks, stroke-level units, or mixed structural + phonographic units.

No phonetic value is assigned during segmentation discovery.

Planned metrics:
- successor/predecessor entropy;
- mutual information;
- positional entropy;
- block recurrence;
- MDL-style compression score;
- stability across hands and sections.


## Candidate block 001 — EVA `qo`

Quire 2 replication gives a strong reason to model `qo` explicitly:

- 89/90 q occurrences are token-initial;
- all 89 token-initial q occurrences are followed immediately by `o`.

Competing segmentation models:

1. `q | o` — independent units;
2. `qo` — one recurrent sound/gesture block;
3. `q(o...)` — q as a structural/prosodic operator selecting an o-initial class.

Do not assign a phonetic value until the models are compared by predictive/compression criteria.
