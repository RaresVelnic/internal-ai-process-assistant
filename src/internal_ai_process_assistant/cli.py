"""Command line interface for the minimal Phase 1 agent."""

from dataclasses import asdict
from pathlib import Path
import json
import sys

from internal_ai_process_assistant.minimal_agent import run_minimal_agent


def main() -> int:
    """Run the minimal agent from the command line."""
    if len(sys.argv) != 2:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": "Usage: python -m internal_ai_process_assistant.cli '<request>'",
                },
                indent=2,
            )
        )
        return 2

    response = run_minimal_agent(request=sys.argv[1], project_root=Path.cwd())
    print(json.dumps(asdict(response), indent=2))
    return 0 if response.status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
