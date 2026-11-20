import unittest
import tempfile
import json
import os
import sys
import uuid
from unittest.mock import patch


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import history_store

class TestHistoryStore(unittest.TestCase):
    def setUp(self):
        self.testdir = tempfile.TemporaryDirectory()

        self.test_filepath = os.path.join(self.testdir.name,"test_history.jsonl")

        self.patcher = patch('src.history_store.filepath', self.test_filepath)

        self.patcher.start()
    def tearDown(self):
        self.patcher.stop()
        self.testdir.cleanup()

    def test_append_and_read(self):
        record1 = {"action": "success", "job_id": "111"}
        record2 = {"action": "failure", "job_id": "222"}
    
        history_store.append_run_history(record1)
        history_store.append_run_history(record2)

        with open(self.test_filepath,"r",encoding="utf-8") as f:
            lines = f.readlines()

        self.assertEqual(len(lines),2)

        first_recorder = json.loads(lines[0])
        self.assertEqual(first_recorder["action"],"success")

    def test_job_id_unique(self):
        id1 = str(uuid.uuid4()) # 记得导入 uuid
        id2 = str(uuid.uuid4())
    
        history_store.append_run_history({"job_id": id1})
        history_store.append_run_history({"job_id": id2})

        with open(self.test_filepath,"r",encoding="utf-8") as f:
            lines = f.readlines()

        self.assertEqual(len(lines), 2)

        record1 = json.loads(lines[0])
        record2 = json.loads(lines[1])

        self.assertNotEqual(record1["job_id"],record2["job_id"])

    @patch('builtins.print')
    def test_invalid_json_rejected(self,mock_print):
        invalid_record = {"data": {1, 2, 3}}
        history_store.append_run_history(invalid_record)
        self.assertTrue(mock_print.called)
        with open(self.test_filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "") # 应该是空字符串

    @patch('builtins.print')
    def test_unwritable_path(self,mock_print):
        self.patcher.stop()
        self.patcher = patch('src.history_store.filepath', self.testdir.name)
        self.patcher.start()
        history_store.append_run_history({"action": "test"})
        printed_text = mock_print.call_args[0][0]
        self.assertIn("写入历史失败", printed_text)