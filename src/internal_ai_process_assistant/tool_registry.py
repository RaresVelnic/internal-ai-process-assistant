"""Registry of safe tools available to the minimal agent."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolParameter:
    """Description of one tool parameter."""

    name: str
    description: str
    allowed_values: tuple[str, ...]


@dataclass(frozen=True)
class ToolDefinition:
    """Public metadata for one available tool."""

    name: str
    description: str
    parameters: tuple[ToolParameter, ...]


def list_tools() -> list[ToolDefinition]:
    """Return the safe tools available to the minimal agent."""
    return [
        ToolDefinition(
            name="list_available_files",
            description="List direct entries from a controlled project directory.",
            parameters=(
                ToolParameter(
                    name="area",
                    description="Controlled project area to inspect.",
                    allowed_values=("input", "workspace", "output"),
                ),
            ),
        )
    ]
