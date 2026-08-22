import subprocess
import sys


def test_package_command_line_help():
    result = subprocess.run(
        [sys.executable, "-m", "readability", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Usage:" in result.stdout
    assert result.stderr == ""
