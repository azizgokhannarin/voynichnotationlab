# Voynich Notation Lab

An open, falsification-first investigation of the Voynich Manuscript.

## Current conclusion — v6.0.0

This project does **not** claim a decipherment. After testing direct language mappings,
surface-language order, procedural generators, recurrence, residual capacity, latent states,
paragraph structure and paragraph-final punctuation, our leading working hypothesis is:

> **Voynichese is writing-as-image: a private, lossy visual mnemonic notation that imitates the
> appearance and motor rhythm of Western/Latin-script handwriting without preserving an ordinary,
> recoverable word-by-word language or classical cipher surface.**

The writer may have used recurring graphic families to recall internally known words, sounds,
phrases or concepts. Illustration, page location, paragraph geometry and memory may have supplied
information that was never written explicitly. The underlying mental language need not have been
Latin; the visible design may instead borrow the visual habits of Latin-script manuscript culture.

This model is human-executable in the fifteenth century. It requires no machine-scale cipher,
large hidden key or modern algorithm: practiced motor chunks, visual analogy, abbreviation,
local copy/modify behaviour and contextual memory are sufficient.

## What “writing-as-image” means

The hypothesis is **not** that the marks are independent random doodles. The surface has stable
graphic and layout organisation. It is also **not** a claim that the manuscript contains a
recoverable plaintext under a normal substitution alphabet.

| Ordinary writing/cipher | Writing-as-image hypothesis |
|---|---|
| Surface units preserve recoverable letters, words or codes | Surface units may be mixed visual reminders |
| One mapping is expected to transfer across pages | Reading may depend on image, topic, position and memory |
| Punctuation or grammar marks boundaries | Layout and decorated starts may supply boundaries |
| Similar words follow linguistic morphology or formulas | Similar forms may also follow visual analogy and motor memory |
| A reader with the key can reconstruct plaintext | The writer may have been the only fully equipped reader |

A plausible but unproven production narrative is that the manuscript began as private notes and
later acquired a more book-like presentation because the writer believed another suitably minded
reader could understand it. This is an interpretation, not evidence about the writer's identity,
diagnosis, speech or mental health.

## How the project reached this hypothesis

| Stage | What we asked | What happened | Licensed conclusion |
|---|---|---|---|
| Early structural work | Are there stable glyph blocks and positional families? | `qo`, gallows families, terminal families and visible boundaries showed repeatable structure. | The surface is organised, not independent randomness. |
| Phonetic anchors | Can pictures or familiar-looking strings provide direct words? | Candidate readings such as `daral = wine` failed counterexamples and boundary checks. | Visual resemblance is not a translation anchor. |
| Terminal decomposition | Do raw word endings behave like ordinary morphology? | `{n,m,y,r,l,s,Ø}` exposed reusable stems, but ending choice was strongly affected by layout and manuscript state. | The terminal system is mixed graphic/structural, not a clean grammatical paradigm. |
| Phase 13 | Does a bounded phonographic key recover German, Italian, French or Latin? | Language-model fit appeared, but held-out phrase order did not. Positive controls recovered their languages strongly. | Fixed units + fixed visible boundaries + bounded homophony are unsupported. This does not prove absence of hidden content. |
| Phase 14 | Is a simple line-reset procedural generator sufficient? | It reproduced only 4 of 18 held-out metrics and failed vocabulary, near-neighbour and line-final behaviour. | A simple first-order generator is insufficient. |
| Phase 15 | Do line-locality and short-range order distinguish language from generation? | Strongly rendered known Latin and real abbreviated medieval Latin reproduced the same broad signature. Legacy class-MI could not be reproduced. | These measurements describe the surface but do not identify content type; legacy class-MI was retired. |
| Phase 16 | Where does exact-token recurrence live? | Tokens were strongly allocated to pages and physical lines, but reliable within-line identity order disappeared after fixing each line's inventory. | Allocation is real; ordinary long-range word order was not recovered. |
| Phase 17 | Could structured non-language data look similar? | An unordered transaction/tally control reproduced the qualitative allocation-without-order phenotype at different magnitudes. | The phenotype cannot identify language, records or generation. |
| Phase 18 | Is residual information capacity too low for hidden content? | A weak unigram/open-vocabulary model left a large one-sided upper bound with high escape rate. | Content-rich hidden material was not rejected, but the bound is not evidence for it. |
| Phase 19 | Is there a transferable binary line state? | Raw gain was tiny; bootstrap and prequential/MDL gates failed. | The frozen binary line-state subclass is unsupported. |
| Phase 20–21 | Was the internal statistical program still identifiable? | Reused Validation became development data; broad H_C/H_D/H_G classes could imitate one another; the generator ladder was cancelled. | Unbounded surface-model expansion was stopped; final-test remained sealed. |
| Phase 22 | Are visible paragraphs real and how are they opened? | Direct gallows began 83.1% of transcriber paragraphs versus 8.6% of other lines; IT2a replicated 81.2% versus 8.5%. Stars and visual paragraphs were not identical layers. | Paragraph openings are strongly designed; marginal stars may mark items/subentries. |
| Phase 23 | Is there a mandatory paragraph-final point hidden in terminal variants? | Real leave-one-page-out AUC was 0.524/0.556; permutation gates failed. An injected allomorph was recovered at about 0.999 AUC. | No single EVA terminal or bounded ending-conditioned mapping is a universal point. Paragraph closure is probably layout/start-marked. |
| Perceptual distance check | Does the page retain Western-handwriting appearance when zoomed out? | Normal pages strongly looked like writing; mirrored pages retained much of the word texture but lost normal initial/reading-direction rhythm. No stable Latin words emerged. | The manuscript convincingly reproduces writing texture; this identifies a visual tradition, not a language. |

## What worked, what failed, and what remains open

### Durable observations

- The script is fluent and graphically practiced.
- Visible word-like spacing is statistically meaningful as a surface boundary.
- Token selection is page- and line-sensitive.
- Near-neighbour visual/token families and productive variation are real surface features.
- Tall/direct gallows have a strong paragraph-initial role.
- EVA `m` is strongly physical-line-final but is not paragraph punctuation.
- Paragraph-final `n`, then `y/r`, are descriptively enriched but do not form a mandatory stop.
- Quire-20 stars may mark entries smaller than a visual paragraph.

### Closed or retired bounded explanations

- simple one-to-one or bounded-homophonic direct language mapping under frozen units/boundaries;
- a simple first-order line-reset generator;
- the frozen binary line-state model;
- a universal point represented by one EVA terminal or a small preceding-ending-to-terminal table;
- legacy class-MI as active evidence.

### Not established

- the underlying mental/spoken language;
- any phonetic value for an EVA glyph;
- a recoverable plaintext;
- a conventional encryption key;
- author identity, number of writers, diagnosis, motive or intended audience;
- whether the visual notation recalled meaningful content or produced only structured pseudo-writing.

## Final hypothesis: H20

The complete hypothesis and falsifiers are recorded in
[`hypotheses/H20_writing_as_image_visual_mnemonic_notation.md`](hypotheses/H20_writing_as_image_visual_mnemonic_notation.md).

Its most important discriminator is no longer another language model. It is the competition
between two visual mechanisms:

1. **Meaningful mnemonic notation:** visual families recur across distant pages when the same
   illustration motif, topic or source concept recurs.
2. **Structured pseudo-writing:** visual families are explained primarily by immediately preceding
   forms, motor memory and available line width.

The external test protocol is documented in
[`docs/EXTERNAL_VISUAL_MNEMONIC_TEST_PROTOCOL.md`](docs/EXTERNAL_VISUAL_MNEMONIC_TEST_PROTOCOL.md).

## Evidence discipline

1. Separate observation, interpretation, hypothesis, result and conclusion.
2. Preserve negative results and counterexamples.
3. Do not assign sounds from visual resemblance.
4. Do not diagnose or invent a biography for the writer.
5. Treat transcription decisions and proposed scribal hands as confounds.
6. Keep Validation history explicit and final-test pages sealed.
7. Do not call a visually compelling hypothesis a decipherment.

## Repository map

- `hypotheses/` — falsifiable mechanism hypotheses;
- `observations/` — claim-limited surface observations;
- `results/` — early structural experiments;
- `phase13_*` through `phase23_*` — calibrated language, generation, audit, paragraph and punctuation tests;
- `phase24_final_synthesis/` — v6.0.0 decision and claim ledger;
- `docs/` — external test protocol, final Turkish synthesis and LinkedIn draft.

## Current status

`FINAL_LEADING_HYPOTHESIS_FROZEN; EXTERNAL_VISUAL_VALIDATION_INVITED`

No additional language brute force, unrestricted generator search or post-hoc surface metric is
authorised. Future work must make a preregistered visual prediction that distinguishes meaningful
mnemonic notation from structured pseudo-writing.
