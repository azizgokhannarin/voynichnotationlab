# EVA `y` as a productive terminal marker / ending probe

Date: 2026-08-24

## Question

Does EVA `y` behave merely as a frequent final letter, or as a productive terminal /
morphological marker that can attach to many bases?

This matters because v1.5 showed that promoting `DY` as one latent unit *worsened* the
global short-token metric. A natural alternative is:

    ... d + Y

where `Y` remains a separable terminal element.

## 1. Positional baseline

| glyph   |   total_occurrences |   token_final_occurrences |   final_share_pct |
|:--------|--------------------:|--------------------------:|------------------:|
| n       |                6168 |                      6067 |            98.363 |
| m       |                1063 |                      1018 |            95.767 |
| y       |               17157 |                     14867 |            86.653 |
| r       |                7534 |                      5860 |            77.781 |
| l       |               10578 |                      5880 |            55.587 |
| s       |                2808 |                      1412 |            50.285 |
| d       |               10324 |                       717 |             6.945 |

EVA `y` is strongly terminal, but positional preference alone is insufficient.

## 2. Productivity against control final glyphs

For each candidate final glyph G, define every token `XG` and strip G to obtain base `X`.

We measure:

- number of distinct bases;
- whether bare `X` independently occurs;
- whether the same `X` appears with alternative final glyphs.

| suffix   |   token_occurrences |   surface_types |   distinct_bases |   independent_base_pct |   alt_ending_pct | top_alt_endings                                      |
|:---------|--------------------:|----------------:|-----------------:|-----------------------:|-----------------:|:-----------------------------------------------------|
| y        |               14657 |            3112 |             3112 |                 24.004 |           17.577 | s:227; o:210; d:197; l:159; r:152; e:87; g:62; m:58  |
| r        |                5664 |            1164 |             1164 |                 19.158 |           51.117 | l:405; m:202; s:158; y:152; n:145; d:104; o:53; g:49 |
| n        |                6062 |            1036 |             1036 |                  2.606 |           16.216 | r:145; m:57; l:57; s:30; y:16; g:16; d:8; i:7        |
| l        |                5724 |             942 |              942 |                 26.327 |           53.291 | r:405; m:179; y:159; s:147; d:105; n:57; o:50; g:47  |
| s        |                1084 |             510 |              510 |                 47.059 |           64.118 | y:227; r:158; l:147; d:138; o:86; m:66; e:40; g:36   |
| m        |                1005 |             400 |              400 |                 20     |           60.25  | r:202; l:179; s:66; y:58; n:57; d:45; g:34; o:22     |
| d        |                 664 |             343 |              343 |                 55.685 |           72.595 | y:197; s:138; l:105; r:104; o:86; m:45; e:43; g:27   |

A productive ending should attach to many distinct bases and participate in recurrent
alternation families rather than only a few frozen lexical forms.

## 3. Does `X` resemble `Xy` distributionally?

For pairs with both `X` and `Xy` occurring at least five times, compare predecessor and
successor context distributions.

| suffix   |   paired_types |   median_mean_cos |   mean_mean_cos |   median_succ_cos |   median_pred_cos |
|:---------|---------------:|------------------:|----------------:|------------------:|------------------:|
| m        |              8 |             0.32  |           0.309 |             0.278 |             0.321 |
| l        |             49 |             0.309 |           0.314 |             0.247 |             0.299 |
| y        |            102 |             0.299 |           0.304 |             0.277 |             0.302 |
| s        |             30 |             0.298 |           0.309 |             0.255 |             0.304 |
| n        |              2 |             0.292 |           0.292 |             0.335 |             0.25  |
| r        |             46 |             0.287 |           0.29  |             0.237 |             0.271 |
| d        |             19 |             0.265 |           0.284 |             0.263 |             0.275 |

For `y`:

- observed paired types: 102
- median X/Xy context cosine: **0.299**
- frequency-matched random-pair median: **0.251**
- random 95th percentile: **0.382**

This test asks whether stripping `y` often leaves something behaving like a related
lexical/morphological base.

## 4. Selected recurrent X / Xy alternations

| base   |   base_count | y_form   |   y_count | alternate_forms                                                                                              |
|:-------|-------------:|:---------|----------:|:-------------------------------------------------------------------------------------------------------------|
| che    |           22 | chey     |       510 | cheo:75; ches:44; ched:25; cher:10; chel:7; chee:7; chek:6; chep:4; chet:2; checkh:2; cheg:2; chef:1; chem:1 |
| qokee  |           15 | qokeey   |       366 | qokeed:27; qokeeo:19; qokees:9; qokeee:4; qokeer:2; qokeel:1; qokeeb:1                                       |
| she    |           41 | shey     |       344 | sheo:46; shed:22; shee:19; shes:12; shek:9; sher:4; shel:3; sheckh:2; shet:1; shecth:1; shem:1; shep:1       |
| ched   |           25 | chedy    |       341 | chedr:2; cheda:1; chedl:1                                                                                    |
| shed   |           22 | shedy    |       255 | shedch:1; sheds:1                                                                                            |
| qokeed |           27 | qokeedy  |       221 |                                                                                                              |
| d      |           53 | dy       |       204 | dl:24; do:15; dr:9; da:6; dch:2; ds:1; dd:1; dm:1; du:1                                                      |
| ch     |           10 | chy      |       197 | cho:77; chl:33; che:22; chs:18; chr:11; chd:6; chckh:6; chcth:4; cha:2; chk:2; cht:1; chm:1                  |
| okee   |            6 | okeey    |       197 | okees:18; okeeo:15; okeed:6; okeer:5; okeee:2; okeem:1; okeeg:1                                              |
| chee   |            7 | cheey    |       188 | chees:36; cheeo:16; cheed:6; cheeb:3; cheef:2; cheet:2; cheea:1; cheel:1; cheer:1; cheee:1; cheeg:1          |
| qoke   |            7 | qokey    |       186 | qokee:15; qokeo:10; qoked:10; qoker:4; qokel:2; qokes:1; qokeg:1                                             |
| qoked  |           10 | qokedy   |       175 |                                                                                                              |
| otee   |            9 | oteey    |       160 | otees:12; oteeo:11; oteed:6; oteee:3                                                                         |
| shee   |           19 | sheey    |       141 | shees:8; sheeo:7; sheed:5; sheek:4; sheet:3; sheel:2; sheer:1; sheep:1                                       |
| chckh  |            6 | chckhy   |       141 | chckhd:2; chckhs:1; chckho:1                                                                                 |
| qok    |           21 | qoky     |       137 | qokl:21; qokr:10; qoke:7; qoko:6; qokch:2; qokd:1; qokm:1                                                    |
| ote    |            5 | otey     |       123 | oteo:15; otee:9; oted:6; otes:5; otea:1; otel:1; oter:1                                                      |
| ot     |           16 | oty      |       114 | oto:10; otl:9; otr:7; ote:5; otch:4; ota:2; otsh:1                                                           |
| chd    |            6 | chdy     |       108 | chdo:1                                                                                                       |
| oke    |            4 | okey     |       106 | okeo:16; oked:7; okee:6; okel:4; okes:3; oker:2                                                              |
| ok     |           13 | oky      |       103 | oko:9; okr:8; okl:5; oke:4; oka:1; okch:1; oksh:1; okm:1                                                     |
| cth    |            8 | cthy     |       100 | ctho:10; cthr:2; cthe:2; cths:1; cthl:1; cthd:1                                                              |
| sh     |           27 | shy      |        94 | sho:118; she:41; shd:8; shs:4; shl:4; shr:3; sha:2; shckh:1; shcth:1; shx:1                                  |
| oted   |            6 | otedy    |        93 | otedr:1                                                                                                      |
| oteed  |            6 | oteedy   |        87 | oteedo:1                                                                                                     |

These examples are not translations. They show that `y` frequently participates in
surface families where a related base exists independently.

## 5. Line-final confound

For matched X/Xy pairs, the median change in line-final rate after adding `y` is:

    7.11 percentage points

Thus some of the terminal behaviour may reflect line/syntactic boundary position.
However, the morphological hypothesis requires more than line-final enrichment; it also
requires productive base alternation and context similarity.

## 6. Currier-state control

For X/Xy pairs with adequate counts, median absolute difference in Currier-A share is:

    8.33 percentage points

Large differences would suggest that many X/Xy relations are text-state-specific rather
than simple inflectional variants.

## Current interpretation

The evidence supports a **terminal-class role for `y`** much more strongly than the
specific claim that `DY` is an indivisible phonographic block.

The remaining alternatives are:

1. productive morphological ending;
2. phonographic final vowel/consonant;
3. clitic-like terminal sign;
4. scribal/line-boundary marker;
5. a mixture of linguistic and layout effects.

The important simplification is:

    treat final `y` as an explicit terminal feature first,
    not automatically as part of every preceding bigram.

## Consequence for latent inventory

Provisional update:

- `QO`: promoted block
- `DA`: promoted onset block
- `Y_final`: promoted **terminal feature**, not necessarily a merged unit
- `DY`: demoted as indivisible block
- `CH/SH`: unresolved linguistic atomicity
- gallows: atomic glyph + internal modifier features

## Next decisive test

Strip final `y` as a feature and rebuild stem families.

Then ask whether:

- the number of stem families decreases;
- `or/s/r` subject-like candidates share more stems;
- ending-agreement becomes more recurrent;
- line-position effects can be separated from grammatical effects.

If stripping terminal `y` produces cleaner families, the manuscript's apparent vocabulary
will shrink substantially.
