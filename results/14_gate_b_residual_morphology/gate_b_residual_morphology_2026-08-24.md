# Gate B — Residual stem × terminal structure after removing the strongest layout effect

Date: 2026-08-24

## Goal

Gate A showed that terminal selection is partly layout/state-conditioned, especially EVA `m`
at physical line endings.

Gate B therefore asks:

> after excluding line-final tokens and conditioning the null model on Currier state and
> broad local context, does a non-random stem × terminal structure remain?

If yes, the terminal system cannot be reduced to line layout alone.

## Dataset

Only **non-line-final tokens** are used.

A stem is retained when it has:

- >=12 non-line-final occurrences;
- >=2 observed terminal variants;
- second-most-common terminal count >=2.

Result:

- eligible stems: **267**
- analysed occurrences: **21862**

## 1. Stem ↔ terminal dependence

Observed mutual information:

    I(STEM; TERMINAL) = 1.3724 bits

Conditional permutation null:

- terminal labels shuffled within `(Currier A/B, previous-role, next-role)` strata;
- stem identities left untouched;
- line-final tokens already removed.

Null:

- mean MI = 0.0644
- SD = 0.0021
- z = **619.38**
- empirical p = **0.001248**

Therefore substantial stem-specific terminal preference remains after the strongest known
layout effect and coarse text/context effects are controlled.

This is compatible with morphology or phonotactics; it is not by itself proof of inflection.

## 2. How structured are stem terminal profiles?

Weighted mean Jensen-Shannon divergence from the global terminal distribution:

- observed: **0.3297**
- conditional-null mean: **0.0128**
- z: **743.57**
- empirical p: **0.003322**

Thus stems are not simply sampling the global terminal inventory at fixed marginal rates.

## 3. Low-dimensional structure

SVD of normalized non-line-final terminal profiles:

|   components |   cumulative_variance |
|-------------:|----------------------:|
|            1 |                0.6118 |
|            2 |                0.8616 |
|            3 |                0.9425 |
|            4 |                0.9826 |
|            5 |                0.9979 |
|            6 |                1      |
|            7 |                1      |

A small number of profile dimensions explains a substantial fraction of variation, consistent
with a limited number of recurrent terminal-behaviour classes.

This can arise from:

- declension/conjugation classes;
- phonotactic final classes;
- lexical stem classes;
- residual notation classes.

The present test does not assign a grammatical label.

## 4. Transparent clustering

Best exploratory k-means solution among k=2..6:

- k = **3**
- silhouette = **0.692**

Cluster summaries:

|   cluster |   n_stems | profile                                                | top_stems                                                                                                                                                 |
|----------:|----------:|:-------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
|         0 |       115 | l:0.37; r:0.35; Ø:0.14; s:0.05; y:0.04; m:0.04; n:0.02 | o:1055; a:730; ch·o:716; d·a:422; sh·o:398; ch·e·o:361; q·o·k·a:327; s:317; o·t·a:285; o·k·a:267; q·o:224; sh·e·o:202                                     |
|         1 |        34 | n:0.76; r:0.16; l:0.02; m:0.02; Ø:0.01; s:0.01; y:0.01 | d·a·i·i:638; a·i·i:611; q·o·k·a·i:286; q·o·k·a·i·i:246; d·a·i:245; a·i:230; o·k·a·i·i:192; o·k·a·i:138; o·t·a·i·i:138; o·t·a·i:114; s·a·i·i:110; s·a·i:90 |
|         2 |       118 | y:0.77; Ø:0.11; s:0.05; l:0.03; r:0.02; m:0.01; n:0.01 | ch·e:557; sh·e:386; q·o·k·e·e:379; ch·e·d:338; sh·e·d:265; ch:247; q·o·k·e·e·d:244; ch·e·e:226; o·k·e·e:211; d:192; q·o·k·e:190; q·o·k·e·d:179            |

The clusters are useful as a compression of terminal behaviour, not as "declension classes"
until they predict independent syntactic or lexical properties.

## 5. Currier robustness

Residual stem-terminal MI calculated separately:

| Currier   |   occurrences |   MI_stem_terminal |
|:----------|--------------:|-------------------:|
| A         |          6177 |             1.2977 |
| B         |         14287 |             1.4419 |

The dependence exists within Currier strata rather than being created solely by mixing
Currier A and B.

## 6. Pronoun/agreement side test with line-final successors removed

| a   | b   |   shared_stems |   differential_stems |   median_TV | top_patterns           |
|:----|:----|---------------:|---------------------:|------------:|:-----------------------|
| or  | s   |             33 |                    3 |      0.269  | r->l:1; n->r:1; l->r:1 |
| or  | ar  |             41 |                    2 |      0.251  | r->l:1; l->r:1         |
| s   | ar  |             38 |                    2 |      0.2857 | r->n:1; r->l:1         |
| r   | ar  |             32 |                    2 |      0.3299 | r->l:1; l->r:1         |
| s   | r   |             27 |                    2 |      0.4168 | r->n:1; r->l:1         |
| or  | r   |             28 |                    0 |    nan      |                        |

The earlier `or/s/r` functional zone still shares many stems, but **clean recurrent person
agreement does not emerge** after the line-final control.

This is an important negative result.

It suggests that:

- `or/s/r` may still be a grammatical/function-word paradigm;
- but the current terminal inventory is not behaving like a simple person-ending system.

## Gate-B verdict

### Supported

1. Terminal variation is **not explained away by layout**.
2. After removing line-final tokens, stem identity still strongly predicts terminal choice.
3. Stem terminal profiles are more structured than a Currier/context-conditioned null.
4. A small number of recurring terminal-profile classes exists.

### Not established

1. These classes are not yet proven to be inflectional paradigms.
2. No stable person-agreement mapping has emerged.
3. The terminal system may still be primarily phonotactic rather than grammatical.

## Updated fork

The evidence now supports a mixed model:

    STEM + residual terminal class
         + layout/notational realization

The next discriminating question is no longer "is there terminal structure?" — there is.

The question is:

> does the residual terminal class correlate with **syntactic function** or mainly with
> **stem-internal/phonological shape**?

That becomes Gate B2.

### Gate B2

For each normalized stem, predict terminal choice from:

1. stem-final/core phonographic features;
2. surrounding functional-token class;
3. both together.

If stem-internal features dominate, interpret the terminal system primarily as phonographic /
phonotactic.

If independent syntactic-context information remains strong, morphology becomes substantially
more plausible.

### Gate C remains mandatory

Before historical-language brute force, independently validate whether visible Voynich spaces
behave like genuine linguistic boundaries.
