from pathlib import Path

from internal_ai_process_assistant.tools.basic_report import generate_basic_report


def test_generate_basic_report_creates_markdown_report(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "sample.csv").write_text(
        "name,department,amount\n"
        "Alice,Finance,1200\n"
        "Bob,,850\n",
        encoding="utf-8",
    )

    result = generate_basic_report("sample.csv", tmp_path)

    report_path = tmp_path / "output" / "sample_report.md"

    assert result.source_filename == "sample.csv"
    assert result.report_filename == "sample_report.md"
    assert result.report_relative_path == "output/sample_report.md"
    assert report_path.exists()

    report_content = report_path.read_text(encoding="utf-8")

    assert "# Basic CSV Report: sample.csv" in report_content
    assert "- Rows: 2" in report_content
    assert "- Columns: 3" in report_content
    assert "- Column names: name, department, amount" in report_content
    assert "- department: 1" in report_content


def test_generate_basic_report_overwrites_existing_generated_report(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    (input_dir / "sample.csv").write_text(
        "name,amount\nAlice,10\n",
        encoding="utf-8",
    )
    (output_dir / "sample_report.md").write_text("old report", encoding="utf-8")

    generate_basic_report("sample.csv", tmp_path)

    report_content = (output_dir / "sample_report.md").read_text(encoding="utf-8")

    assert "old report" not in report_content
    assert "# Basic CSV Report: sample.csv" in report_content
