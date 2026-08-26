import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from readability import Document
from readability.benchmark import body_tokens, calculate_metrics, main


class TestBenchmark(unittest.TestCase):
    def make_fixture(self, root, ideal_text):
        fixture = root / "example"
        fixture.mkdir()
        article_text = "Reliable article content with punctuation. " * 20
        (fixture / "page.html").write_text(
            "<html><body><article><p>{}</p></article></body></html>".format(
                article_text
            )
        )
        (fixture / "ideal.html").write_text(
            "<article><p>{}</p></article>".format(ideal_text)
        )
        (fixture / "metadata.json").write_text(json.dumps({"url": "https://example.com"}))

    def test_passes_when_total_score_meets_threshold(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ideal_text = "Reliable article content with punctuation. " * 20
            self.make_fixture(root, ideal_text)

            output = io.StringIO()
            with redirect_stdout(output):
                result = main(["--pages", str(root), "--min-score", "0.95"])

        self.assertEqual(0, result)
        self.assertIn("TOTAL", output.getvalue())
        self.assertIn("PASS", output.getvalue())

    def test_warns_and_fails_when_total_score_is_too_low(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ideal_text = "Completely different expected words. " * 20
            self.make_fixture(root, ideal_text)

            output = io.StringIO()
            with redirect_stdout(output):
                result = main(["--pages", str(root), "--min-score", "0.95"])

        self.assertEqual(1, result)
        self.assertIn("WARNING", output.getvalue())

    def test_calculates_precision_recall_and_f1_from_counts(self):
        precision, recall, f1 = calculate_metrics(3, 4, 6)

        self.assertEqual(0.75, precision)
        self.assertEqual(0.5, recall)
        self.assertEqual(0.6, f1)

    def test_saved_summaries_match_current_extraction(self):
        pages = Path(__file__).parents[1] / "pages"
        fixtures = sorted(path.parent for path in pages.rglob("metadata.json"))

        self.assertEqual(166, len(fixtures))
        for fixture in fixtures:
            metadata = json.loads((fixture / "metadata.json").read_text())
            summary = Document(
                (fixture / "page.html").read_bytes(),
                url=metadata["url"],
            ).summary()
            self.assertEqual(
                body_tokens((fixture / "actual.html").read_text()),
                body_tokens(summary),
                fixture.name,
            )

    def test_corpus_contains_complete_mozilla_dataset(self):
        pages = Path(__file__).parents[1] / "pages"
        mozilla_fixtures = []
        commits = set()
        for metadata_path in pages.rglob("metadata.json"):
            metadata = json.loads(metadata_path.read_text())
            if "github.com/mozilla/readability" not in metadata.get("provenance", ""):
                continue
            mozilla_fixtures.append(metadata_path.parent.name)
            commits.add(metadata["upstream_commit"])

        self.assertEqual(130, len(mozilla_fixtures))
        self.assertEqual(
            {"ab4027a8b37669745016869a37a504727992b2ba"},
            commits,
        )

    def test_corpus_groups_have_expected_sizes(self):
        pages = Path(__file__).parents[1] / "pages"

        self.assertEqual(10, len(list((pages / "base").glob("*/metadata.json"))))
        self.assertEqual(20, len(list((pages / "dragnet").glob("*/metadata.json"))))
        self.assertEqual(6, len(list((pages / "user").glob("*/metadata.json"))))
        self.assertEqual(130, len(list((pages / "mozilla").glob("*/metadata.json"))))

    def test_dragnet_sample_has_fixed_provenance(self):
        pages = Path(__file__).parents[1] / "pages" / "dragnet"
        metadata = [
            json.loads(path.read_text())
            for path in pages.glob("*/metadata.json")
        ]

        self.assertEqual(20, len(metadata))
        self.assertEqual({"CC-BY-4.0"}, {item["data_license"] for item in metadata})
        self.assertEqual(
            {"5d97da4c3c5cf775fa02794b84d31786b8d51d3a"},
            {item["upstream_commit"] for item in metadata},
        )

    def test_jcharum_manual_ideal_and_regressions(self):
        pages = Path(__file__).parents[1] / "pages" / "jcharum"
        fixtures = sorted(path.parent for path in pages.glob("*/regression.json"))

        self.assertEqual(15, len(fixtures))
        for fixture in fixtures:
            metadata = json.loads((fixture / "regression.json").read_text())
            summary = Document(
                (fixture / "page.html").read_bytes(),
                url=metadata["url"],
            ).summary()
            self.assertTrue(metadata["quality_benchmark"])
            self.assertEqual("2026-08-23", metadata["manual_reviewed"])
            self.assertEqual(
                "manually reviewed from saved page.html and engine outputs",
                metadata["ideal_method"],
            )
            self.assertTrue(metadata["silver_reference"])
            self.assertEqual(
                "Mozilla Readability 0.6.0 with jsdom 26.1.0",
                metadata["silver_method"],
            )
            self.assertTrue(
                body_tokens(
                    (fixture / metadata["silver_summary_file"]).read_text()
                ),
                fixture.name,
            )
            self.assertEqual(
                "cec2d35c55cc8b94f0f6ff582cf700dab377af8a",
                metadata["upstream_commit"],
            )
            self.assertTrue(body_tokens((fixture / "ideal.html").read_text()))
            self.assertEqual(
                body_tokens((fixture / "actual.html").read_text()),
                body_tokens(summary),
                fixture.name,
            )
