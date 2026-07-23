"""Safe file listing tool for controlled project directories."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

ControlledArea = Literal["input", "workspace", "output"]
ALLOWED_AREAS = {"input", "workspace", "output"}


@dataclass(frozen=True)
class FileInfo:
    """Metadata for one directory entry."""

    name: str
    relative_path: str
    size_bytes: int
    is_file: bool


@dataclass(frozen=True)
class FileListResult:
    """Structured result returned by the file listing tool."""

    area: ControlledArea
    files: list[FileInfo]


def list_available_files(area: ControlledArea, project_root: Path) -> FileListResult:
    """List direct entries from a controlled project directory."""
    if area not in ALLOWED_AREAS:
        msg = f"Unsupported controlled area: {area}"
        raise ValueError(msg)

    target_dir = project_root / area

    if not target_dir.exists():
        return FileListResult(area=area, files=[])

    entries = []
    for path in sorted(target_dir.iterdir(), key=lambda item: item.name.lower()):
        if path.name == ".gitkeep":
            continue

        relative_path = path.relative_to(project_root).as_posix()
        entries.append(
            FileInfo(
                name=path.name,
                relative_path=relative_path,
                size_bytes=path.stat().st_size if path.is_file() else 0,
                is_file=path.is_file(),
            )
        )

    return FileListResult(area=area, files=entries)
