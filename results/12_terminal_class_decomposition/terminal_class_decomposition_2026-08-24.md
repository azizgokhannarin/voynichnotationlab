# Terminal-class decomposition

Date: 2026-08-24

## Hypothesis

A large fraction of Voynich surface vocabulary may factor as:

    STEM + TERMINAL

with a recurring terminal class.

First-pass terminal set:

    {n, m, y, r, l, s}

This set is motivated by token-final positional bias and recurrent rime/ending families.
It is not assigned grammatical meanings.

## 1. Vocabulary collapse

Clean RF1b-EVA surface vocabulary:

- distinct surface token types: 8315
- distinct stems after one-terminal decomposition: 6412
- type collapse: **22.89%**
- surface types actually decomposed: 7164
- token occurrences carrying one of the terminal glyphs: 34196

The collapse is real but not, by itself, proof of morphology: any aggressive suffix stripping
will collapse vocabulary.

A deliberately non-terminal six-glyph control `{o,d,e,k,t,a}` leaves 7962 stems and
creates 246 multi-form stem groups. Therefore the important evidence is not raw
collapse alone, but whether terminal stripping creates **productive and contextually coherent
alternation families**.

## 2. Productive stem families

Under the terminal set:

- stems with >=2 observed endings and >=5 occurrences: **652**
- stems with >=3 endings: **357**
- stems with >=4 endings: **187**

Largest/highest-diversity examples:

| stem   |   total |   ending_types | endings                                    |
|:-------|--------:|---------------:|:-------------------------------------------|
| o      |    1152 |              7 | l:588; r:390; Ø:114; s:27; m:20; y:12; n:1 |
| a      |     898 |              7 | r:449; l:311; m:115; n:9; Ø:7; s:5; y:2    |
| cho    |     740 |              7 | l:367; r:215; Ø:77; s:42; y:23; m:15; n:1  |
| sho    |     406 |              7 | l:176; Ø:118; r:91; s:12; y:4; m:4; n:1    |
| oka    |     309 |              7 | l:147; r:130; m:23; n:5; s:2; Ø:1; y:1     |
| sa     |     144 |              7 | r:77; l:48; m:13; Ø:2; n:2; y:1; s:1       |
| che    |     594 |              6 | y:510; s:44; Ø:22; r:10; l:7; m:1          |
| da     |     562 |              6 | r:287; l:190; m:59; n:17; Ø:6; s:3         |
| she    |     405 |              6 | y:344; Ø:41; s:12; r:4; l:3; m:1           |
| cheo   |     377 |              6 | l:160; r:86; Ø:75; s:36; y:12; m:8         |
| qoka   |     366 |              6 | l:183; r:146; m:24; n:8; s:3; y:2          |
| ota    |     334 |              6 | r:150; l:132; m:44; n:3; s:3; Ø:2          |
| d      |     292 |              6 | y:204; Ø:53; l:24; r:9; s:1; m:1           |
| ch     |     270 |              6 | y:197; l:33; s:18; r:11; Ø:10; m:1         |
| ai     |     261 |              6 | n:149; r:95; m:9; l:5; y:2; s:1            |
| sheo   |     208 |              6 | l:94; Ø:46; r:42; s:14; y:8; m:4           |
| l      |     202 |              6 | Ø:156; y:17; s:16; r:10; l:2; m:1          |
| cha    |     176 |              6 | r:79; l:59; m:24; n:10; Ø:2; s:2           |
| oto    |     147 |              6 | l:82; r:35; y:14; Ø:10; s:5; m:1           |
| qota   |     145 |              6 | r:64; l:64; m:12; n:2; s:2; y:1            |
| qoko   |     138 |              6 | l:98; r:29; Ø:6; m:2; y:2; s:1             |
| oko    |     128 |              6 | l:72; r:29; Ø:9; s:8; y:6; m:4             |
| otai   |     125 |              6 | n:95; r:25; m:2; Ø:1; l:1; s:1             |
| so     |     124 |              6 | l:63; r:43; Ø:7; s:7; y:3; m:1             |
| okeo   |     123 |              6 | l:62; r:18; Ø:16; y:12; s:11; m:4          |

These families are the main payoff of the decomposition. They turn many surface words into
recurrent stem + ending paradigms.

## 3. Context preservation

For bare-base / suffixed-variant pairs with both sides occurring >=5 times, median combined
predecessor+successor cosine is:

    **0.300**

Context preservation is not extremely high. Thus many stem-sharing surface forms may have
different grammatical roles; simple inflection is only one explanation.

## 4. Subject-candidate stem overlap

After terminal stripping, compare which stems follow the strongest short functional candidates:

- `or / s`: **0.943**
- `or / r`: **0.921**
- `s / r`: **0.931**
- `ar / or`: **0.862**

The `or/s/r` functional zone remains strong under the decomposition.

## 5. Direct ending-agreement probe

For the same stripped stem, require >=5 observations after each subject candidate and compare
the terminal distributions.

| a   | b   |   differential_stems |   median_TV | top_ending_contrast_patterns   |
|:----|:----|---------------------:|------------:|:-------------------------------|
| or  | s   |                    2 |       0.254 | r->l:1; n->r:1                 |
| s   | r   |                    1 |       0.517 | r->n:1                         |
| s   | ar  |                    1 |       0.176 | r->n:1                         |
| or  | r   |                    0 |     nan     |                                |
| or  | ar  |                    0 |     nan     |                                |
| r   | ar  |                    0 |     nan     |                                |

A genuine person-agreement system should eventually show *repeated compatible ending
contrasts*, not merely many different preferred endings.

The current data contains repeated subject × ending dependencies, but the contrast patterns
are not yet clean enough to call a person paradigm.

## 6. Terminal-set ablation

Each candidate terminal was removed in turn:

| model   | terminal_set   |   stem_types |   type_collapse_pct |   multi_ending_stems |   stems_3plus_endings |   median_base_variant_context_cos |   or_s_stem_cos |   or_r_stem_cos |   s_r_stem_cos |
|:--------|:---------------|-------------:|--------------------:|---------------------:|----------------------:|----------------------------------:|----------------:|----------------:|---------------:|
| FULL    | lmnrsy         |         6412 |              22.886 |                  652 |                   357 |                             0.3   |           0.943 |           0.921 |          0.931 |
| DROP_l  | mnrsy          |         6775 |              18.521 |                  643 |                   269 |                             0.298 |           0.941 |           0.931 |          0.936 |
| DROP_m  | lnrsy          |         6646 |              20.072 |                  637 |                   295 |                             0.3   |           0.943 |           0.921 |          0.927 |
| DROP_n  | lmrsy          |         6559 |              21.118 |                  611 |                   333 |                             0.303 |           0.94  |           0.901 |          0.896 |
| DROP_r  | lmnsy          |         6928 |              16.681 |                  590 |                   236 |                             0.3   |           0.927 |           0.893 |          0.901 |
| DROP_s  | lmnry          |         6693 |              19.507 |                  606 |                   297 |                             0.295 |           0.942 |           0.925 |          0.933 |
| DROP_y  | lmnrs          |         6984 |              16.007 |                  412 |                   272 |                             0.292 |           0.943 |           0.916 |          0.925 |
| Y_ONLY  | y              |         7581 |               8.827 |                  484 |                     0 |                             0.299 |           0.924 |           0.904 |          0.901 |
| NMYR    | mnry           |         7068 |              14.997 |                  599 |                   169 |                             0.298 |           0.941 |           0.933 |          0.937 |
| NONE    | none           |         8315 |               0     |                    0 |                     0 |                           nan     |           0.921 |           0.9   |          0.898 |

Interpretation:

- a useful terminal should contribute to productive multi-ending families;
- it should not destroy contextual coherence;
- grammatical signals should remain stable or strengthen.

The terminal class should therefore be treated as a **feature inventory**, not a single suffix.

## Current conclusion

### Supported

1. Voynich has a large, highly reusable token-final repertoire.
2. Stripping one member of `{n,m,y,r,l,s}` exposes many recurrent multi-ending stem families.
3. The `or/s/r` functional-paradigm signal survives this new representation.
4. `DY` should remain split as `d + y_final`, not promoted again as one unit.

### Not established

1. The terminal class is not proven to be inflectional morphology.
2. No final glyph has yet been identified as person, case, gender or tense.
3. `or/s/r` is not yet identified as a pronoun paradigm.

## Strategic consequence

The search space can now be represented at three levels:

    onset/block features
        QO, DA, gallows...

    recurrent stems
        exposed by terminal stripping

    terminal features
        n / m / y / r / l / s / Ø

This is substantially more constrained than treating every surface token as an unrelated word.

## Next decisive step

Construct a **stem × terminal matrix** and ask whether terminal choices cluster by the
surrounding functional class.

In particular:

    or -> STEM -> ending
    s  -> STEM -> ending
    r  -> STEM -> ending

If the same ending contrasts recur across many stems, test them against historical
person/number/case paradigms. If not, reinterpret the terminal class as phonographic or
structural rather than inflectional.


## 7. Minimum-stem-length robustness control

The raw collapse is partly inflated by one-glyph stems such as `a -> ar/al/am/...` and
`o -> or/ol/...`. The analysis was therefore repeated while requiring the stripped stem
to contain at least 2, 3, or 4 EVA glyphs.

|   min_stem_len |   stem_types |   collapse_pct |   multi_stems |   threeplus |   fourplus |   multi_occ | model    |
|---------------:|-------------:|---------------:|--------------:|------------:|-----------:|------------:|:---------|
|              1 |         6412 |         22.886 |           652 |         357 |        187 |       28633 | terminal |
|              1 |         7962 |          4.245 |           164 |          63 |         24 |       10109 | control  |
|              2 |         6456 |         22.357 |           647 |         343 |        177 |       26950 | terminal |
|              2 |         7979 |          4.041 |           163 |          53 |         20 |        8956 | control  |
|              3 |         6638 |         20.168 |           606 |         297 |        144 |       22633 | terminal |
|              3 |         8032 |          3.403 |           140 |          36 |         14 |        6190 | control  |
|              4 |         7062 |         15.069 |           461 |         192 |         82 |       14676 | terminal |
|              4 |         8140 |          2.105 |            84 |          16 |          6 |        3443 | control  |

Terminal-family contribution at minimum stem length 2:

| glyph   |   productive_stems_full |   after_drop |   families_lost |   families_gained |
|:--------|------------------------:|-------------:|----------------:|------------------:|
| y       |                    1149 |          774 |             405 |                30 |
| r       |                    1149 |          957 |             271 |                79 |
| l       |                    1149 |         1069 |             198 |               118 |
| s       |                    1149 |         1066 |             118 |                35 |
| n       |                    1149 |         1070 |              97 |                18 |
| m       |                    1149 |         1095 |              59 |                 5 |

The terminal set continues to generate substantially more recurrent multi-ending families
than the six-glyph non-terminal control after short stems are excluded. Therefore the
effect is not driven only by `a` and `o` one-glyph families.

This strengthens the structural terminal-class result, while still not proving grammatical
inflection.
