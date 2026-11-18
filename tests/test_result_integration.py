"""集成测试：验证 main.py 端到端写入的 JSON 与真实运行结果一致。

运行方式（在项目根目录 simulation-runner/ 下）：
    python -m unittest tests.test_result_integration -v
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
MAIN_PY = SRC_DIR / "main.py"
RESULT_JSON = PROJECT_ROOT / "outputs" / "run_result.json"

# src/ 不是包，加进 sys.path 才能 import main
sys.path.insert(0, str(SRC_DIR))

from main import status_judge


class TestRunIntegration(unittest.TestCase):
    """把 main.py 当黑盒跑起来，检查它写出的 JSON。"""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self._tmpdir.name)

        # 备份真实的输出文件，避免测试污染工作区
        self._backup = None
        if RESULT_JSON.exists():
            self._backup = self.tmpdir / "run_result.json.bak"
            shutil.move(str(RESULT_JSON), str(self._backup))

    def tearDown(self):
        # 先删掉测试产生的文件，再把备份还原回去
        if RESULT_JSON.exists():
            RESULT_JSON.unlink()
        if self._backup is not None:
            shutil.move(str(self._backup), str(RESULT_JSON))
        self._tmpdir.cleanup()

    def _run_main(self, action: str) -> subprocess.CompletedProcess:
        """以子进程运行 main.py，返回 CompletedProcess。"""
        return subprocess.run(
            [sys.executable, str(MAIN_PY), action],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=10,
        )

    def _read_result(self) -> dict:
        """读取 main.py 写出的 JSON。"""
        with open(RESULT_JSON, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_success_writes_success_status(self):
        proc = self._run_main("success")
        data = self._read_result()

        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["exit_code"], 0)
        self.assertIs(data["timed_out"], False)

    def test_failure_exit_code_two_is_not_success(self):
        """验收点：退出码 2 必须记为 failed，不能算成功。"""
        proc = self._run_main("failure")
        data = self._read_result()

        self.assertEqual(proc.returncode, 1)
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["exit_code"], 2)
        self.assertIs(data["timed_out"], False)

    def test_slow_is_recorded_as_timeout(self):
        proc = self._run_main("slow")
        data = self._read_result()

        self.assertEqual(proc.returncode, 1)
        self.assertEqual(data["status"], "timeout")
        self.assertIsNone(data["exit_code"])
        self.assertIs(data["timed_out"], True)

    def test_import_result_store_has_no_side_effect(self):
        """在没有输出文件的环境里导入 result_store，不应产生文件。

        必须用子进程：本进程可能早已 import 过 result_store，
        再次 import 只会命中 sys.modules 缓存，不会重新执行模块。
        """
        self.assertFalse(RESULT_JSON.exists(), "前置条件：此时不应有输出文件")

        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC_DIR) + os.pathsep + env.get("PYTHONPATH", "")

        proc = subprocess.run(
            [sys.executable, "-c", "import result_store"],
            cwd=str(self.tmpdir),
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # 导入本身必须成功，否则"没有副作用"这个结论不成立
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertFalse(RESULT_JSON.exists(), "导入模块不应创建工作文件")


class TestStatusJudge(unittest.TestCase):
    """status_judge 是纯函数，直接测映射规则。"""

    def test_timeout_wins_over_exit_code(self):
        """超时优先：即使 exit_code 是 0 也应判为 timeout。"""
        self.assertEqual(status_judge(True, None), "timeout")
        self.assertEqual(status_judge(True, 0), "timeout")

    def test_exit_code_zero_is_success(self):
        self.assertEqual(status_judge(False, 0), "success")

    def test_nonzero_exit_code_is_failed(self):
        self.assertEqual(status_judge(False, 2), "failed")
        self.assertEqual(status_judge(False, 1), "failed")


if __name__ == "__main__":
    unittest.main()