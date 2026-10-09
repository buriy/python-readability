import os
import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest


CONSOLE_SCRIPT = Path(sysconfig.get_path("scripts")) / (
    "readability-lxml.exe" if os.name == "nt" else "readability-lxml"
)


@pytest.mark.parametrize("command", [[sys.executable, "-m", "readability"], [str(CONSOLE_SCRIPT)]])
def test_package_command_line_help(command):
    result = subprocess.run(
        command + ["--help"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Usage:" in result.stdout
    assert result.stderr == ""


def test_console_script_reads_local_file(tmp_path):
    html = tmp_path / "article.html"
    html.write_text(
        "<html><head><title>Example article</title></head>"
        "<body><article><p>This is the article content.</p></article></body></html>",
        encoding="utf-8",
    )
    result = subprocess.run(
        [str(CONSOLE_SCRIPT), str(html)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Title:Example article" in result.stdout
    assert "This is the article content." in result.stdout
    assert result.stderr == ""
