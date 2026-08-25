# Campaign 1 — TRAIN + VALIDATION branch results

Date: 2026-08-25

Status: **mappings frozen; final test not scored**.

These are branch-level development results. Raw cross-entropies across different target-language models are **not directly comparable**. The preregistered primary comparison requires null-standardization, which was subsequently found to be undefined for Null B/D under the frozen design.

| Branch | Train H | Validation H | Complexity | Adjusted validation J | NULL units | Mapping SHA-256 |
|---|---:|---:|---:|---:|---:|---|
| ReF | 6.458390 | 6.431762 | 9.0 | 6.566762 | 0 | `dafcb63380e18076f904e78a1cad8826328d8f8986afdcce919c3c81420fc3e6` |
| ReN | 6.654947 | 6.628248 | 9.0 | 6.763248 | 0 | `95e26cec2f624f0e01338a2802120146e573a0795e250f25c050b3035c31f978` |
| BFM | 5.855482 | 5.818446 | 9.5 | 5.960946 | 0 | `f887a65b5184c9aa8fad83bf3727c5e55b8b69b9fe5400868d31e806d287c142` |
| Dante | 5.766990 | 5.730624 | 9.0 | 5.865624 | 0 | `4ae1ba5f53188a7661c84ce9fdee4223dfef3c32c69c6a04245a75ddd8b25d5d` |
| Latin | 5.888030 | 5.865254 | 9.0 | 6.000254 | 0 | `200485de8010e30280f06bc8aa55f4754ed8d72ef30c62b7a6bb68f46e67c6b0` |

## Observations

### O1 — held-out transfer exists numerically

For all five branches, validation loss is close to and slightly below the corresponding TRAIN loss. This means the selected mappings do not show an obvious train→validation collapse under the current token-local objective. It does **not** identify a language, because optimized matched-null calibration is required.

### O2 — no optimizer selected a NULL source unit

All five selected mappings use zero NULL assignments. Thus the allowed two silent units were not needed by the current objective.

### O3 — complexity is at the minimum collision cost implied by inventory size

The Voynich source inventory has 37 units. ReF, ReN, Dante and Latin target inventories have 19 classes, so a mapping using every target class necessarily has at least 18 many-to-one collisions and complexity `18 × 0.5 = 9.0`. BFM has 18 target classes, yielding minimum collision complexity `19 × 0.5 = 9.5`. Every selected mapping reaches that minimum and uses every available target class.

This also reveals a limitation of the Campaign-1 collision penalty: once all target classes are used, it does not distinguish a balanced collision profile from a highly concentrated one. This parameter is now frozen and cannot be changed inside Campaign 1.

Largest source→target concentrations:
- ReF: N:6, S:4, I:4, T:3
- ReN: I:6, T:5, J:4, K:4
- BFM: E:14, S:3, I:3, A:3
- Dante: A:7, I:4, S:4, O:3
- Latin: A:9, E:4, K:3, I:3

### O4 — branch mappings are not semantic readings

The optimizer minimizes phonotactic loss. A unit→class assignment is therefore a statistical candidate mapping, not a word translation or decipherment. No lexical-looking output is treated as evidence.

## Final-test status

The 46 frozen final-test pages were not scored. Campaign 1 was stopped at the null-design gate before final-test opening.
