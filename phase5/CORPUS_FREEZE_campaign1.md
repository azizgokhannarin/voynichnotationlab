# Campaign 1 — Frozen Historical Corpus Registry

Date frozen: 2026-08-25

Status: **FROZEN BEFORE ANY LANGUAGE-MAPPING SEARCH**

This registry converts the family-level preregistration into concrete historical resources.

No corpus may be replaced because another corpus yields a better Voynich score. If a frozen
resource later proves technically unusable, Campaign 1 must record the failure and use only
the explicitly predeclared fallback.

---

# 1. Selection principles

A corpus is preferred when it is:

1. historically close to 1300–1500 CE;
2. large enough for phonotactic modeling;
3. based on scholarly transcription rather than OCR-only text;
4. versioned or otherwise reproducibly identifiable;
5. available in structured text form;
6. broad enough not to reduce a language family to a single attractive author.

Corpus text is never selected because it contains words that resemble Voynich tokens.

---

# 2. West Germanic

## WG-P1 — ReF: Referenzkorpus Frühneuhochdeutsch

Frozen resource:
- Referenzkorpus Frühneuhochdeutsch (ReF), Version 1.0
- full corpus span: 1350–1650
- Campaign-1 subset: texts dated from 1350 through 1500 inclusive
- preferred representation: annotated normalized word layer where available
- diplomatic layer retained only for robustness

The resource is downloadable in CorA-XML / TIGER-XML and is licensed CC BY-SA 4.0.

Primary role:
- High German branch of West Germanic.

## WG-P2 — ReN: Reference Corpus Middle Low German / Low Rhenish

Frozen resource:
- ReN Version 1.1 (2021)
- full corpus span: 1200–1650
- Campaign-1 subset: 14th- and 15th-century texts only
- preferred representation: annotated/normalized token layer
- TEI / CorA-XML source is preferred for reproducibility

Primary role:
- Low German / Low Rhenish branch of West Germanic.

## West-Germanic family score

The family score is the **unweighted mean of the two null-standardized held-out scores**
for WG-P1 and WG-P2.

A West-Germanic advance is not allowed if one branch is strongly negative and the other alone
creates the family win.

This prevents post-hoc dialect cherry-picking.

---

# 3. Romance

## RO-P1 — Base de français médiéval (BFM2022)

Frozen resource:
- BFM2022
- Campaign-1 subset: texts whose composition/manuscript dating intersects 1300–1500
- TEI XML distribution
- open Etalab license
- wordforms are primary; lemma/POS annotation is not used to create phonetic matches

Primary role:
- Medieval French branch.

## RO-P2 — DanteSearch vernacular corpus

Frozen resource:
- DanteSearch downloadable TEI XML
- vernacular works only
- primary material overlapping the Campaign-1 period, especially the Comedy
  (approximately 1306–1321)
- Latin works by Dante are excluded from the Romance branch

Primary role:
- Old Italian / Florentine branch.

Dante is a single-author corpus, so it cannot alone cause Romance to advance.

## Romance family score

The family score is the **unweighted mean of the null-standardized BFM and DanteSearch
held-out scores**.

Both branch scores are always reported.

This deliberately makes a Romance win harder than selecting whichever Romance variety happens
to resemble the Voynich representation best.

---

# 4. West Slavic

## WS-P1 — Staročeská textová banka (Old Czech Text Bank)

Frozen resource:
- Staročeská textová banka / Vokabulář webový
- frozen data version for acquisition: **1.1.27**
- historical coverage: 13th–15th centuries
- Campaign-1 subset: texts dated 1300–1500
- the bank is used through its transcribed historical-Czech layer
- foreign-language passages must be excluded where metadata permits

The bank uses transcriptions into modern Czech orthographic conventions. This is useful for
a conservative grapheme-to-phonographic-class normalizer but must not be mistaken for exact
15th-century pronunciation.

### Reproducibility requirement

Before Campaign 1 search begins, the selected export/query result must be saved locally and
SHA-256 hashed. The hash becomes part of the frozen corpus manifest.

If bulk export is technically unavailable, the Campaign-1 West-Slavic branch is marked
**DATA-ACQUISITION BLOCKED** rather than silently replaced by modern Czech.

## WS-R1 — Old Polish up to 1500

The Corpus of Polish up to 1500 is recognized as a relevant robustness resource, but it is
**not a primary Campaign-1 corpus** unless a stable export/version can be frozen before any
Voynich-language score is inspected.

Thus Old Czech is the sole preregistered primary West-Slavic representative for Campaign 1.

---

# 5. Latin

## LA-P1 — LatinISE

Frozen resource:
- LatinISE historical Latin corpus
- distribution identified through the CLARIN/LINDAT resource
- metadata includes century/date, genre, title and author
- Campaign-1 subset: texts dated 1300–1500 inclusive where metadata allows
- surface wordforms, not lemmas, are used for phonographic modeling

Primary role:
- medieval/late-medieval Latin baseline.

## LA-R1 — Corpus Corporum

Corpus Corporum is frozen as an **external robustness resource**, not a development corpus.

Rules:
- only texts with explicit dates between 1300 and 1500 may be selected;
- a text-ID manifest must be frozen before its score is evaluated;
- TEI XML / text downloads may be used for non-commercial research where permitted;
- Corpus Corporum results cannot be used to retune LA-P1 normalization.

This avoids leakage from an actively growing meta-corpus.

---

# 6. Corpus balance rules

For each primary corpus/subcorpus:

1. remove editorial apparatus where identifiable;
2. remove non-target-language passages where tagged;
3. retain ordinary token boundaries from the edition;
4. do not lemmatize the phonotactic stream;
5. do not deduplicate recurring words;
6. cap any single work/author at 25% of the training tokens where the resource is multi-author;
7. retain at least 100,000 usable word tokens where the source permits.

If a source cannot meet the token threshold, it remains reportable but is marked LOW-DATA.

---

# 7. Family-level comparison rule

Primary family scores are computed only from the frozen primary resources:

- West Germanic = mean(WG-P1, WG-P2)
- Romance = mean(RO-P1, RO-P2)
- West Slavic = WS-P1
- Latin = LA-P1

Every component score is first expressed as a **null-standardized held-out improvement**
relative to that corpus's own matched null distribution.

Raw cross-entropies from different languages are not directly averaged because the native
phoneme inventories and entropy rates differ.

---

# 8. No corpus shopping

Forbidden after mapping search starts:

- adding Swiss German because German underperforms;
- switching French to Occitan because Romance underperforms;
- replacing Old Czech with modern Czech;
- adding a favorable author;
- removing a difficult genre because it hurts the score;
- changing the date window for one family only.

Such changes require Campaign 2 preregistration.

---

# 9. Acquisition checkpoint

Before the search engine may run, create:

`phase5/corpora/CORPUS_MANIFEST_SHA256.csv`

with:
- corpus ID;
- source/version;
- local file(s);
- date filter;
- token count;
- SHA-256;
- license/access note.

Until this manifest exists, Phase 5 remains in PREPARATION state.
