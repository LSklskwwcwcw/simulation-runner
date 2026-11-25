import pytest 
import os
import json
import sys
import tempfile
from unittest.mock import patch


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from src import history_store

def test_pytest_normal_record():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir,"pytest_history.jsonl")

        with patch('src.history_store.filepath', temp_file):
             history_store.append_run_history({"status": "success"})

             with open(temp_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

             assert len(lines) == 1
             data = json.loads(lines[0])
             assert data["status"] == "success"

def test_pytest_invalid_record():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, "pytest_history.jsonl")
        with patch('src.history_store.filepath', temp_file):
            with pytest.raises(TypeError):
                history_store.append_run_history({"data": {1, 2, 3}})
        