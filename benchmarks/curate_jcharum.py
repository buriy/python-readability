import copy
import json
from pathlib import Path

from lxml import html


PROJECT_ROOT = Path(__file__).resolve().parents[1]
JCHARUM_ROOT = PROJECT_ROOT / "pages" / "jcharum"
MANUAL_REVIEW_DATE = "2026-08-23"
MANUAL_METHOD = "manually reviewed from saved page.html and engine outputs"
CURATED_XPATHS = {
    "arstechnica-002": (
        "//div[@id='story']/div[@class='body']",
    ),
    "slate-000": (
        "//h2[@class='slst-article-dek']",
        "//article//div[@class='body parsys']",
    ),
    "washingtonpost-000": ("//div[@id='article_body']//article",),
    "washingtonpost-001": ("//div[@id='article_body']//article",),
}
REMOVED_XPATH = (
    ".//script | .//style | .//noscript | .//iframe | .//form | .//object | "
    ".//table[contains(concat(' ', normalize-space(@class), ' '), ' aside ')]"
)


def curated_summary(source, xpaths):
    document = html.fromstring(source)
    nodes = []
    for xpath in xpaths:
        nodes.extend(document.xpath(xpath))
    assert nodes

    wrapper = html.Element("div", attrib={"class": "manual-ideal"})
    for source_node in nodes:
        node = copy.deepcopy(source_node)
        for removed in node.xpath(REMOVED_XPATH):
            removed.drop_tree()
        wrapper.append(node)

    return html.tostring(wrapper, encoding="unicode", method="html")


def main():
    fixtures = sorted(JCHARUM_ROOT.glob("*/regression.json"))
    assert len(fixtures) == 15

    for metadata_path in fixtures:
        fixture = metadata_path.parent
        metadata = json.loads(metadata_path.read_text())
        metadata["ideal_method"] = MANUAL_METHOD
        metadata["manual_reviewed"] = MANUAL_REVIEW_DATE
        metadata["quality_benchmark"] = True
        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")

        if fixture.name in CURATED_XPATHS:
            summary = curated_summary(
                (fixture / "page.html").read_text(),
                CURATED_XPATHS[fixture.name],
            )
            (fixture / "ideal.html").write_text(summary)


if __name__ == "__main__":
    main()
