# Extraction quality

This directory contains reproducible extraction reports:

- [0.8.4 baseline](0.8.4.md)
- [0.9 candidate](0.9.md)
- [three-engine comparison](comparison.md)
- [user issue corpus](user-corpus.md)

## Corpus

The corpus is stored in three groups under `pages/`:

- `base/` — 10 independent current-page snapshots;
- `user/` — 6 pages reported in open and closed GitHub issues;
- `mozilla/` — all 130 fixtures from Mozilla Readability commit `ab4027a8b37669745016869a37a504727992b2ba`.

Each of the 146 fixture directories contains `page.html`, `ideal.html`, `actual.html`, and `metadata.json`. Mozilla provenance and the pinned commit are recorded in each imported fixture. Attribution is retained in the repository `NOTICE` file.

The version reports use the same set of 198,361 ideal-content tokens. Changing the corpus requires measuring every compared version again.

## Extraction protocol

To compare `readability-lxml` versions, `page.html` is passed to `Document` with the URL from `metadata.json`, and `summary()` is called with default arguments. The 0.8.4.1 baseline uses UTF-8 text because that version fails when given bytes. The 0.9 release benchmark uses bytes.

The side-by-side engine comparison uses UTF-8 text for all engines. Its exact Trafilatura configuration and environment are recorded in [comparison.md](comparison.md).

## Tokenization

The extracted output and `ideal.html` are parsed as HTML. `<h1>` elements are excluded because the title is not part of the evaluated body and sources place it differently. Remaining text is lowercased and tokenized with `\w+(?:['’]\w+)*`; repeated words are counted separately.

## Metrics

Overlap is the multiset intersection of extracted and ideal tokens. Aggregate precision, recall, and F1 use micro-averaged token counts, so longer articles have more weight.

The default regression threshold is F1 `0.95`:

```bash
make benchmark
```

Values in reports are rounded to three decimal places only for display.
