# Campaign 2 — Frozen Implementation Plan
1. Implement deterministic weak surrogate.
2. Implement deterministic independent-slot surrogate.
3. Implement positive/negative calibration.
4. Seed via SHA256("C2|<component>|<branch>|<replicate>|20260825").
5. Validate generator invariants on fixtures.
6. Run calibration.
7. Run N=500 weak and N=500 slot replicates per active branch with full re-optimization.
8. Aggregate frozen families; Holm alpha=0.01.
9. Either stop, or hash-freeze and open final test once.
No experimental component may be inserted between steps 5 and 9.
