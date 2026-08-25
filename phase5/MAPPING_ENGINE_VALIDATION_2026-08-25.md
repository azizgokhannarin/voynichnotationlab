# Mapping engine pre-search validation

Date: 2026-08-25

**PASS**

No real Voynich→historical-language score was computed.

Validated before real search:

- canonical `C1-STRUCT-v1` serializer round trip and deterministic SHA-256;
- trigram add-0.25 target model;
- fixed beam width 256;
- maximum two NULL source units;
- fixed complexity function and lambda 0.015;
- beam-search optimum equals exhaustive optimum on a complete small mapping space;
- deterministic mapping hash;
- final-test access blocked before mapping freeze;
- mapping mutation rejected after freeze;
- all frozen Null A/B/C/D regression tests still pass.

Combined regression-output SHA-256:

`49eca08d19a0236c0cda4b3763dee46439b313a79be4f59aa319d1342d35b42d`

This satisfies the infrastructure gate for the first real Campaign-1 TRAIN/VALIDATION branch
search. Final-test access remains locked.
