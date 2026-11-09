# Judge vs human agreement, v2 (AI-generated; review before use)

QA items labelled: 150 of 150 (skipped for QA measures: 0 []). Predicate pairs used: 79; not used (NA on either side or missing): 71. Human predicate values present while human_grounded = 0: 0. Grounded = 1 but predicate blank: 0.

## QA verdict: gc (correct AND grounded)

| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |
|---|---:|---|---|---|---|
| EDC | 30 | 0.933 [0.833, 1.000] | 0.867 [0.667, 1.000] | 0.50 / 0.57 | 0 / 2 |
| L0 | 30 | 0.800 [0.667, 0.933] | 0.600 [0.310, 0.864] | 0.50 / 0.37 | 5 / 1 |
| Ours | 30 | 0.833 [0.700, 0.967] | 0.667 [0.372, 0.930] | 0.50 / 0.53 | 2 / 3 |
| U-ext+seed | 30 | 0.933 [0.833, 1.000] | 0.867 [0.667, 1.000] | 0.50 / 0.43 | 2 / 0 |
| iText2KG | 30 | 0.900 [0.767, 1.000] | 0.800 [0.541, 1.000] | 0.50 / 0.47 | 2 / 1 |
| ALL arms | 150 | 0.880 [0.827, 0.927] | 0.760 [0.653, 0.853] | 0.50 / 0.47 | 11 / 7 |

## QA verdict: correct

| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |
|---|---:|---|---|---|---|
| EDC | 30 | 0.967 [0.900, 1.000] | 0.902 [0.634, 1.000] | 0.77 / 0.80 | 0 / 1 |
| L0 | 30 | 0.733 [0.567, 0.900] | 0.400 [0.027, 0.729] | 0.67 / 0.67 | 4 / 4 |
| Ours | 30 | 0.900 [0.767, 1.000] | 0.734 [0.379, 1.000] | 0.77 / 0.73 | 2 / 1 |
| U-ext+seed | 30 | 0.833 [0.700, 0.967] | 0.615 [0.262, 0.902] | 0.67 / 0.70 | 2 / 3 |
| iText2KG | 30 | 0.800 [0.633, 0.933] | 0.550 [0.195, 0.851] | 0.67 / 0.67 | 3 / 3 |
| ALL arms | 150 | 0.847 [0.787, 0.900] | 0.628 [0.481, 0.761] | 0.71 / 0.71 | 11 / 12 |

## QA verdict: grounded

| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |
|---|---:|---|---|---|---|
| EDC | 30 | 0.933 [0.833, 1.000] | 0.862 [0.645, 1.000] | 0.57 / 0.63 | 0 / 2 |
| L0 | 30 | 0.800 [0.633, 0.933] | 0.600 [0.286, 0.865] | 0.57 / 0.50 | 4 / 2 |
| Ours | 30 | 0.867 [0.733, 0.967] | 0.714 [0.426, 0.932] | 0.60 / 0.67 | 1 / 3 |
| U-ext+seed | 30 | 0.967 [0.900, 1.000] | 0.933 [0.791, 1.000] | 0.53 / 0.50 | 1 / 0 |
| iText2KG | 30 | 0.900 [0.800, 1.000] | 0.789 [0.526, 1.000] | 0.60 / 0.63 | 1 / 2 |
| ALL arms | 150 | 0.893 [0.840, 0.940] | 0.781 [0.673, 0.877] | 0.57 / 0.59 | 7 / 9 |

## Predicate fit: human_predicate_ok vs code (gc_pred-style predicate check)

| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |
|---|---:|---|---|---|---|
| EDC | 17 | 0.882 [0.706, 1.000] | 0.000 [0.000, 0.000] (kappa CI from 88% of resamples) | 1.00 / 0.88 | 2 / 0 |
| L0 | 13 | 0.769 [0.538, 1.000] | 0.316 [0.000, 0.831] | 0.92 / 0.69 | 3 / 0 |
| Ours | 17 | 0.941 [0.824, 1.000] | 0.000 [0.000, 0.000] (kappa CI from 65% of resamples) | 1.00 / 0.94 | 1 / 0 |
| U-ext+seed | 15 | 0.933 [0.800, 1.000] | 0.634 [0.000, 1.000] (kappa CI from 88% of resamples) | 0.93 / 0.87 | 1 / 0 |
| iText2KG | 17 | 0.941 [0.824, 1.000] | 0.767 [0.000, 1.000] (kappa CI from 96% of resamples) | 0.88 / 0.82 | 1 / 0 |
| ALL arms | 79 | 0.899 [0.835, 0.962] | 0.459 [0.134, 0.750] | 0.95 / 0.85 | 8 / 0 |

## Fact precision: human 'supported' rate per arm (95% percentile bootstrap over facts, B = 10000)

skipped facts: 0; replaced arms: none

| arm | n facts | human precision [95% CI] |
|---|---:|---|
| EDC | 40 | 0.800 [0.675, 0.925] |
| L0 | 40 | 0.725 [0.575, 0.850] |
| L0+seed | 40 | 0.775 [0.650, 0.900] |
| Ours | 40 | 0.775 [0.650, 0.900] |
| U-ext+seed | 40 | 0.800 [0.675, 0.925] |
| ALL arms | 200 | 0.775 [0.715, 0.830] |

## Fact judge agreement (Gemma pass 1 vs human), only where a stored verdict exists

| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |
|---|---:|---|---|---|---|
| Ours | 1 | 1.000 [1.000, 1.000] | n/a [n/a, n/a] (kappa CI from 0% of resamples) | 1.00 / 1.00 | 0 / 0 |
| U-ext+seed | 2 | 1.000 [1.000, 1.000] | n/a [n/a, n/a] (kappa CI from 0% of resamples) | 1.00 / 1.00 | 0 / 0 |
| ALL arms | 3 | 1.000 [1.000, 1.000] | n/a [n/a, n/a] (kappa CI from 0% of resamples) | 1.00 / 1.00 | 0 / 0 |

Notes: QA and fact samples are not prevalence-matched (QA balanced on judge gc; facts on the sampled set). Predicate pairs with NA on either side are excluded. Judge FP = judge says 1, human says 0; FN = the reverse.
