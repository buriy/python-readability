# User issue corpus

The user corpus contains saved pages from reproducible GitHub issue reports:
three open and three closed issues. `ideal.html` is built from the semantic
content containers recorded in `metadata.json`, independently of the compared
extraction engines.

| Fixture | Issue | State | Site | Readability 0.9 F1 |
|---|---:|---|---|---:|
| closed-173-verge-import | [#173](https://github.com/buriy/python-readability/issues/173) | closed | www.theverge.com | 0.851 |
| closed-30-macrumors-inline | [#30](https://github.com/buriy/python-readability/issues/30) | closed | www.macrumors.com | 0.996 |
| closed-49-guardian-invalid-link | [#49](https://github.com/buriy/python-readability/issues/49) | closed | www.theguardian.com | 0.935 |
| open-119-fiol-missing-sections | [#119](https://github.com/buriy/python-readability/issues/119) | open | www.fiolinjurylaw.com | 0.941 |
| open-170-blogger-inline | [#170](https://github.com/buriy/python-readability/issues/170) | open | negligeable.blogspot.com | 0.996 |
| open-171-cyberwire-sections | [#171](https://github.com/buriy/python-readability/issues/171) | open | thecyberwire.com | 0.942 |

Readability 0.9 preserves the inline `<i>` and `<b>` elements reported in #170
inside their surrounding paragraphs. The issue remains marked open in this
table because that is its GitHub state before the release.
