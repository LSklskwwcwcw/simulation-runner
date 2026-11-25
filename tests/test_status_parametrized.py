import pytest
import sys
import os
import subprocess
from unittest.mock import patch,MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.process_runner import run_job

@pytest.mark.parametrize("exit_code, is_timeout, expected_status", [
    (0, False, "success"),
    (1, False, "failed"),
    (2, False, "failed"),
    (None, True, "timeout")
])
@patch('src.process_runner.subprocess.run')
def test_run_job_status(mock_run,exit_code,is_timeout,expected_status):
    if is_timeout:
         mock_run.side_effect = subprocess.TimeoutExpired(cmd="dummy", timeout=1)
    else:
         mock_run.return_value = MagicMock(returncode=exit_code)

    result = run_job("test_action")

    assert result["status"] == expected_status