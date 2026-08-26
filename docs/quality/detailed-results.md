# Detailed extraction results

This document preserves the complete benchmark tables, failure analysis,
reproducibility notes, and per-page results. See the concise
[engine comparison](comparison.md) for the primary findings.

The comparison contains 181 fixtures with `ideal.html`: the main set of 166
fixtures and 15 manually checked jcharum pages. See the
[benchmark methodology](methodology.md) for engine configurations and metric
definitions.

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

Mozilla Readability has the best aggregate F1, but 130 of the 181 fixtures come
from its own test suite. Its F1 on the Mozilla corpus rounds to `1.000`, so the
overall result is not an independent comparison. On the 51 pages outside the
Mozilla corpus, Readability 0.9 leads with F1 `0.975232`; Defuddle is second at
`0.967495`. This slice is not fully neutral either because the jcharum corpus
was used while developing the 0.9 fixes. Readability 0.9 leads on base,
Dragnet, and jcharum; Defuddle leads on the user corpus. jusText was fastest,
and Arc90 was slowest.

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

Values in this table are micro-averaged F1 within each group. Full precision,
recall, and F1 values follow:

| Corpus | Engine | Precision | Recall | F1 |
|---|---|---:|---:|---:|
| base | Readability 0.8.4.1 | 0.996 | 0.933 | 0.964 |
| base | Readability 0.9 | 0.999 | 0.968 | 0.983 |
| base | Mozilla Readability 0.6.0 | 0.976 | 0.983 | 0.980 |
| base | Arc90 Readability.js 1.7.1 | 0.994 | 0.960 | 0.977 |
| base | Defuddle 0.19.2 | 0.967 | 0.992 | 0.980 |
| base | Postlight Parser 2.2.3 | 0.855 | 0.867 | 0.861 |
| base | Trafilatura 2.2.0 | 0.978 | 0.989 | 0.983 |
| base | Goose3 3.1.22 | 0.999 | 0.560 | 0.718 |
| base | jusText 3.0.2 | 0.971 | 0.879 | 0.923 |
| base | Newspaper4k 0.9.6 | 0.994 | 0.939 | 0.966 |
| dragnet | Readability 0.8.4.1 | 0.969 | 0.938 | 0.953 |
| dragnet | Readability 0.9 | 0.970 | 0.961 | 0.965 |
| dragnet | Mozilla Readability 0.6.0 | 0.958 | 0.969 | 0.963 |
| dragnet | Arc90 Readability.js 1.7.1 | 0.965 | 0.935 | 0.950 |
| dragnet | Defuddle 0.19.2 | 0.916 | 0.982 | 0.948 |
| dragnet | Postlight Parser 2.2.3 | 0.965 | 0.941 | 0.953 |
| dragnet | Trafilatura 2.2.0 | 0.962 | 0.955 | 0.959 |
| dragnet | Goose3 3.1.22 | 0.972 | 0.906 | 0.938 |
| dragnet | jusText 3.0.2 | 0.926 | 0.840 | 0.881 |
| dragnet | Newspaper4k 0.9.6 | 0.972 | 0.943 | 0.957 |
| user | Readability 0.8.4.1 | 0.975 | 0.760 | 0.854 |
| user | Readability 0.9 | 0.991 | 0.902 | 0.944 |
| user | Mozilla Readability 0.6.0 | 0.961 | 0.815 | 0.882 |
| user | Arc90 Readability.js 1.7.1 | 0.973 | 0.760 | 0.853 |
| user | Defuddle 0.19.2 | 0.986 | 0.977 | 0.981 |
| user | Postlight Parser 2.2.3 | 0.998 | 0.684 | 0.811 |
| user | Trafilatura 2.2.0 | 0.994 | 0.739 | 0.848 |
| user | Goose3 3.1.22 | 0.991 | 0.258 | 0.409 |
| user | jusText 3.0.2 | 0.907 | 0.400 | 0.556 |
| user | Newspaper4k 0.9.6 | 0.988 | 0.148 | 0.258 |
| mozilla | Readability 0.8.4.1 | 0.970 | 0.886 | 0.926 |
| mozilla | Readability 0.9 | 0.992 | 0.959 | 0.975 |
| mozilla | Mozilla Readability 0.6.0 | 1.000 | 0.999 | 1.000 |
| mozilla | Arc90 Readability.js 1.7.1 | 0.948 | 0.881 | 0.913 |
| mozilla | Defuddle 0.19.2 | 0.942 | 0.946 | 0.944 |
| mozilla | Postlight Parser 2.2.3 | 0.942 | 0.918 | 0.930 |
| mozilla | Trafilatura 2.2.0 | 0.960 | 0.969 | 0.964 |
| mozilla | Goose3 3.1.22 | 0.976 | 0.708 | 0.821 |
| mozilla | jusText 3.0.2 | 0.931 | 0.741 | 0.825 |
| mozilla | Newspaper4k 0.9.6 | 0.992 | 0.784 | 0.876 |
| jcharum | Readability 0.8.4.1 | 0.998 | 0.957 | 0.977 |
| jcharum | Readability 0.9 | 1.000 | 1.000 | 1.000 |
| jcharum | Mozilla Readability 0.6.0 | 0.867 | 0.999 | 0.928 |
| jcharum | Arc90 Readability.js 1.7.1 | 0.998 | 0.954 | 0.976 |
| jcharum | Defuddle 0.19.2 | 0.948 | 0.990 | 0.968 |
| jcharum | Postlight Parser 2.2.3 | 0.996 | 0.980 | 0.988 |
| jcharum | Trafilatura 2.2.0 | 0.973 | 0.970 | 0.971 |
| jcharum | Goose3 3.1.22 | 0.999 | 0.784 | 0.879 |
| jcharum | jusText 3.0.2 | 0.721 | 0.966 | 0.826 |
| jcharum | Newspaper4k 0.9.6 | 0.997 | 0.946 | 0.971 |

## Extraction failures

An empty result or exception counts as an extraction failure with zero overlap;
it is not excluded from the metric. Both Python Readability versions, Mozilla
Readability, and Arc90 processed every page. Defuddle has two empty results in
the Mozilla corpus. Postlight has three failures: one each in base, Mozilla,
and user. Trafilatura returned an empty result for
`user/closed-49-guardian-invalid-link`. Goose3 has 17 failures, jusText 55, and
Newspaper4k with multilingual extras 11.

Goose3 and Newspaper4k target full news articles and extract little text from
short or synthetic test pages. Goose3 therefore retains high precision at low
recall. Newspaper4k performs better on base and Dragnet but loses substantial
recall on the issue-derived user corpus. These results describe this corpus and
these configurations, not every library feature such as metadata, NLP, or image
extraction.

## Reproducibility and saved results

The runner is `benchmarks/compare.py`, and the Node workers are
`benchmarks/*_js.mjs`. Raw JSON containing aggregate, group, and per-page
results for all ten engines is stored in `benchmarks/results/`. Building tables
does not require repeated extraction; extraction is needed after changing the
corpus, engine version, or configuration.

Mozilla Readability is installed with jsdom 26.1.0 in a separate
`../mozilla-readability-0.6.0` environment. The command for the main 166-page
corpus is:

```bash
.venv/bin/python benchmarks/compare.py readability-js 0.6.0 \
  benchmarks/results/comparison-readability-js-0.6.0-166.json \
  --readability-js-env ../mozilla-readability-0.6.0
```

Arc90 uses source commit `0ac367b6def41f1e841282790ceb80989ac3b404` from
`MHordecki/readability-redux`. The compatibility adapter does not change
extraction logic; it only restores the `null` value for `CSSStyleSheet.href`
expected by browsers of the Arc90 1.7.1 era. Defuddle and Postlight operate
only on saved HTML; asynchronous network extraction and multi-page fetching
are disabled.

## Additional full Dragnet dataset check

The complete set of 500 manually annotated Dragnet pages was measured outside
the release corpus. Readability 0.9 achieved precision `0.949`, recall `0.910`,
and F1 `0.929`; Trafilatura 2.2.0 achieved precision `0.947`, recall `0.966`,
and F1 `0.957`. The complete unpacked dataset occupies about 139 MB, so the
repository includes only the fixed 20-page sample.

The older `jcharum/lxml-readability` fork was also checked. It contains 15
real-page regression cases and HTML diff measurements. These pages were added
separately from the 166-page release corpus, and their `ideal.html` files were
manually checked against the saved source DOM.

## Manually curated jcharum benchmark

Manual review corrected four generated baselines: two Washington Post pages
lost lead article fragments around the side rail, Slate lost a quote
introduction and blockquotes, and Ars Technica lost the article table of
contents. Navigation, comments, related stories, market widgets, and
promotional callouts were excluded. The JavaScript-only Business Insider
slideshow payload was not included because the offline protocol does not
execute page scripts.

| Engine | Pages | Precision | Recall | F1 | s/page | Failures |
|---|---:|---:|---:|---:|---:|---:|
| Readability 0.9 | 15 | 1.000 | 1.000 | **1.000** | 0.040 | 0 |
| Postlight Parser 2.2.3 | 15 | 0.996 | 0.980 | 0.988 | 0.093 | 0 |
| Readability 0.8.4.1 | 15 | 0.998 | 0.957 | 0.977 | 0.036 | 0 |
| Arc90 Readability.js 1.7.1 | 15 | 0.998 | 0.954 | 0.976 | 0.368 | 0 |
| Trafilatura 2.2.0 | 15 | 0.973 | 0.970 | 0.971 | 0.048 | 0 |
| Newspaper4k 0.9.6 | 15 | 0.997 | 0.946 | 0.971 | 0.175 | 0 |
| Defuddle 0.19.2 | 15 | 0.948 | 0.990 | 0.968 | 0.165 | 0 |
| Mozilla Readability 0.6.0 | 15 | 0.867 | 0.999 | 0.928 | 0.231 | 0 |
| Goose3 3.1.22 | 15 | 0.999 | 0.784 | 0.879 | 0.135 | 0 |
| jusText 3.0.2 | 15 | 0.721 | 0.966 | 0.826 | 0.032 | 0 |

Timings come from sequential offline execution. Raw per-page reports and
failures are stored in `benchmarks/results/*-jcharum-manual-15.json`.

## Mozilla silver reference for jcharum

All 15 jcharum pages were also processed by Mozilla Readability 0.6.0 through
jsdom 26.1.0. Its output is stored in `silver.html`, with provenance in
`regression.json`. Against this silver reference, Python Readability 0.9
achieved precision `0.999`, recall `0.867`, and F1 `0.928`, with no extraction
failures.

Reproducible generation and comparison commands:

```bash
.venv/bin/python benchmarks/compare.py readability-js 0.6.0 \
  benchmarks/results/comparison-readability-js-0.6.0-jcharum-regression-15.json \
  --readability-js-env ../mozilla-readability-0.6.0 \
  --metadata-name regression.json --ideal-name ideal.html \
  --save-output-name silver.html
.venv/bin/python benchmarks/compare.py readability 0.9 \
  benchmarks/results/comparison-readability-0.9-jcharum-silver-15.json \
  --metadata-name regression.json --ideal-name silver.html
```

| Fixture | Precision | Recall | F1 | Silver tokens absent from Python |
|---|---:|---:|---:|---:|
| businessinsider-000 | 0.981 | 0.067 | 0.125 | 2 178 |
| washingtonpost-001 | 1.000 | 0.805 | 0.892 | 125 |
| washingtonpost-000 | 1.000 | 0.918 | 0.957 | 66 |
| slate-000 | 0.970 | 0.987 | 0.979 | 6 |
| espn-000 | 1.000 | 0.994 | 0.997 | 7 |

Low recall does not mean that all additional Mozilla output should be copied.
The silver output for `businessinsider-000` contains navigation and related
story links, while `washingtonpost-001` contains market data and footer blocks.
The silver reference is therefore used to find recall candidates and review
regressions, but is excluded from the independent ranking.

## Remaining differences

Simple semantic guards improved segmented pages: `mozilla-1` reached F1
`0.947`, `mozilla-2` `0.965`, `lazy-image-1` `0.978`, and `medium-3` `0.931`.
MathJax content is now retained at F1 `1.000`. `nytimes-5` remains a separate
case where a small block is selected incorrectly, while `wikipedia-4` selects
one large table instead of the full article body. The low
`hukumusume-greedy-dog` score is caused by an ideal output that includes the
site directory and related widgets after the complete story.

## Post-0.9 plan

1. Publish the verified 0.9 release and close the changelog issues after publication.
2. Implement and measure Mozilla-style multi-attempt candidate selection first. Disable unlikely-candidate stripping, class weighting, and conditional cleaning in sequence, select by content score, and begin with `nytimes-5`, where F1 is `0.059` while Mozilla reaches `1.000`. This is a separate mechanism and must not become an unconditional fallback without checking precision across every corpus.
3. Investigate `wikipedia-4`, where a large sortable table outscores the complete `main`; the change should use semantic article evidence rather than a Wikipedia-specific rule.
4. Do not optimize the extractor for `hukumusume-greedy-dog` before correcting its ideal output: the current output contains the complete story, and the missing tokens belong to site widgets.
5. Examine the imported or embedded article body in `user/closed-173-verge-import` (`0.851` versus Postlight's `0.975`) and segmented sections in `user/open-171-cyberwire-sections` (`0.942` versus Defuddle's `0.993`). Do not move site-specific Defuddle extractors into core without separate measurement because domain rules increase the maintenance surface.
6. For every change, calculate precision, recall, and F1 deltas separately for base, Dragnet, user, Mozilla, and jcharum. Accept a change only when precision does not fall materially; the current 181-page result has recall `0.959304` at precision `0.991465`.
7. Decide separately whether to include the complete 500-page Dragnet dataset, considering its size and CI time.

## Per-page F1 for the three primary engines

| Page | Readability 0.8.4.1 | Readability 0.9 | Trafilatura 2.2.0 |
|---|---:|---:|---:|
| base/africanews-ghana-repatriation | 1.000 | 1.000 | 0.994 |
| base/aljazeera-west-bank | 0.990 | 1.000 | 1.000 |
| base/django-speaker-lineup | 0.048 | 0.972 | 0.964 |
| base/guardian-army-kenya | 0.985 | 0.985 | 0.985 |
| base/nasa-astronaut-return | 0.983 | 0.983 | 1.000 |
| base/python-315-alpha-6 | 0.953 | 0.953 | 0.988 |
| base/rnz-parental-leave | 0.977 | 0.987 | 0.962 |
| base/times-india-parliament | 1.000 | 1.000 | 1.000 |
| base/un-news-global | 0.973 | 1.000 | 0.998 |
| base/wikipedia-kanom-piakpoon | 0.900 | 0.900 | 0.924 |
| dragnet/abcnews-go-com-054b1328 | 0.961 | 0.961 | 0.978 |
| dragnet/bbc-co-uk-06f23d19 | 0.976 | 0.976 | 0.975 |
| dragnet/buzzfeed-com-02c0f2ea | 0.979 | 0.979 | 0.996 |
| dragnet/cbc-ca-05b58651 | 0.948 | 0.948 | 0.940 |
| dragnet/designyoutrust-com-0401ed26 | 0.972 | 0.972 | 0.985 |
| dragnet/dw-com-00f16132 | 0.963 | 0.963 | 0.967 |
| dragnet/edsurge-com-04c44b3f | 0.994 | 0.994 | 0.994 |
| dragnet/foxnews-com-0577765a | 0.960 | 0.959 | 0.942 |
| dragnet/globalnews-ca-05d3f23b | 0.931 | 0.929 | 0.945 |
| dragnet/goodmenproject-com-005cdad0 | 0.982 | 0.982 | 0.961 |
| dragnet/mensjournal-com-06b9d2a9 | 0.912 | 0.912 | 0.846 |
| dragnet/sciencedaily-com-03d6e790 | 0.912 | 0.912 | 0.913 |
| dragnet/smallbiztrends-com-06b7f020 | 0.947 | 0.947 | 0.947 |
| dragnet/telegraph-co-uk-05f1c7b6 | 0.789 | 0.985 | 0.949 |
| dragnet/telegraph-co-uk-061dafdf | 0.688 | 0.979 | 0.955 |
| dragnet/theguardian-com-007ce512 | 0.981 | 0.981 | 0.981 |
| dragnet/thisiscolossal-com-06bfa65e | 0.925 | 0.925 | 0.867 |
| dragnet/thisiscolossal-com-078e4f7d | 0.841 | 0.841 | 0.763 |
| dragnet/womenandhollywood-com-05e04c48 | 1.000 | 1.000 | 1.000 |
| dragnet/zdnet-com-02c50335 | 0.933 | 0.933 | 0.796 |
| mozilla/001 | 0.976 | 0.976 | 0.993 |
| mozilla/002 | 0.993 | 0.993 | 1.000 |
| mozilla/003-metadata-preferred | 0.989 | 0.989 | 0.657 |
| mozilla/004-metadata-space-separated-properties | 0.989 | 0.989 | 0.657 |
| mozilla/005-unescape-html-entities | 1.000 | 1.000 | 1.000 |
| mozilla/aclu-surveillance | 1.000 | 1.000 | 0.984 |
| mozilla/aktualne-news | 0.988 | 0.988 | 0.948 |
| mozilla/archive-of-our-own | 1.000 | 1.000 | 1.000 |
| mozilla/ars-technica-article | 0.989 | 0.988 | 0.989 |
| mozilla/article-author-tag | 1.000 | 1.000 | 1.000 |
| mozilla/base-url | 0.996 | 0.996 | 0.967 |
| mozilla/base-url-base-element | 0.996 | 0.996 | 0.967 |
| mozilla/base-url-base-element-relative | 0.996 | 0.996 | 0.967 |
| mozilla/basic-tags-cleaning | 1.000 | 1.000 | 0.996 |
| mozilla/bbc-obama-gun-laws | 1.000 | 1.000 | 0.982 |
| mozilla/blogger | 1.000 | 1.000 | 0.929 |
| mozilla/breitbart-snopes | 0.989 | 0.989 | 0.964 |
| mozilla/bug-1255978 | 0.185 | 0.920 | 0.324 |
| mozilla/buzzfeed-diet-pills | 0.945 | 0.997 | 0.916 |
| mozilla/citylab-article | 0.970 | 0.977 | 0.961 |
| mozilla/clean-links | 0.967 | 0.967 | 0.991 |
| mozilla/cnet-facebook-acquisitions | 1.000 | 1.000 | 0.988 |
| mozilla/cnet-svg-classes | 1.000 | 1.000 | 0.941 |
| mozilla/cnn-birth-lottery | 1.000 | 0.994 | 0.977 |
| mozilla/comment-inside-script-parsing | 1.000 | 1.000 | 0.996 |
| mozilla/daring-fireball-article | 0.960 | 0.960 | 0.932 |
| mozilla/data-url-image | 1.000 | 1.000 | 1.000 |
| mozilla/dev418 | 1.000 | 1.000 | 0.960 |
| mozilla/dropbox-blog | 0.996 | 0.996 | 0.999 |
| mozilla/ebb-org | 0.117 | 0.970 | 0.992 |
| mozilla/ehow-2 | 0.276 | 0.953 | 0.953 |
| mozilla/ehow-terrarium | 0.363 | 0.854 | 0.875 |
| mozilla/embedded-videos | 0.986 | 0.986 | 0.993 |
| mozilla/engadget-xbox-one-x | 0.295 | 0.970 | 0.995 |
| mozilla/firefox-nightly-blog | 0.012 | 0.792 | 0.881 |
| mozilla/folha-tite-libertadores | 1.000 | 0.948 | 1.000 |
| mozilla/gitlab-blog-article | 0.995 | 0.995 | 1.000 |
| mozilla/gmw | 1.000 | 1.000 | 0.993 |
| mozilla/google-sre-book | 0.980 | 0.980 | 0.987 |
| mozilla/guardian-1 | 0.938 | 0.938 | 0.999 |
| mozilla/heise-1password | 0.070 | 1.000 | 0.978 |
| mozilla/herald-sun-article | 0.844 | 0.844 | 0.894 |
| mozilla/hidden-nodes | 0.507 | 1.000 | 0.507 |
| mozilla/hukumusume-greedy-dog | 0.537 | 0.537 | 1.000 |
| mozilla/iab-1 | 0.988 | 0.988 | 0.985 |
| mozilla/ietf-remotestorage | 1.000 | 1.000 | 1.000 |
| mozilla/invalid-attributes | 1.000 | 1.000 | 1.000 |
| mozilla/js-link-replacement | 1.000 | 1.000 | 1.000 |
| mozilla/keep-images | 0.994 | 0.994 | 0.991 |
| mozilla/keep-tabular-data | 0.995 | 0.995 | 0.971 |
| mozilla/la-nacion-mapuche | 0.992 | 0.992 | 0.990 |
| mozilla/lazy-image-1 | 0.781 | 0.978 | 0.971 |
| mozilla/lazy-image-2 | 0.999 | 1.000 | 0.991 |
| mozilla/lazy-image-3 | 1.000 | 1.000 | 1.000 |
| mozilla/lemonde-intelligence-law | 1.000 | 1.000 | 1.000 |
| mozilla/liberation-nepal-earthquake | 1.000 | 0.998 | 1.000 |
| mozilla/lifehacker-article | 0.974 | 0.974 | 1.000 |
| mozilla/lifehacker-post-comment-load | 0.021 | 0.978 | 1.000 |
| mozilla/links-in-tables | 0.995 | 1.000 | 0.979 |
| mozilla/lwn-article | 0.988 | 0.988 | 0.971 |
| mozilla/mathjax | 0.537 | 1.000 | 0.537 |
| mozilla/medical-news-today-article | 0.063 | 1.000 | 0.982 |
| mozilla/medium-2 | 1.000 | 1.000 | 0.976 |
| mozilla/medium-3 | 0.818 | 0.931 | 0.999 |
| mozilla/medium-article | 0.999 | 0.999 | 0.991 |
| mozilla/mercurial | 0.934 | 0.934 | 0.942 |
| mozilla/metadata-content-missing | 0.989 | 0.989 | 0.657 |
| mozilla/missing-paragraphs | 1.000 | 1.000 | 1.000 |
| mozilla/mozilla-1 | 0.385 | 0.947 | 0.912 |
| mozilla/mozilla-2 | 0.291 | 0.965 | 1.000 |
| mozilla/msn-super-mario-run | 0.998 | 0.998 | 0.987 |
| mozilla/normalize-spaces | 0.996 | 0.996 | 0.996 |
| mozilla/nytimes-2 | 0.888 | 0.998 | 0.996 |
| mozilla/nytimes-3 | 0.893 | 0.893 | 0.893 |
| mozilla/nytimes-4 | 0.957 | 0.974 | 0.957 |
| mozilla/nytimes-5 | 0.059 | 0.059 | 0.507 |
| mozilla/nytimes-sudan-sanctions | 1.000 | 0.994 | 0.966 |
| mozilla/ol | 1.000 | 0.909 | 1.000 |
| mozilla/parsely-metadata | 0.989 | 0.989 | 0.657 |
| mozilla/pixnet-camping | 1.000 | 1.000 | 0.877 |
| mozilla/qq-news-article | 0.914 | 0.914 | 0.895 |
| mozilla/quanta-article | 0.710 | 1.000 | 1.000 |
| mozilla/remove-aria-hidden | 0.986 | 0.986 | 0.973 |
| mozilla/remove-extra-brs | 1.000 | 1.000 | 0.996 |
| mozilla/remove-extra-paragraphs | 1.000 | 1.000 | 0.996 |
| mozilla/remove-script-tags | 1.000 | 1.000 | 0.996 |
| mozilla/reordering-paragraphs | 1.000 | 1.000 | 1.000 |
| mozilla/replace-brs | 0.996 | 0.996 | 0.670 |
| mozilla/replace-font-tags | 0.996 | 0.996 | 0.996 |
| mozilla/royal-road | 0.993 | 0.993 | 0.999 |
| mozilla/rtl-1 | 0.996 | 0.996 | 0.996 |
| mozilla/rtl-2 | 0.996 | 0.996 | 0.996 |
| mozilla/rtl-3 | 0.996 | 0.996 | 0.996 |
| mozilla/rtl-4 | 0.996 | 0.996 | 0.996 |
| mozilla/salon-sharing-economy | 0.979 | 0.979 | 0.942 |
| mozilla/schema-org-context-object | 0.985 | 0.985 | 0.954 |
| mozilla/seattle-times-halibut | 1.000 | 1.000 | 0.992 |
| mozilla/simplyfound-1 | 1.000 | 1.000 | 0.953 |
| mozilla/social-buttons | 0.990 | 0.990 | 0.331 |
| mozilla/spiceworks-vidyard | 1.000 | 1.000 | 0.992 |
| mozilla/style-tags-removal | 0.996 | 0.996 | 0.996 |
| mozilla/svg-parsing | 1.000 | 1.000 | 1.000 |
| mozilla/table-style-attributes | 0.999 | 0.998 | 0.926 |
| mozilla/telegraph-zimbabwe | 0.599 | 1.000 | 0.982 |
| mozilla/the-verge-vision-pro | 0.998 | 0.984 | 0.937 |
| mozilla/title-and-h1-discrepancy | 0.948 | 0.948 | 0.621 |
| mozilla/title-en-dash | 1.000 | 1.000 | 0.667 |
| mozilla/tmz-1 | 0.994 | 0.994 | 0.931 |
| mozilla/toc-missing | 0.991 | 0.990 | 0.989 |
| mozilla/topicseed-1 | 0.990 | 0.990 | 0.986 |
| mozilla/tumblr | 0.993 | 0.993 | 0.962 |
| mozilla/v8-blog | 0.999 | 1.000 | 1.000 |
| mozilla/videos-1 | 0.992 | 0.992 | 0.978 |
| mozilla/videos-2 | 0.998 | 0.996 | 0.998 |
| mozilla/visibility-hidden | 0.627 | 1.000 | 0.624 |
| mozilla/wapo-2 | 0.985 | 1.000 | 0.961 |
| mozilla/washington-post-tunisia | 1.000 | 1.000 | 0.986 |
| mozilla/webmd-2 | 0.988 | 0.974 | 0.952 |
| mozilla/webmd-peanut-allergy | 0.990 | 0.974 | 0.950 |
| mozilla/wikia | 1.000 | 1.000 | 1.000 |
| mozilla/wikipedia | 0.975 | 0.974 | 0.978 |
| mozilla/wikipedia-2 | 0.985 | 0.986 | 0.987 |
| mozilla/wikipedia-3 | 0.714 | 0.934 | 0.956 |
| mozilla/wikipedia-4 | 0.753 | 0.753 | 0.999 |
| mozilla/wordpress | 0.869 | 0.870 | 1.000 |
| mozilla/yahoo-1 | 0.940 | 0.940 | 0.963 |
| mozilla/yahoo-2 | 0.828 | 0.828 | 0.513 |
| mozilla/yahoo-3 | 0.989 | 0.989 | 0.472 |
| mozilla/yahoo-4 | 1.000 | 1.000 | 1.000 |
| mozilla/youth-two-sessions | 1.000 | 1.000 | 1.000 |
| user/closed-173-verge-import | 0.851 | 0.851 | 0.842 |
| user/closed-30-macrumors-inline | 0.656 | 0.996 | 0.951 |
| user/closed-49-guardian-invalid-link | 0.935 | 0.935 | 0.000 |
| user/open-119-fiol-missing-sections | 0.523 | 0.941 | 0.927 |
| user/open-170-blogger-inline | 0.996 | 0.996 | 0.996 |
| user/open-171-cyberwire-sections | 0.858 | 0.942 | 0.858 |
