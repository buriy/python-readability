from benchmarks.compare import metrics, read_source


def test_empty_extraction_metrics():
    assert metrics(0, 0, 10) == (0.0, 0.0, 0.0)


def test_readability_source_preserves_original_bytes(tmp_path):
    source = tmp_path / "page.html"
    source.write_bytes(b"<p>caf\xe9</p>")

    assert read_source(source, "readability") == b"<p>caf\xe9</p>"
