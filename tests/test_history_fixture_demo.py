from src.history_store import append_run_history
import json
import pytest

RECORD_A = {"job_id": "001", "status": "success"}
INVALID = {"data": {1, 2, 3}}

def test_append_normal_record(history_file):
    append_run_history(RECORD_A,str(history_file))

    assert history_file.exists()
    with open(history_file,"r",encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 1
        assert RECORD_A == json.loads(lines[0])


def test_invalid_record_creates_no_file(history_file):
    with pytest.raises(TypeError):
        append_run_history(INVALID,str(history_file))

    assert not history_file.exists()