from internal_ai_process_assistant.tool_registry import list_tools


def test_list_tools_returns_file_listing_tool() -> None:
    tools = list_tools()

    assert len(tools) == 1
    assert tools[0].name == "list_available_files"
    assert tools[0].parameters[0].name == "area"
    assert tools[0].parameters[0].allowed_values == ("input", "workspace", "output")
