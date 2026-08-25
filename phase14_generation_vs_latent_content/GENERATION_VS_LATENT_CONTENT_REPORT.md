# Generation vs latent-content diagnostics

Date: 2026-08-26

Final-test manuscript pages used: **NO**.

This phase follows closure of direct language search. No historical lexicon, phonographic key, or
semantic crib is used.

## 1. Line reset

Distributional token classes were learned on TRAIN only and frozen.

On 979 same-page VALIDATION line starts:

- reset-prior loss: **2.1409 bits/start**
- previous-line-last conditioned loss: **2.1549 bits/start**
- cross-line predictive gain: **-0.0140 bits/start**
- bootstrap 95% CI: **[-0.0362, 0.0075]**

The previous line's final class does not improve prediction of the next line's first class.

**Interpretation:** at the frozen surface level, a Voynich line behaves much more like a reset
boundary than a transparent typographic wrap.

## 2. Distant-context predictive gain

The local model predicts frozen token class from:

- immediately previous class;
- current line-position bucket;
- line-length bucket;
- previous token length bucket;
- previous token initial/final unit.

The distant model adds classes at lags 2, 3 and 4.

Held-out VALIDATION:

- local: **2.7831 bits/token**
- local + distant: **2.7996 bits/token**
- distant gain: **-0.0165 bits/token**
- bootstrap 95% CI: **[-0.0288, -0.0035]**
- accuracy changes from **43.36%** to **42.91%**.

Distant context slightly worsens held-out prediction.

## 3. Model competition

All models use the same frozen TRAIN-derived token classes and the same multinomial learner.

| Model | VALIDATION bits/token | Accuracy |
|---|---:|---:|
| Position baseline | 2.7611 | 45.75% |
| Continuous language-like | 2.7487 | 45.43% |
| Line-local procedural | **2.6907** | 45.59% |
| Hybrid procedural + distant | 2.6917 | 45.58% |

The line-local procedural model beats the continuous model by
**0.0581 bits/token**.

Adding distant/cross-line context to it changes held-out loss by only
**-0.0010 bits/token** in the wrong direction.

This is evidence about the **surface dependency structure**. It is not proof that the manuscript
has no hidden natural-language plaintext.

## 4. Procedural generator surrogate

A simple generator was fitted on TRAIN only:

- reset at every line;
- next distributional class conditioned on previous class, line position and line length;
- token emitted from TRAIN class/position distributions;
- actual VALIDATION line lengths supplied only as fixed layout scaffolding.

It was **not explicitly fitted** to near-duplicate adjacency, exact-repeat rate, vocabulary
growth, token entropy, repetition distance, or class MI at lags 2–5.

Two hundred synthetic validation-size corpora were generated.

Only **4 / 18** measured features of the real
VALIDATION corpus fall inside the surrogate 95% interval.

### Features reproduced

- token entropy: real **9.841**, surrogate mean **9.824**
- mean token length: real **4.181**, surrogate mean **4.192**
- median within-line repeat distance: real **3.0**, surrogate mean **2.99**
- class MI lag 1: real **0.0842**, surrogate mean **0.0947**

### Major failures

- unique types: real **2605**, surrogate **2378.2**, z **7.99**
- hapax fraction: real **0.714**, surrogate **0.602**, z **13.32**
- non-identical edit-distance-1 adjacency: real **0.0464**, surrogate **0.0271**, z **8.47**
- line-final `m`: real **0.150**, surrogate **0.072**, z **10.16**
- line-final/internal `m` ratio: real **18.30**, surrogate **3.74**, z **27.53**
- class MI lag 2: z **6.82**
- class MI lag 3: z **4.40**
- class MI lag 4: z **5.23**
- class MI lag 5: z **3.71**

## Combined interpretation

The results rule out two overly simple stories at once.

### Not a plain surface natural-language stream

At this representation level:

- line breaks behave as reset boundaries;
- lags 2–4 provide no held-out predictive benefit after local/positional information;
- a line-local model predicts better than a continuous language-like model.

### Not a simple line-local Markov/template generator either

The simple generator reproduces immediate class behavior but misses most of the manuscript's
distinctive structure, especially:

- productive vocabulary/novelty;
- copy/modify-like near-neighbor adjacency;
- the extreme line-final `m` realization;
- residual lag-2–5 structure.

Therefore the current evidence favors **a richer surface mechanism**.

Two broad explanations remain genuinely competitive:

1. a content-bearing natural-language stream transformed by a substantial, line-aware notation /
   generation layer;
2. a richer procedural generator with explicit copy-modify, positional realization, vocabulary
   innovation and possibly a latent line state.

A hybrid is also possible: meaningful content could constrain a line-aware generator.

## What this phase buys us

The question is no longer "which dictionary should be tried next?"

It is now possible to test concrete mechanism components without knowing the language.

The next experiment should be a preregistered **augmentation / ablation ladder**. Starting from the
failed simple generator, add exactly one independently observed mechanism at a time:

1. explicit line-final realization (`m`);
2. copy/modify near-neighbor generation;
3. productive novel-token generation;
4. one latent line-level state.

Each addition must be evaluated on the same held-out metrics that it was **not** directly fitted
to. If a small bounded set of rules reproduces the remaining Voynich signature, procedural
generation gains strong support. If even the enriched generator cannot reproduce transferable
residual structure without effectively memorizing the corpus, a hidden content-bearing source
becomes substantially more plausible.
