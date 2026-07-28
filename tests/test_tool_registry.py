from internal_ai_process_assistant.tool_registry import list_tools


def test_list_tools_returns_registered_tools() -> None:
    tools = list_tools()

    tool_names = {tool.name for tool in tools}

    assert tool_names == {
        "list_available_files",
        "validate_input_file",
        "inspect_csv",
        "generate_basic_report",
    }


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


def test_list_tools_describes_basic_report_parameters() -> None:
    tools = list_tools()
    report_tool = next(tool for tool in tools if tool.name == "generate_basic_report")

    assert report_tool.parameters[0].name == "filename"
    assert report_tool.parameters[0].allowed_values == ()


def test_list_tools_describes_input_file_validation_parameters() -> None:
    tools = list_tools()
    validation_tool = next(tool for tool in tools if tool.name == "validate_input_file")

    assert validation_tool.parameters[0].name == "filename"
    assert validation_tool.parameters[0].allowed_values == ()
