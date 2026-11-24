import unittest
import os
import tempfile
import json
import sys
from unittest.mock import patch
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
from src import history_store
class TestHistoryErrors(unittest.TestCase):
    def setUp(self):
        self.testdir = tempfile.TemporaryDirectory()
        self.test_filepath = os.path.join(self.testdir.name,"test_err.json1")

        self.patcher = patch('src.history_store.filepath', self.test_filepath)
        self.patcher.start()
    def tearDown(self):
        self.patcher.stop()
        self.testdir.cleanup()

    def test_write_read(self):
        record = {"status": "success"}
        history_store.append_run_history(record)
        with open(self.test_filepath,"r",encoding="utf-8") as f:
            lines = f.readlines()
        first_recorder = json.loads(lines[0])
        self.assertEqual(first_recorder["status"],"success")

    def test_set_error(self):
        invalid_record = {"data": {1, 2, 3}}
        with self.assertRaises(TypeError):
            history_store.append_run_history(invalid_record)

    @patch('builtins.open', side_effect=OSError("模拟磁盘写满"))
    def test_write_error(self,mock_open):
        history_saved = True
        try:
            history_store.append_run_history({"action":"test"})
        except OSError:
            history_saved = False

        self.assertFalse(history_saved)

    def test_file_content_unchanged_on_serialization_error(self):
        history_store.append_run_history({"status": "success"})
        with open(self.test_filepath,"r",encoding="utf-8") as f:
            original_content = f.read()
        invalid_record = {"data": {1, 2, 3}}
        with self.assertRaises(TypeError):
            history_store.append_run_history(invalid_record)

        with open(self.test_filepath,"r",encoding="utf-8") as f:
            new_content = f.read()

        self.assertEqual(original_content,new_content)

    def test_write_method_raises_oserror(self):
        mock_file = MagicMock()

        mock_file.write.side_effect = OSError("模拟写入磁盘时失败")

        mock_file.__enter__.return_value = mock_file 
        
        history_saved = True

        with patch('builtins.open', return_value=mock_file):
            try:
                history_store.append_run_history({"action": "test"})
            except OSError:
                history_saved = False

        self.assertFalse(history_saved)