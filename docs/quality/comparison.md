# Extraction engine comparison

Ten extraction engines were measured on the same 181 saved pages. Exact
configurations, metric definitions, and reproduction commands are documented
in the [benchmark methodology](methodology.md) and
[detailed results](detailed-results.md).

## Aggregate results

| Engine | Pages | Precision | Recall | F1 | s/page | Failures |
|---|---:|---:|---:|---:|---:|---:|
| Mozilla Readability 0.6.0 | 181 | 0.984843 | 0.988054 | **0.986446** | 0.136117 | 0 |
| Readability 0.9 | 181 | 0.991465 | 0.959304 | **0.975120** | 0.082809 | 0 |
| Trafilatura 2.2.0 | 181 | 0.962477 | 0.957424 | 0.959944 | 0.050174 | 1 |
| Defuddle 0.19.2 | 181 | 0.943781 | 0.953461 | 0.948597 | 0.175439 | 2 |
| Readability 0.8.4.1 | 181 | 0.973377 | 0.888917 | 0.929232 | 0.077070 | 0 |
| Postlight Parser 2.2.3 | 181 | 0.946154 | 0.910864 | 0.928174 | 0.072220 | 3 |
| Arc90 Readability.js 1.7.1 | 181 | 0.954803 | 0.885414 | 0.918800 | 0.432534 | 0 |
| Newspaper4k 0.9.6 | 181 | 0.991088 | 0.778143 | 0.871801 | 0.195238 | 11 |
| jusText 3.0.2 | 181 | 0.908048 | 0.749686 | 0.821303 | **0.026058** | 55 |
| Goose3 3.1.22 | 181 | 0.978587 | 0.698158 | 0.814922 | 0.157307 | 17 |

Mozilla Readability leads the aggregate table, but 130 fixtures come from its
own test suite. Readability 0.9 has the highest F1 on the 51 pages outside the
Mozilla corpus.

## Results without Mozilla fixtures

| Engine | Pages | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Readability 0.9 | 51 | 0.989625 | 0.961252 | **0.975232** |
| Defuddle 0.19.2 | 51 | 0.950587 | 0.985016 | **0.967495** |
| Trafilatura 2.2.0 | 51 | 0.974894 | 0.913372 | 0.943130 |
| Arc90 Readability.js 1.7.1 | 51 | 0.982933 | 0.903536 | 0.941564 |
| Readability 0.8.4.1 | 51 | 0.984874 | 0.901182 | 0.941171 |
| Mozilla Readability 0.6.0 | 51 | 0.925944 | 0.944199 | 0.934982 |
| Postlight Parser 2.2.3 | 51 | 0.963982 | 0.881598 | 0.920952 |
| Newspaper4k 0.9.6 | 51 | 0.987765 | 0.753185 | 0.854671 |
| jusText 3.0.2 | 51 | 0.831256 | 0.783682 | 0.806768 |
| Goose3 3.1.22 | 51 | 0.988287 | 0.657227 | 0.789454 |

## Results by corpus

| Corpus | Pages | Readability 0.8.4.1 | Readability 0.9 | Mozilla 0.6.0 | Arc90 1.7.1 | Defuddle 0.19.2 | Postlight 2.2.3 | Trafilatura 2.2.0 | Goose3 3.1.22 | jusText 3.0.2 | Newspaper4k 0.9.6 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base | 10 | 0.964 | **0.983** | 0.980 | 0.977 | 0.980 | 0.861 | 0.983 | 0.718 | 0.923 | 0.966 |
| dragnet | 20 | 0.953 | **0.965** | 0.963 | 0.950 | 0.948 | 0.953 | 0.959 | 0.938 | 0.881 | 0.957 |
| user | 6 | 0.854 | 0.944 | 0.882 | 0.853 | **0.981** | 0.811 | 0.848 | 0.409 | 0.556 | 0.258 |
| mozilla | 130 | 0.926 | 0.975 | **1.000** | 0.913 | 0.944 | 0.930 | 0.964 | 0.821 | 0.825 | 0.876 |
| jcharum | 15 | 0.977 | **1.000** | 0.928 | 0.976 | 0.968 | 0.988 | 0.971 | 0.879 | 0.826 | 0.971 |

Readability 0.9 leads on base, Dragnet, and jcharum. Defuddle leads on the user
corpus, and Mozilla Readability leads on its own corpus. These slices are not
fully neutral: the Mozilla fixtures belong to Mozilla's suite, and jcharum was
used while developing the 0.9 fixes.

## Detailed analysis

The [detailed results](detailed-results.md) include:

- full precision, recall, and F1 values for every corpus and engine;
- extraction failures and saved-result locations;
- the complete Dragnet dataset check;
- manually curated and Mozilla-silver jcharum measurements;
- remaining differences and the post-0.9 improvement plan;
- per-page F1 for Readability 0.8.4.1, Readability 0.9, and Trafilatura 2.2.0.
