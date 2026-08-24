# Data provenance

Large third-party manuscript images and transliteration corpora are not vendored into this repository by default.

## Primary source

René Zandbergen, RF1b reference transliteration:
https://www.voynich.nu/data/sta/RF1b.txt

Documentation:
https://www.voynich.nu/transcr.html

STA1:
https://www.voynich.nu/data/sta/STA1_def.pdf

Analytical alignment alphabet:
https://www.voynich.nu/extra/sta-aaa.html

Always record source, version, retrieval date, and checksum where possible.
Never silently substitute another transcription.


## RF1b full EVA mirror used in v0.4

https://github.com/Workwrite-Niidome/voynich-manuscript-analysis/blob/master/archive/data/RF1b-e.txt

Official transliteration resource index:
https://www.voynich.nu/transcr.html


## Exact local input used for v0.6

- filename: `RF1b-e.txt`
- header: `#=IVTFF Eva- 2.0 D 9`
- line count: 5613
- SHA-256: `e7d3238e35743e06c63367a933909ec37b1e2de7ada3a1b449447eafa1918782`

The corpus is intentionally not included in release ZIPs. Reproduce by placing the exact
file locally and verifying the checksum above.
