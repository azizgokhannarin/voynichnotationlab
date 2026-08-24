# Atomic EVA vs decomposed-stroke prediction test

Date: 2026-08-24

## Question

Does representing common Voynich glyphs as analytical stroke components improve
out-of-page predictive compression relative to treating EVA glyphs as atomic?

This is a representation test, **not** a decipherment test.

## Input

`RF1b-e.txt`, IVTFF Eva 2.0.

To avoid uncertain high-ASCII and illegible readings, the experiment uses a clean
basic-EVA subset:

- 34,072 usable tokens
- 88.4% of raw token candidates
- all but one clean token could be mapped by the high-confidence EVA -> analytical
  stroke table used in this experiment

Whole pages, not individual tokens, are assigned to five deterministic folds. This
prevents exact same-page material from appearing in both train and test.

## Representations

### A — Atomic EVA

Common EVA glyphs such as

`k t p f ckh cth cph cfh ch sh d y ...`

are single model symbols.

### B — Gallows-factor model

Only the four normal gallows and their pedestalled partners are decomposed.

The 2x2 gallows structure is:

| EVA | left component | right component |
|---|---|---|
| `k` | L | P |
| `t` | Q | P |
| `p` | Q | X |
| `f` | L | X |

Pedestalled forms preserve the same contrast inside a common frame:

- `ckh` -> frame + L + P + frame
- `cth` -> frame + Q + P + frame
- `cph` -> frame + Q + X + frame
- `cfh` -> frame + L + X + frame

### C — Unique-split control

Each gallows is split into two deterministic pieces, but the pieces are unique to that
glyph and are **not shared** with other gallows.

This controls for the trivial fact that splitting a symbol creates predictable internal
transitions.

### D — Analytical-stroke model

The high-confidence common EVA inventory is converted to Zandbergen-style analytical
stroke/minim units.

Connections inside a glyph are retained in the symbol names so glyph boundaries are
not silently erased.

## Test 1 — held-out n-gram predictive compression

Add-alpha back-off n-gram models were evaluated by whole-page five-fold
cross-validation.

Score = bits needed for held-out text / original EVA glyph count.

Lower is better.

Representative alpha=0.1 results:

| context order | Atomic | Gallows factor | Unique split | Full analytical |
|---:|---:|---:|---:|---:|
| 0 | 4.7350 | 5.5840 | 5.7481 | 6.4419 |
| 1 | 2.8101 | 2.8155 | 2.8127 | 2.9792 |
| 2 | **2.6055** | 2.6143 | 2.6180 | 2.6653 |
| 3 | 2.6221 | **2.6181** | 2.6311 | 2.6096 |
| 4 | 2.6919 | 2.6767 | 2.6998 | **2.6364** |

The stroke representation needs a longer Markov context because one original glyph
may expand into several stroke symbols.

### Smoothing sensitivity

After testing alpha values 0.01, 0.05, 0.1, 0.5 and 1.0:

- best observed Atomic: **2.6055 bits/original glyph** (order 2, alpha 0.1)
- best observed Full analytical: **2.6067** (order 3, alpha 0.05)
- best observed Gallows factor: **2.6131** (order 3, alpha 0.05)

The best Atomic and Full-analytical scores differ by only ~0.0011 bits/glyph
(~0.04%).

### Result

**No global predictive winner.**

The fully decomposed representation catches up almost exactly with the atomic
representation, but does not beat it robustly.

This is important:

> graphic decomposability does not yet imply that the sub-strokes are independent
> linguistic units.

## Test 2 — does *shared* gallows decomposition help?

At order 3 / alpha 0.05:

- Atomic: 2.6194 bits/glyph
- official/shared gallows factor: **2.6131**
- unique-split control: 2.6219

At this matched context order, the shared-component model performs better than merely
splitting each gallows into arbitrary unique pieces.

However, the globally best Atomic hyperparameter setting remains slightly better.

Interpretation: the shared gallows structure contains useful regularity, but the evidence
is not sufficient to replace atomic glyphs throughout the model.

## Test 3 — predict gallows identity from context

A separate discriminative test predicts which base gallows class (`k/t/p/f`) appears
from:

- preceding glyph
- following glyph
- position from token start/end
- normal vs pedestalled form
- Currier state
- proposed hand
- illustration/text class

Whole pages are again held out.

### Atomic four-class classifier

Best tested regularisation:

**1.276 bits per gallows occurrence**

### Official two-component factorisation

Two binary component classifiers:

**1.300 bits per gallows occurrence**

This is ~1.8% worse predictive log-loss than predicting all four classes directly.

But the factor model uses approximately half as many output coefficients in a typical
fold:

- atomic 4-class output: ~252 coefficients
- two binary component outputs: ~126 coefficients

Thus the component model preserves most of the predictive information with substantially
greater parsimony.

## Test 4 — is the published 2x2 pairing arbitrary?

There are only three distinct ways to pair four gallows into a 2x2 feature system
(up to label/axis symmetry).

All six row/column orientations were tested.

At the same regularisation, the published/graphic pairing:

- first split: `{k,f}` vs `{t,p}`
- second split: `{k,t}` vs `{f,p}`

is the **best / tied-best** factorisation.

Factorised held-out losses:

| Pairing axes | bits/occurrence |
|---|---:|
| official A×B | **1.2997** |
| transposed B×A | **1.2997** |
| B×C | 1.3040 |
| C×B | 1.3040 |
| A×C | 1.8200 |
| C×A | 1.8200 |

The margin over the nearest alternative is small, so this is supporting evidence,
not proof.

## Test 5 — the two gallows components correlate with different metadata

Using the published/graphic decomposition:

### Right component: P vs X

The X-side corresponds to `p/f`; P-side corresponds to `k/t`.

| right component | N | line-initial token | glyph is token-initial |
|---|---:|---:|---:|
| P (`k/t`) | 15,947 | 15.38% | 15.39% |
| X (`p/f`) | 1,926 | **29.34%** | **37.69%** |

Exploratory odds ratios:

- X component vs line-initial token: **2.28**
- X component vs token-initial gallows: **3.32**

The X component therefore behaves partly like a positional/structural modifier.

### Left component: L vs Q

The Q-side (`t/p`) is more frequent in Currier A than Currier B:

- Currier A: Q-side 49.18%
- Currier B: Q-side 39.90%

By contrast the X-side proportion is almost unchanged:

- Currier A: 10.66%
- Currier B: 11.01%

This suggests that the two visual component dimensions may not be redundant:
one dimension is more text-state sensitive, while the other is more strongly tied
to onset/line position.

This is exactly the kind of partially separable behaviour expected from a
modifier + payload or feature-composition system.

It could still arise from ordinary contextual differences among four atomic glyphs.

## Current verdict

### Supported

- Gallows are graphically composite.
- Their published component pairing is not arbitrary with respect to corpus context.
- Shared components preserve almost all gallows-prediction information with roughly
  half the output parameters.
- The right-hand X/P contrast and left-hand L/Q contrast show measurably different
  contextual behaviour.

### Not supported yet

- Full stroke decomposition is **not** globally more predictive than atomic EVA.
- We cannot claim each primitive stroke has an independent phoneme.
- We cannot yet claim a gallows is a multi-phoneme syllable.

## Updated working model

Do **not** choose between atomic and decomposed representations globally.

Use a hybrid latent-unit model:

    some shapes behave atomically
    some shapes behave as recurring blocks
    some composite shapes contain modifier-like substructure

Candidate hierarchy:

    strokes
       ↓
    learned graphic compounds
       ↓
    latent functional/phonographic units
       ↓
    onset/rime/token grammar
       ↓
    historical-language scoring

## Next experiment

Infer the hybrid inventory from the corpus rather than declaring it in advance.

For each candidate compound (`qo`, `ch`, `sh`, `da`, `dy`, gallows, pedestalled gallows):

1. compare atomic vs decomposed held-out likelihood;
2. compare positional entropy;
3. measure internal mutual information;
4. measure whether components retain independent predictive value outside the compound;
5. classify the candidate as:
   - atomic-like
   - compositional
   - modifier+base
   - unresolved

Only after this inventory is frozen should phoneme and historical-language scoring resume.
