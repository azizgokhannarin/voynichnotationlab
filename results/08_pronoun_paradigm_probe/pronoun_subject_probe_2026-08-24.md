# Pronoun / explicit-subject distributional probe

Date: 2026-08-24

## Motivation

If the underlying language normally expresses personal subjects explicitly, frequent short
tokens may include a pronoun paradigm analogous to `I/you/he/she/we/they` or
`ich/du/er/sie/wir/sie`.

The test does **not** assume German or English spellings.

The central distributional prediction is:

> different personal pronouns should often occur in similar syntactic environments,
> especially before/around overlapping verb or predicate classes.

Therefore we search for short tokens with **similar predecessor and successor distributions**.

## Important language-family caveat

"European language" does not imply obligatory explicit subject pronouns.

- English and German are relatively non-pro-drop.
- Italian, Spanish and many historical Romance varieties can omit subjects.
- Latin is strongly compatible with null subjects.

Therefore absence of a clear pronoun paradigm would not imply non-European language.
It would instead weaken specifically non-pro-drop candidates or imply that our tokenisation /
sentence model is wrong.

Gender is also language-specific:

- English distinguishes `he/she` and object/possessive `her`;
- German distinguishes `er/sie/es`, but `sie` also has other grammatical uses;
- Romance languages encode gender in different pronoun/article systems.

## Corpus

- clean tokens: 37948
- short candidates tested (<=3 EVA glyphs, count >=30): 71

## Most frequent short candidates

| token   |   count |   glen |   line_initial_pct |   line_final_pct |   succ_types |   pred_types |
|:--------|--------:|-------:|-------------------:|-----------------:|-------------:|-------------:|
| ol      |     588 |      2 |              6.633 |            8.163 |          262 |          322 |
| chey    |     510 |      3 |              1.961 |            6.078 |          282 |          285 |
| ar      |     449 |      2 |              2.227 |            8.686 |          245 |          262 |
| or      |     390 |      2 |              7.692 |            4.103 |          196 |          239 |
| chol    |     367 |      3 |              5.177 |            1.635 |          220 |          232 |
| shey    |     344 |      3 |              2.616 |            5.233 |          221 |          228 |
| s       |     328 |      1 |              8.537 |           12.195 |          138 |          232 |
| al      |     311 |      2 |              0.965 |           13.505 |          191 |          172 |
| dar     |     287 |      3 |             12.892 |           14.983 |          167 |          190 |
| chor    |     215 |      3 |              6.512 |            2.791 |          146 |          151 |
| y       |     210 |      1 |             20     |           21.905 |          133 |          127 |
| dy      |     204 |      2 |              0.98  |           35.784 |          107 |          153 |
| chy     |     197 |      2 |              1.523 |           10.66  |          135 |          145 |
| r       |     196 |      1 |              4.082 |            8.163 |           95 |          138 |
| dal     |     190 |      3 |              2.105 |           23.158 |          113 |          145 |
| shol    |     176 |      3 |              9.091 |            2.273 |          135 |          120 |
| l       |     156 |      1 |              7.692 |            8.974 |           95 |          109 |
| ain     |     149 |      3 |              4.027 |           13.423 |          101 |           86 |
| qol     |     147 |      3 |             12.925 |            6.122 |           80 |           81 |
| chckhy  |     141 |      3 |              0.709 |            7.801 |          109 |           93 |

## Distributional-paradigm search

For each pair of short tokens we compare:

1. distribution of tokens one or two positions to the right;
2. immediate predecessor distribution;
3. Jensen-Shannon divergence;
4. cosine similarity.

A potential pronoun pair should have similar continuation distributions even when its
surface spelling is not trivially related.

### Strong non-trivial pairs

The following require edit distance >=2 to reduce simple suffix/prefix-family matches:

| a    | b     |   count_a |   count_b |   edit_distance |   successor_cosine |   predecessor_cosine |   successor_JSD |   combined_score |
|:-----|:------|----------:|----------:|----------------:|-------------------:|---------------------:|----------------:|-----------------:|
| or   | s     |       390 |       328 |               2 |              0.927 |                0.59  |           0.19  |            0.826 |
| chey | ol    |       510 |       588 |               4 |              0.734 |                0.806 |           0.214 |            0.756 |
| chor | cthol |       215 |        55 |               2 |              0.741 |                0.646 |           0.268 |            0.712 |
| cthy | cthol |       100 |        55 |               2 |              0.709 |                0.716 |           0.223 |            0.711 |
| y    | ol    |       210 |       588 |               2 |              0.746 |                0.618 |           0.228 |            0.707 |
| shey | ol    |       344 |       588 |               4 |              0.693 |                0.728 |           0.231 |            0.704 |
| ain  | al    |       149 |       311 |               2 |              0.703 |                0.701 |           0.245 |            0.702 |
| ar   | s     |       449 |       328 |               2 |              0.809 |                0.404 |           0.223 |            0.688 |
| ar   | ol    |       449 |       588 |               2 |              0.681 |                0.703 |           0.25  |            0.688 |
| r    | ol    |       196 |       588 |               2 |              0.778 |                0.472 |           0.24  |            0.686 |
| dar  | ol    |       287 |       588 |               3 |              0.726 |                0.592 |           0.25  |            0.686 |
| chol | cthy  |       367 |       100 |               3 |              0.739 |                0.557 |           0.257 |            0.684 |
| s    | ol    |       328 |       588 |               2 |              0.737 |                0.555 |           0.277 |            0.682 |
| chor | chy   |       215 |       197 |               2 |              0.668 |                0.712 |           0.303 |            0.681 |
| cthy | cthor |       100 |        45 |               2 |              0.66  |                0.727 |           0.255 |            0.68  |
| s    | sar   |       328 |        77 |               2 |              0.813 |                0.354 |           0.248 |            0.675 |
| ar   | ain   |       449 |       149 |               2 |              0.655 |                0.722 |           0.227 |            0.675 |
| or   | sar   |       390 |        77 |               2 |              0.821 |                0.331 |           0.258 |            0.674 |
| or   | cheo  |       390 |        75 |               4 |              0.731 |                0.539 |           0.327 |            0.673 |
| r    | lor   |       196 |        38 |               2 |              0.721 |                0.558 |           0.293 |            0.672 |

## Graph-like candidate families

Using a conservative exploratory threshold (successor cosine >=0.72 and predecessor
cosine >=0.45), the strongest connected short-token families are:

- ol, chey, ar, or, shey, s, al, dar, y, r, cheo, lor (total N=3726)
- chol, chor, chy, shol, cthy, cthol (total N=1110)
- o, d (total N=167)

These are **distributional paradigms**, not pronoun identifications.

## First interpretation

A genuine pronoun paradigm should satisfy several additional constraints:

- multiple members share the same likely predicate/verb continuations;
- members are broadly distributed across manuscript sections rather than tied to one
  illustration type;
- the family should not be explainable simply as graphical variants or suffix families;
- if the underlying language has grammatical gender, at least some members may divide
  contexts in ways compatible with animate/sex or noun-gender distinctions;
- if the language is non-pro-drop, candidate subject pronouns should occur often enough
  to account for a substantial fraction of clause-like units.

At this stage the corpus produces **several distributionally similar short-token pairs**,
but no unique `I/he/she` mapping.

## Stronger next tests

### 1. Predicate-class inference
Infer recurring "predicate-like" token classes from what follows candidate short tokens.
Pronouns should share these classes.

### 2. Person-paradigm test
Look for 3–6 short tokens with mutually similar continuation distributions but different
surface forms, analogous to a pronoun paradigm.

### 3. Gender/third-person probe
Only after a candidate paradigm exists, test whether two members behave almost identically
syntactically but differ systematically by local semantic/illustration context.

Illustrations must not be used to assign gender first; they are only a later external check.

### 4. Pro-drop discriminator
Estimate how many clause-like sequences can begin directly with a predicate-like class
without an overt short-token subject. This can distinguish a non-pro-drop-like grammar
from a pro-drop-like one.

## Current verdict

The user's "subject scan" is methodologically promising because it targets a **closed
grammatical paradigm** instead of individual word meanings.

It should be pursued as a distributional/syntactic test, not by searching directly for
strings resembling `ich`, `I`, `sie`, or `her`.
