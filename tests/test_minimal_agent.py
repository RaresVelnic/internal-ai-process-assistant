from pathlib import Path

from internal_ai_process_assistant.minimal_agent import run_minimal_agent


def test_run_minimal_agent_lists_files_in_input(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text("name,value\nAlice,10\n", encoding="utf-8")

    response = run_minimal_agent("list files in input", tmp_path)

    assert response.status == "completed"
    assert response.tool_name == "list_available_files"
    assert response.result is not None
    assert response.result.area == "input"
    assert response.result.files[0].name == "sample.csv"


def test_run_minimal_agent_normalizes_request_text(tmp_path: Path) -> None:
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()

    response = run_minimal_agent("  LIST FILES IN WORKSPACE  ", tmp_path)

    assert response.status == "completed"
    assert response.result is not None
    assert response.result.area == "workspace"


def test_run_minimal_agent_rejects_unsupported_request(tmp_path: Path) -> None:
    response = run_minimal_agent("delete files in input", tmp_path)

    assert response.status == "unsupported_request"
    assert response.tool_name is None
    assert response.result is None
