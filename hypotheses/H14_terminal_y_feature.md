# H14 — EVA `y` is a productive terminal feature

## Motivation

EVA `y` is overwhelmingly token-final. v1.5 ablation also showed that merging `d+y`
into one `DY` latent unit worsens the global short-token metric.

## Hypothesis

Final `y` should initially be modelled as a separable terminal feature:

    STEM + Y_final

rather than as part of every preceding bigram.

Possible linguistic realizations include:

- inflectional suffix;
- final phoneme/vowel;
- clitic or closure marker;
- modifier.

A line-management role remains a competing explanation.

## Falsification

The hypothesis weakens if stripping final `y` does not reduce stem-family complexity,
does not preserve contextual relatedness between X and Xy, or if the effect is explained
almost entirely by line geometry.

## Status

Supported as a terminal-class feature; exact linguistic meaning unresolved.
