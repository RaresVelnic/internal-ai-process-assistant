from internal_ai_process_assistant.tool_registry import list_tools


def test_list_tools_returns_registered_tools() -> None:
    tools = list_tools()

    tool_names = {tool.name for tool in tools}

    assert tool_names == {
        "list_available_files",
        "validate_input_file",
        "inspect_csv",
        "inspect_excel",
        "inspect_pdf",
        "extract_pdf_text",
        "search_pdf_text",
        "estimate_pdf_vector_retrieval",
        "search_pdf_by_vector",
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


def test_list_tools_describes_excel_inspection_parameters() -> None:
    tools = list_tools()
    excel_tool = next(tool for tool in tools if tool.name == "inspect_excel")

    assert excel_tool.parameters[0].name == "filename"
    assert excel_tool.parameters[0].allowed_values == ()


def test_list_tools_describes_pdf_inspection_parameters() -> None:
    tools = list_tools()
    pdf_tool = next(tool for tool in tools if tool.name == "inspect_pdf")

    assert pdf_tool.parameters[0].name == "filename"
    assert pdf_tool.parameters[0].allowed_values == ()


def test_list_tools_describes_pdf_text_extraction_parameters() -> None:
    tools = list_tools()
    pdf_text_tool = next(tool for tool in tools if tool.name == "extract_pdf_text")

    assert pdf_text_tool.parameters[0].name == "filename"
    assert pdf_text_tool.parameters[0].allowed_values == ()


def test_list_tools_describes_pdf_keyword_search_parameters() -> None:
    tools = list_tools()
    pdf_search_tool = next(tool for tool in tools if tool.name == "search_pdf_text")

    assert [parameter.name for parameter in pdf_search_tool.parameters] == ["filename", "query"]
    assert pdf_search_tool.parameters[0].allowed_values == ()
    assert pdf_search_tool.parameters[1].allowed_values == ()

def test_list_tools_describes_pdf_vector_search_parameters() -> None:
    tools = list_tools()
    pdf_search_tool = next(tool for tool in tools if tool.name == "search_pdf_by_vector")

    assert [parameter.name for parameter in pdf_search_tool.parameters] == ["filename", "query"]
    assert pdf_search_tool.parameters[0].allowed_values == ()
    assert pdf_search_tool.parameters[1].allowed_values == ()

def test_list_tools_describes_pdf_vector_estimate_parameters() -> None:
    tools = list_tools()
    estimate_tool = next(tool for tool in tools if tool.name == "estimate_pdf_vector_retrieval")

    assert [parameter.name for parameter in estimate_tool.parameters] == ["filename"]
    assert estimate_tool.parameters[0].allowed_values == ()

