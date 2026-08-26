# Benchmark methodology

This document defines the shared corpus, extraction protocol, tokenization,
and metrics used by the version reports and engine comparison.

## Corpus

The main release corpus contains 166 pages in four groups under `pages/`:

- `base/` — 10 independent snapshots of current pages;
- `dragnet/` — the first 20 UUIDs from the manually annotated Dragnet dataset at commit `5d97da4c3c5cf775fa02794b84d31786b8d51d3a`;
- `user/` — 6 pages from open and closed GitHub issues;
- `mozilla/` — all 130 fixtures from Mozilla Readability commit `ab4027a8b37669745016869a37a504727992b2ba`.

Each of the 166 fixture directories contains `page.html`, `ideal.html`,
`actual.html`, and `metadata.json`. The imported fixtures record their
provenance, pinned commit, and license. Attribution is preserved in `NOTICE`;
the complete Dragnet data license is stored in `pages/dragnet/LICENSE`.

An additional fifth group, `jcharum/`, contains 15 real-page fixtures from
`jcharum/lxml-readability` commit `cec2d35c55cc8b94f0f6ff582cf700dab377af8a`.
Their `ideal.html` files were manually checked against the saved `page.html`
and form an independent 15-page evaluation. Each fixture also contains a
generated `silver.html` from Mozilla Readability 0.6.0 through jsdom 26.1.0;
the silver output is not used as ground truth.

The main version reports use 166 pages and one set of 210,572 ideal-content
tokens. The combined 181-page comparison adds the 15 manually annotated
jcharum fixtures. Every compared version is measured again after the corpus
changes.

## Extraction protocol

For comparisons between `readability-lxml` versions, the contents of
`page.html` are passed to `Document` with the URL from `metadata.json`, then
`summary()` is called with default arguments. Baseline 0.8.4.1 receives UTF-8
text because that version cannot process bytes. The 0.9 release benchmark uses
bytes.

The side-by-side comparison uses UTF-8 text for every engine. Exact versions
and configurations are:

- Readability — `Document(source, url=url).summary()`;
- Mozilla Readability — `new Readability(document).parse().content` through
  jsdom 26.1.0;
- Arc90 Readability.js 1.7.1 — pinned browser source through jsdom 26.1.0 with
  a compatibility shim for old `CSSStyleSheet.href` semantics;
- Defuddle — Node API through linkedom with `useAsync:false`;
- Postlight Parser — supplied HTML with `fetchAllPages:false`;
- Trafilatura — default HTML extraction without comments, with links and
  tables;
- Goose3 — `cleaned_text`, with image fetching disabled;
- jusText — English stoplist, combining all non-boilerplate paragraphs;
- Newspaper4k — `Article.parse()` for supplied HTML, with image fetching
  disabled and the official `zh` and `ja` extras installed.

Python engines were installed in separate Python 3.13 virtual environments,
and JavaScript engines in separate Node environments next to the source
repository. Raw per-page results are stored in `benchmarks/results/`, so
analysis does not require repeated extraction.

## Tokenization

Extraction output and `ideal.html` are parsed as HTML. `<h1>` elements are
excluded because the title is not part of the evaluated body and sources place
it differently. The remaining text is converted to lowercase and tokenized
with `\w+(?:['’]\w+)*`; repeated words are counted separately.

## Metrics

Overlap is the multiset intersection of extracted and ideal tokens. Aggregate
precision, recall, and F1 use micro-averaged token counts, so longer articles
carry more weight.

The default regression threshold is F1 `0.95`:

```bash
make benchmark
```

Report values are rounded to three decimal places only for display.

`s/page` is the sum of measured per-page extraction time divided by the number
of pages. Timings come from sequential offline extraction on one machine.
Environments and imports are initialized before the loop, and persistent Node
workers are not restarted for every page.

Token overlap measures text completeness and cleanliness, but not HTML
structure, metadata, or output security. Separate tests cover those properties.
