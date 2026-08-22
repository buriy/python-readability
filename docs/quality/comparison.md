# Extraction engine comparison

## Environment

All engines were installed in separate Python 3.13 environments next to the source repository. Every engine received the same UTF-8 text input. Trafilatura used balanced/default extraction with HTML output, comments disabled, and links and tables enabled.

## Aggregate results

| Engine | Pages | Precision | Recall | F1 | Median/page | Failures |
|---|---:|---:|---:|---:|---:|---:|
| Readability 0.8.4.1 | 146 | 0.972 | 0.881 | 0.924 | 0.074 s | 0 |
| Readability 0.9 | 146 | 0.977 | 0.936 | 0.956 | 0.051 s | 0 |
| Trafilatura 2.2.0 | 146 | 0.962 | 0.957 | 0.959 | 0.044 s | 1 |

## Results by corpus

| Corpus | Pages | Readability 0.8.4.1 F1 | Readability 0.9 F1 | Trafilatura 2.2.0 F1 |
|---|---:|---:|---:|---:|
| base | 10 | 0.964 | 0.983 | 0.983 |
| user | 6 | 0.854 | 0.933 | 0.848 |
| mozilla | 130 | 0.926 | 0.956 | 0.964 |

Trafilatura returned no content for `user/closed-49-guardian-invalid-link`; the comparison counts that page as zero overlap and zero extracted tokens.

## Per-page F1

| Page | Readability 0.8.4.1 | Readability 0.9 | Trafilatura 2.2.0 |
|---|---:|---:|---:|---:|
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
| mozilla/bug-1255978 | 0.185 | 0.185 | 0.324 |
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
| mozilla/ebb-org | 0.117 | 0.117 | 0.992 |
| mozilla/ehow-2 | 0.276 | 0.953 | 0.953 |
| mozilla/ehow-terrarium | 0.363 | 0.854 | 0.875 |
| mozilla/embedded-videos | 0.986 | 0.986 | 0.993 |
| mozilla/engadget-xbox-one-x | 0.295 | 0.970 | 0.995 |
| mozilla/firefox-nightly-blog | 0.012 | 0.774 | 0.881 |
| mozilla/folha-tite-libertadores | 1.000 | 0.948 | 1.000 |
| mozilla/gitlab-blog-article | 0.995 | 0.995 | 1.000 |
| mozilla/gmw | 1.000 | 1.000 | 0.993 |
| mozilla/google-sre-book | 0.980 | 0.980 | 0.987 |
| mozilla/guardian-1 | 0.938 | 0.938 | 0.999 |
| mozilla/heise-1password | 0.070 | 1.000 | 0.978 |
| mozilla/herald-sun-article | 0.844 | 0.844 | 0.894 |
| mozilla/hidden-nodes | 0.507 | 0.672 | 0.507 |
| mozilla/hukumusume-greedy-dog | 0.537 | 0.537 | 1.000 |
| mozilla/iab-1 | 0.988 | 0.988 | 0.985 |
| mozilla/ietf-remotestorage | 1.000 | 1.000 | 1.000 |
| mozilla/invalid-attributes | 1.000 | 1.000 | 1.000 |
| mozilla/js-link-replacement | 1.000 | 1.000 | 1.000 |
| mozilla/keep-images | 0.994 | 0.994 | 0.991 |
| mozilla/keep-tabular-data | 0.995 | 0.995 | 0.971 |
| mozilla/la-nacion-mapuche | 0.992 | 0.992 | 0.990 |
| mozilla/lazy-image-1 | 0.781 | 0.781 | 0.971 |
| mozilla/lazy-image-2 | 0.999 | 1.000 | 0.991 |
| mozilla/lazy-image-3 | 1.000 | 1.000 | 1.000 |
| mozilla/lemonde-intelligence-law | 1.000 | 1.000 | 1.000 |
| mozilla/liberation-nepal-earthquake | 1.000 | 0.998 | 1.000 |
| mozilla/lifehacker-article | 0.974 | 0.974 | 1.000 |
| mozilla/lifehacker-post-comment-load | 0.021 | 0.978 | 1.000 |
| mozilla/links-in-tables | 0.995 | 1.000 | 0.979 |
| mozilla/lwn-article | 0.988 | 0.988 | 0.971 |
| mozilla/mathjax | 0.537 | 0.537 | 0.537 |
| mozilla/medical-news-today-article | 0.063 | 1.000 | 0.982 |
| mozilla/medium-2 | 1.000 | 1.000 | 0.976 |
| mozilla/medium-3 | 0.818 | 0.818 | 0.999 |
| mozilla/medium-article | 0.999 | 0.999 | 0.991 |
| mozilla/mercurial | 0.934 | 0.934 | 0.942 |
| mozilla/metadata-content-missing | 0.989 | 0.989 | 0.657 |
| mozilla/missing-paragraphs | 1.000 | 1.000 | 1.000 |
| mozilla/mozilla-1 | 0.385 | 0.385 | 0.912 |
| mozilla/mozilla-2 | 0.291 | 0.291 | 1.000 |
| mozilla/msn-super-mario-run | 0.998 | 0.998 | 0.987 |
| mozilla/normalize-spaces | 0.996 | 0.996 | 0.996 |
| mozilla/nytimes-2 | 0.888 | 0.998 | 0.996 |
| mozilla/nytimes-3 | 0.893 | 0.893 | 0.893 |
| mozilla/nytimes-4 | 0.957 | 0.957 | 0.957 |
| mozilla/nytimes-5 | 0.059 | 0.059 | 0.507 |
| mozilla/nytimes-sudan-sanctions | 1.000 | 0.994 | 0.966 |
| mozilla/ol | 1.000 | 1.000 | 1.000 |
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
| mozilla/table-style-attributes | 0.999 | 0.999 | 0.926 |
| mozilla/telegraph-zimbabwe | 0.599 | 1.000 | 0.982 |
| mozilla/the-verge-vision-pro | 0.998 | 0.983 | 0.937 |
| mozilla/title-and-h1-discrepancy | 0.948 | 0.948 | 0.621 |
| mozilla/title-en-dash | 1.000 | 1.000 | 0.667 |
| mozilla/tmz-1 | 0.994 | 0.994 | 0.931 |
| mozilla/toc-missing | 0.991 | 0.990 | 0.989 |
| mozilla/topicseed-1 | 0.990 | 0.990 | 0.986 |
| mozilla/tumblr | 0.993 | 0.993 | 0.962 |
| mozilla/v8-blog | 0.999 | 1.000 | 1.000 |
| mozilla/videos-1 | 0.992 | 0.992 | 0.978 |
| mozilla/videos-2 | 0.998 | 0.996 | 0.998 |
| mozilla/visibility-hidden | 0.627 | 0.627 | 0.624 |
| mozilla/wapo-2 | 0.985 | 0.985 | 0.961 |
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
| user/closed-30-macrumors-inline | 0.656 | 0.655 | 0.951 |
| user/closed-49-guardian-invalid-link | 0.935 | 0.935 | 0.000 |
| user/open-119-fiol-missing-sections | 0.523 | 0.941 | 0.927 |
| user/open-170-blogger-inline | 0.996 | 0.996 | 0.996 |
| user/open-171-cyberwire-sections | 0.858 | 0.942 | 0.858 |
