# OBS-0015 — Core shape predicts terminal class on unseen stems

In whole-stem held-out evaluation, INTERNAL core features outperform EXTERNAL local-context
features by 0.2782 bits/occurrence.

Adding external context after internal features changes held-out loss by
-0.2286 bits/occurrence.

This supports a transferable core/rime-conditioned terminal system rather than a terminal
inventory determined mainly by local syntax.
