"""run_with_retry 的单元测试。

run_job 会真的起子进程、time.sleep 会真的等，所以全部用 mock 替换掉。
运行方式（在项目根目录 simulation-runner/ 下）：
    python -m unittest tests.test_retry -v
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from process_runner import run_with_retry


def make_result(status: str) -> dict:
    """造一份和 run_job 返回值同构的假数据。

    每次调用都返回新 dict，避免 mock 复用同一个对象被 run_with_retry 改动。
    """
    if status == "success":
        return {
            "action": "success",
            "status": "success",
            "exit_code": 0,
            "stdout": "job done",
            "stderr": "",
            "timed_out": False,
        }
    if status == "failed":
        return {
            "action": "failure",
            "status": "failed",
            "exit_code": 2,
            "stdout": "",
            "stderr": "Error: Job failed intentionally!",
            "timed_out": False,
        }
    return {
        "action": "slow",
        "status": "timeout",
        "exit_code": None,
        "stdout": "",
        "stderr": "",
        "timed_out": True,
    }


class TestRunWithRetry(unittest.TestCase):

    @patch("process_runner.run_job")
    def test_success_stops_immediately(self, mock_run_job):
        """首次就成功：只调用一次，后面的配额不该被消耗。"""
        mock_run_job.side_effect = lambda action: make_result("success")

        result = run_with_retry("success", max_attempts=5)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(mock_run_job.call_count, 1)
        mock_run_job.assert_called_once_with("success")

    @patch("process_runner.time.sleep")
    @patch("process_runner.run_job")
    def test_failure_exhausts_all_attempts(self, mock_run_job, mock_sleep):
        """一直失败：跑满配额，最后一次之后不再 sleep。"""
        mock_run_job.side_effect = lambda action: make_result("failed")

        result = run_with_retry("failure", max_attempts=3)

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["attempts"], 3)
        self.assertEqual(result["exit_code"], 2)
        self.assertEqual(mock_run_job.call_count, 3)
        # 3 次尝试之间只有 2 个间隔
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("process_runner.time.sleep")
    @patch("process_runner.run_job")
    def test_timeout_exhausts_all_attempts(self, mock_run_job, mock_sleep):
        """一直超时：跑满配额，结果保留 timed_out / exit_code=None。"""
        mock_run_job.side_effect = lambda action: make_result("timeout")

        result = run_with_retry("slow", max_attempts=3)

        self.assertEqual(result["status"], "timeout")
        self.assertIs(result["timed_out"], True)
        self.assertIsNone(result["exit_code"])
        self.assertEqual(result["attempts"], 3)
        self.assertEqual(mock_run_job.call_count, 3)

    @patch("process_runner.time.sleep")
    @patch("process_runner.run_job")
    def test_retry_recovers_after_failure(self, mock_run_job, mock_sleep):
        """失败两次后成功：证明重试真的有第二次机会，且成功后立即停。"""
        mock_run_job.side_effect = [
            make_result("failed"),
            make_result("failed"),
            make_result("success"),
        ]

        result = run_with_retry("failure", max_attempts=5)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["attempts"], 3)
        self.assertEqual(mock_run_job.call_count, 3)

    @patch("process_runner.time.sleep")
    @patch("process_runner.run_job")
    def test_retry_recovers_after_timeout(self, mock_run_job, mock_sleep):
        """超时一次后成功：说明超时也会触发重试。"""
        mock_run_job.side_effect = [
            make_result("timeout"),
            make_result("success"),
        ]

        result = run_with_retry("slow", max_attempts=3)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["attempts"], 2)
        self.assertEqual(mock_run_job.call_count, 2)

    @patch("process_runner.run_job")
    def test_invalid_max_attempts_raises(self, mock_run_job):
        """非法配额：抛 ValueError，且一次都不执行。"""
        with self.assertRaises(ValueError):
            run_with_retry("success", max_attempts=0)

        with self.assertRaises(ValueError):
            run_with_retry("success", max_attempts=-1)

        self.assertEqual(mock_run_job.call_count, 0)


if __name__ == "__main__":
    unittest.main()