import argparse
import json
import re
import statistics
import subprocess
import time
from collections import Counter
from pathlib import Path

from lxml import html


TOKEN_RE = re.compile(r"\w+(?:['’]\w+)*", re.UNICODE)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def body_tokens(content):
    root = html.fromstring(content)
    for heading in root.xpath("//h1"):
        heading.drop_tree()
    return TOKEN_RE.findall(" ".join(root.itertext()).lower())


def metrics(overlap, actual_count, ideal_count):
    precision = 0.0 if actual_count == 0 else overlap / actual_count
    recall = overlap / ideal_count
    f1 = 0.0 if overlap == 0 else 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def read_source(path, engine):
    if engine == "readability":
        return path.read_bytes()
    return path.read_text()


def start_javascript_worker(script, environment):
    return subprocess.Popen(
        [
            "node",
            str(PROJECT_ROOT / "benchmarks" / script),
            str(environment.resolve()),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )


def extract_with_worker(worker, source, url):
    worker.stdin.write(json.dumps({"source": source, "url": url}) + "\n")
    worker.stdin.flush()
    response = json.loads(worker.stdout.readline())
    if "error" in response:
        raise RuntimeError(response["error"])
    return response["content"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "engine",
        choices=(
            "readability",
            "readability-js",
            "arc90",
            "defuddle",
            "postlight",
            "trafilatura",
            "goose",
            "justext",
            "newspaper",
        ),
    )
    parser.add_argument("version")
    parser.add_argument("output", type=Path)
    parser.add_argument("--readability-js-env", type=Path)
    parser.add_argument("--arc90-env", type=Path)
    parser.add_argument("--defuddle-env", type=Path)
    parser.add_argument("--postlight-env", type=Path)
    parser.add_argument("--metadata-name", default="metadata.json")
    parser.add_argument("--ideal-name", default="ideal.html")
    parser.add_argument("--save-output-name")
    args = parser.parse_args()

    worker = None
    if args.engine == "readability":
        from readability import Document

        def extract(source, url):
            return Document(source, url=url).summary()
    elif args.engine == "readability-js":
        if args.readability_js_env is None:
            parser.error("--readability-js-env is required for readability-js")
        worker = start_javascript_worker(
            "readability_js.mjs", args.readability_js_env
        )

        def extract(source, url):
            return extract_with_worker(worker, source, url)
    elif args.engine == "arc90":
        if args.arc90_env is None:
            parser.error("--arc90-env is required for arc90")
        worker = start_javascript_worker("arc90_js.mjs", args.arc90_env)

        def extract(source, url):
            return extract_with_worker(worker, source, url)
    elif args.engine == "defuddle":
        if args.defuddle_env is None:
            parser.error("--defuddle-env is required for defuddle")
        worker = start_javascript_worker("defuddle_js.mjs", args.defuddle_env)

        def extract(source, url):
            return extract_with_worker(worker, source, url)
    elif args.engine == "postlight":
        if args.postlight_env is None:
            parser.error("--postlight-env is required for postlight")
        worker = start_javascript_worker("postlight_js.mjs", args.postlight_env)

        def extract(source, url):
            return extract_with_worker(worker, source, url)
    elif args.engine == "trafilatura":
        from trafilatura import extract as trafilatura_extract

        def extract(source, url):
            return trafilatura_extract(
                source,
                url=url,
                output_format="html",
                include_comments=False,
                include_links=True,
                include_tables=True,
            )
    elif args.engine == "goose":
        from goose3 import Goose
        from goose3.configuration import Configuration

        configuration = Configuration()
        configuration.enable_image_fetching = False
        goose = Goose(configuration)

        def extract(source, url):
            return goose.extract(raw_html=source, url=url).cleaned_text
    elif args.engine == "justext":
        import justext

        stoplist = justext.get_stoplist("English")

        def extract(source, url):
            paragraphs = justext.justext(source, stoplist)
            return "\n".join(
                paragraph.text
                for paragraph in paragraphs
                if not paragraph.is_boilerplate
            )
    else:
        from newspaper import Article, Config

        configuration = Config()
        configuration.fetch_images = False

        def extract(source, url):
            article = Article(url, config=configuration)
            article.download(input_html=source)
            article.parse()
            return article.text

    root = PROJECT_ROOT / "pages"
    rows = []
    failures = []
    fixtures = sorted(path.parent for path in root.rglob(args.metadata_name))
    for fixture in fixtures:
        metadata = json.loads((fixture / args.metadata_name).read_text())
        source = read_source(fixture / "page.html", args.engine)
        started = time.perf_counter()
        try:
            summary = extract(source, metadata["url"])
            elapsed = time.perf_counter() - started
            if not summary:
                raise ValueError("empty extraction")
            if args.save_output_name is not None:
                (fixture / args.save_output_name).write_text(summary)
            actual = body_tokens(summary)
            ideal = body_tokens((fixture / args.ideal_name).read_text())
            if not actual or not ideal:
                raise ValueError("empty token set")
            overlap = sum((Counter(actual) & Counter(ideal)).values())
            precision, recall, f1 = metrics(overlap, len(actual), len(ideal))
            rows.append({
                "name": fixture.relative_to(root).as_posix(),
                "group": fixture.relative_to(root).parts[0],
                "overlap": overlap,
                "actual": len(actual),
                "ideal": len(ideal),
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "seconds": elapsed,
            })
        except Exception as error:
            elapsed = time.perf_counter() - started
            ideal = body_tokens((fixture / args.ideal_name).read_text())
            rows.append({
                "name": fixture.relative_to(root).as_posix(),
                "group": fixture.relative_to(root).parts[0],
                "overlap": 0,
                "actual": 0,
                "ideal": len(ideal),
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0,
                "seconds": elapsed,
            })
            failures.append({
                "name": fixture.relative_to(root).as_posix(),
                "error": repr(error),
            })

    if worker is not None:
        worker.stdin.close()
        return_code = worker.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, worker.args)

    overlap = sum(row["overlap"] for row in rows)
    actual = sum(row["actual"] for row in rows)
    ideal = sum(row["ideal"] for row in rows)
    precision, recall, f1 = metrics(overlap, actual, ideal)
    group_totals = {}
    for group in sorted({row["group"] for row in rows}):
        group_rows = [row for row in rows if row["group"] == group]
        group_overlap = sum(row["overlap"] for row in group_rows)
        group_actual = sum(row["actual"] for row in group_rows)
        group_ideal = sum(row["ideal"] for row in group_rows)
        group_precision, group_recall, group_f1 = metrics(
            group_overlap, group_actual, group_ideal
        )
        group_totals[group] = {
            "pages": len(group_rows),
            "precision": group_precision,
            "recall": group_recall,
            "f1": group_f1,
        }

    output = {
        "engine": args.engine,
        "version": args.version,
        "rows": rows,
        "failures": failures,
        "groups": group_totals,
        "totals": {
            "pages": len(rows),
            "overlap": overlap,
            "actual": actual,
            "ideal": ideal,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "median_seconds": statistics.median(row["seconds"] for row in rows),
            "total_seconds": sum(row["seconds"] for row in rows),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output["totals"], indent=2))
    print("failures", failures)


if __name__ == "__main__":
    main()
