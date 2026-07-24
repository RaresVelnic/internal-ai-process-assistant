import json
import subprocess
import sys
from pathlib import Path


def test_cli_lists_files_in_input(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.txt").write_text("hello", encoding="utf-8")

    completed_process = subprocess.run(
        [
            sys.executable,
            "-m",
            "internal_ai_process_assistant.cli",
            "list files in input",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed_process.stdout)

    assert completed_process.returncode == 0
    assert payload["status"] == "completed"
    assert payload["tool_name"] == "list_available_files"
    assert payload["result"]["files"][0]["name"] == "sample.txt"


def test_cli_returns_error_for_missing_request() -> None:
    completed_process = subprocess.run(
        [sys.executable, "-m", "internal_ai_process_assistant.cli"],
        check=False,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed_process.stdout)

    assert completed_process.returncode == 2
    assert payload["status"] == "error"
    assert "Usage:" in payload["message"]


def test_cli_returns_nonzero_for_unsupported_request(tmp_path: Path) -> None:
    completed_process = subprocess.run(
        [
            sys.executable,
            "-m",
            "internal_ai_process_assistant.cli",
            "delete files in input",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed_process.stdout)

    assert completed_process.returncode == 1
    assert payload["status"] == "unsupported_request"
