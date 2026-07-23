from internal_ai_process_assistant.app_info import get_app_name


def test_get_app_name() -> None:
    assert get_app_name() == "Internal AI Process Assistant"
