import argparse
import json
import re
from collections import Counter
from pathlib import Path

from lxml import html

from .readability import Document


TOKEN_RE = re.compile(r"\w+(?:['’]\w+)*", re.UNICODE)


def body_tokens(content):
    root = html.fromstring(content)
    for heading in root.xpath("//h1"):
        heading.drop_tree()
    text = " ".join(root.itertext()).lower()
    return TOKEN_RE.findall(text)


def calculate_metrics(overlap, actual_count, ideal_count):
    precision = overlap / actual_count
    recall = overlap / ideal_count
    f1 = 0.0 if overlap == 0 else 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def benchmark(pages_dir):
    fixtures = sorted(path.parent for path in pages_dir.rglob("metadata.json"))
    if not fixtures:
        raise ValueError("No benchmark fixtures found in {}".format(pages_dir))

    results = []
    for fixture in fixtures:
        metadata = json.loads((fixture / "metadata.json").read_text())
        summary = Document(
            (fixture / "page.html").read_bytes(),
            url=metadata["url"],
        ).summary()
        actual = body_tokens(summary)
        ideal = body_tokens((fixture / "ideal.html").read_text())
        if not actual or not ideal:
            raise ValueError("Empty benchmark body in {}".format(fixture.name))
        overlap = sum((Counter(actual) & Counter(ideal)).values())
        name = fixture.relative_to(pages_dir).as_posix()
        results.append((name, overlap, len(actual), len(ideal)))
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description="Benchmark article extraction quality")
    parser.add_argument("--pages", type=Path, default=Path("pages"))
    parser.add_argument("--min-score", type=float, default=0.95)
    args = parser.parse_args(argv)
    if not 0 <= args.min_score <= 1:
        parser.error("--min-score must be between 0 and 1")

    results = benchmark(args.pages)
    print("{:<34} {:>9} {:>9} {:>9}".format("PAGE", "PRECISION", "RECALL", "F1"))
    total_overlap = 0
    total_actual = 0
    total_ideal = 0
    for name, overlap, actual_count, ideal_count in results:
        precision, recall, f1 = calculate_metrics(
            overlap, actual_count, ideal_count
        )
        print("{:<34} {:>9.3f} {:>9.3f} {:>9.3f}".format(
            name, precision, recall, f1
        ))
        total_overlap += overlap
        total_actual += actual_count
        total_ideal += ideal_count

    precision, recall, f1 = calculate_metrics(
        total_overlap, total_actual, total_ideal
    )
    print("{:<34} {:>9.3f} {:>9.3f} {:>9.3f}".format(
        "TOTAL", precision, recall, f1
    ))
    if f1 < args.min_score:
        print(
            "WARNING: total F1 {:.3f} is below minimum {:.3f}".format(
                f1, args.min_score
            )
        )
        return 1
    print("PASS: total F1 {:.3f} meets minimum {:.3f}".format(
        f1, args.min_score
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
