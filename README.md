# Voynich Notation Lab

An open, hypothesis-driven research project on the Voynich Manuscript.

## Purpose

This repository does **not** claim that the Voynich Manuscript has been deciphered. Its purpose is to document observations, formulate falsifiable hypotheses, design reproducible experiments, preserve negative results, and make the reasoning process auditable.

The current working direction explores whether Voynichese may be a **personal visual/phonographic notation system** rather than a conventional cipher or ordinary alphabetic script.

## Core research principles

1. Separate **observation**, **interpretation**, and **conclusion**.
2. Every important hypothesis should have a stated falsification criterion.
3. Do not assign phonetic values to glyphs prematurely.
4. Treat page order and production chronology as different variables until demonstrated otherwise.
5. Compare visual context, glyph position, recurrence, transitions, and chronology jointly.
6. Preserve failed experiments and alternative explanations.
7. Avoid claims about identity, gender, relationships, mental state, or motive unless supported by manuscript evidence.

## Initial research tracks

### 1. First two pages
Analyze f1r and f1v as a possible calibration / system-formation region.

### 2. Repeated persona / voice motifs
Search for glyph or token motifs disproportionately associated with recurring human-figure contexts, especially the female-figure sections.

### 3. Glyph and block segmentation
Test whether single glyphs or recurring multi-glyph blocks behave more like phonemes, syllables, prosodic markers, or structural operators.

### 4. Conditional frequency analysis
Measure frequency by token position, line position, page context, manuscript region, and neighboring glyphs—not only globally.

### 5. Notation evolution
Track the first appearance and later handwriting of glyphs/blocks to test whether the notation system appears to develop during manuscript production.

## Working hypotheses

See [`hypotheses/`](hypotheses/).

## Experiments

See [`experiments/`](experiments/).

## Research status

**v4.8.0 — calibrated small latent-state checkpoint.**

Direct language search is closed only for the frozen-unit, fixed-boundary, bounded-homophonic
model class. H_C (hidden linguistic content), H_D (structured non-linguistic content) and H_G
(autonomous procedural generation) remain open and deliberately unranked.

A binary line-state HMM was frozen before results and calibrated against 100 parameter-matched
zero-state procedural nulls plus a known injected-state positive control. The positive control
was recovered with 0.577 bits/token held-out gain, 0.549 bits/token prequential gain and 99.0%
state accuracy; all calibration gates passed. On Voynich VALIDATION the raw held-out gain was only
0.0043 bits/token, its page-bootstrap interval crossed zero, and TRAIN-only prequential/MDL gain
was -0.0602 bits/token. The frozen three-condition rule therefore detects no robust transferable
binary line state. This bounded negative result does not rank H_C, H_D or H_G, and all final-test
pages remain sealed. No decipherment claim is made.
