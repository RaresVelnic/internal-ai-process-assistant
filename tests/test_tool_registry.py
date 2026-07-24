from internal_ai_process_assistant.tool_registry import list_tools


def test_list_tools_returns_registered_tools() -> None:
    tools = list_tools()

    tool_names = {tool.name for tool in tools}

    assert tool_names == {"list_available_files", "inspect_csv"}


def test_list_tools_describes_file_listing_parameters() -> None:
    tools = list_tools()
    file_listing_tool = next(tool for tool in tools if tool.name == "list_available_files")

    assert file_listing_tool.parameters[0].name == "area"
    assert file_listing_tool.parameters[0].allowed_values == ("input", "workspace", "output")


def test_list_tools_describes_csv_inspection_parameters() -> None:
    tools = list_tools()
    csv_tool = next(tool for tool in tools if tool.name == "inspect_csv")

    assert csv_tool.parameters[0].name == "filename"
    assert csv_tool.parameters[0].allowed_values == ()
