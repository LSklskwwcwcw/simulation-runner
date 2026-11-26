import pytest


@pytest.fixture
def history_file(tmp_path):
    return tmp_path / "history.jsonl"

