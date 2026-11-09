# Judge vs human agreement (AI-generated; review before use)

Items labelled: 149 of 150; skipped (missing/invalid label or unknown id): 1 ['Q150']

## QA verdict: gc (correct AND grounded)

| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |
|---|---:|---|---|---|---|
| EDC | 29 | 0.759 [0.586, 0.897] | 0.513 [0.199, 0.795] | 0.48 / 0.38 | 5 / 2 |
| L0 | 30 | 0.933 [0.833, 1.000] | 0.867 [0.664, 1.000] | 0.50 / 0.50 | 1 / 1 |
| Ours | 30 | 0.933 [0.833, 1.000] | 0.867 [0.667, 1.000] | 0.50 / 0.43 | 2 / 0 |
| U-ext+seed | 30 | 0.867 [0.733, 0.967] | 0.733 [0.467, 0.933] | 0.50 / 0.50 | 2 / 2 |
| iText2KG | 30 | 0.833 [0.667, 0.967] | 0.667 [0.348, 0.932] | 0.50 / 0.47 | 3 / 2 |
| ALL arms | 149 | 0.866 [0.812, 0.919] | 0.731 [0.617, 0.838] | 0.50 / 0.46 | 13 / 7 |

## QA verdict: correct

| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |
|---|---:|---|---|---|---|
| EDC | 29 | 0.897 [0.793, 1.000] | 0.754 [0.465, 1.000] | 0.76 / 0.66 | 3 / 0 |
| L0 | 30 | 0.900 [0.767, 1.000] | 0.769 [0.488, 1.000] | 0.67 / 0.70 | 1 / 2 |
| Ours | 30 | 0.933 [0.833, 1.000] | 0.814 [0.489, 1.000] | 0.77 / 0.77 | 1 / 1 |
| U-ext+seed | 30 | 0.833 [0.700, 0.967] | 0.634 [0.309, 0.902] | 0.67 / 0.63 | 3 / 2 |
| iText2KG | 30 | 0.900 [0.800, 1.000] | 0.780 [0.500, 1.000] | 0.67 / 0.63 | 2 / 1 |
| ALL arms | 149 | 0.893 [0.839, 0.940] | 0.749 [0.624, 0.861] | 0.70 / 0.68 | 10 / 6 |

## QA verdict: grounded

| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |
|---|---:|---|---|---|---|
| EDC | 29 | 0.862 [0.724, 0.966] | 0.721 [0.426, 0.931] | 0.55 / 0.55 | 2 / 2 |
| L0 | 30 | 0.933 [0.833, 1.000] | 0.864 [0.648, 1.000] | 0.57 / 0.57 | 1 / 1 |
| Ours | 30 | 0.933 [0.833, 1.000] | 0.865 [0.658, 1.000] | 0.60 / 0.53 | 2 / 0 |
| U-ext+seed | 30 | 0.867 [0.733, 0.967] | 0.730 [0.462, 0.933] | 0.53 / 0.60 | 1 / 3 |
| iText2KG | 30 | 0.867 [0.733, 0.967] | 0.722 [0.426, 0.933] | 0.60 / 0.60 | 2 / 2 |
| ALL arms | 149 | 0.893 [0.839, 0.940] | 0.781 [0.670, 0.879] | 0.57 / 0.57 | 8 / 8 |

## Fact precision (Gemma judge, pass 1) vs human 'supported'

skipped: 0

| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |
|---|---:|---|---|---|---|
| Ours | 20 | 0.900 [0.750, 1.000] | 0.800 [0.519, 1.000] | 0.50 / 0.60 | 0 / 2 |
| U-ext+seed | 20 | 0.800 [0.600, 0.950] | 0.600 [0.200, 0.900] | 0.50 / 0.50 | 2 / 2 |
| ALL arms | 40 | 0.850 [0.725, 0.950] | 0.700 [0.450, 0.899] | 0.50 / 0.55 | 2 / 4 |

Notes: sample is balanced on judge gc (QA) or judge verdict (facts); rates above are sample rates, not arm means.
Judge FP = judge says 1, human says 0; FN = judge says 0, human says 1.
