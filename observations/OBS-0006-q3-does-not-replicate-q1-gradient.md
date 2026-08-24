# OBS-0006 — Clean Quire 3 does not replicate the Q1 gradient

Quire 3 is `$L=A`, `$H=1`, `$I=H` across all four physical bifolio layers.

`qo` per 100 tokens:

    7.94 -> 12.90 -> 11.21 -> 10.38

The sequence is non-monotonic and does not reproduce Q1's outer-to-inner rise.

This weakens any universal physical-bifolio-depth explanation.
