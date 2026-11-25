import pytest
import os
import json
import sys
from unittest.mock import patch


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import history_store


def test_history_tmp_path(tmp_path):
    test_file = tmp_path / "tmp_history.jsonl"

    with patch('src.history_store.filepath', str(test_file)):
        history_store.append_run_history({"msg": "hello pytest"})

        assert test_file.exists()

        with open(test_file,"r",encoding="utf-8") as f:
            data = json.loads(f.readlines()[0])
            assert data["msg"] == "hello pytest"