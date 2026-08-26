# Pre-Voynich permutation-resolution erratum

Date: 2026-08-26

This erratum was frozen after the first control run exposed a mathematical
resolution error and before Voynich VALIDATION was opened.

The preregistration initially specified 1,000 permutations and applied Holm to
all 11 descriptors under every null. The smallest possible plus-one p-value was
`1/1001`; multiplying by 11 gives `11/1001 = 0.010989...`. The stated family
alpha of `0.01` was therefore unreachable even in principle.

The correction is mechanical, not result-selected:

1. increase every permutation stream from 1,000 to 2,000;
2. retain the same seed derivation, so the first 1,000 draws are an exact prefix;
3. apply Holm only to descriptors that can vary under the given null;
4. rerun synthetic calibration and both real controls from the beginning;
5. discard the 1,000-permutation outputs from the deliverable;
6. keep Voynich closed until the corrected control gate passes.

At 2,000 draws the worst-case 11-metric floor is `11/2001 = 0.005497...`, below
the frozen alpha. Invariant descriptors remain reported for audit but receive no
p-value or Holm decision under that null.

