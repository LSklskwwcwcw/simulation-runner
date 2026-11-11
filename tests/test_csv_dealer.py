"""csv_reader 的单元测试。

运行方式（在项目根目录 simulation-runner/ 下）：
    python -m unittest discover -s tests -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

# src/ 不是包，把它加到 sys.path 才能 import csv_dealer
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from csv_dealer import csv_reader


HEADER = "task_id,temperature_C,parameter_value\n"


class CsvReaderTestBase(unittest.TestCase):
    """公共基类：每个测试方法都有独立的临时目录。

    注意类名不以 Test 开头，且没有 test_ 方法，unittest 不会把它当测试收集。
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self._tmpdir.name)

    def tearDown(self):
        self._tmpdir.cleanup()

    def _write_csv(self, content: str, name: str = "data.csv") -> str:
        """在临时目录写一个 CSV，返回路径字符串。"""
        path = self.tmpdir / name
        path.write_text(content, encoding="utf-8")
        return str(path)


class TestHappyPath(CsvReaderTestBase):
    """合法输入应当正常返回。"""

    def test_single_row_returns_one_record(self):
        path = self._write_csv(HEADER + "1,-10,0.25\n")

        records = csv_reader(path)

        self.assertEqual(len(records), 1)
        self.assertEqual(
            records[0],
            {"task_id": 1, "temperature_C": -10.0, "parameter_value": 0.25},
        )

    def test_multiple_rows_keep_file_order(self):
        path = self._write_csv(
            HEADER
            + "1,-10,0.25\n"
            + "2,-5,0.40\n"
            + "3,2,0.60\n"
        )

        records = csv_reader(path)

        self.assertEqual([r["task_id"] for r in records], [1, 2, 3])

    def test_converted_values_have_numeric_types(self):
        path = self._write_csv(HEADER + "1,-10,0.25\n")

        record = csv_reader(path)[0]

        self.assertIsInstance(record["task_id"], int)
        self.assertIsInstance(record["temperature_C"], float)
        self.assertIsInstance(record["parameter_value"], float)

    def test_accepts_plus_sign_and_scientific_notation(self):
        path = self._write_csv(HEADER + "1,+2.5,1e-3\n")

        record = csv_reader(path)[0]

        self.assertAlmostEqual(record["temperature_C"], 2.5)
        self.assertAlmostEqual(record["parameter_value"], 0.001)

    def test_accepts_parameter_value_boundaries(self):
        """design.md 写的是 [0,1]，0 和 1 都应当合法。"""
        path = self._write_csv(HEADER + "1,0,0\n2,0,1\n")

        records = csv_reader(path)

        self.assertEqual(records[0]["parameter_value"], 0.0)
        self.assertEqual(records[1]["parameter_value"], 1.0)


class TestFileValidation(CsvReaderTestBase):
    """文件层面的错误。"""

    def test_wrong_extension_raises(self):
        path = self._write_csv(HEADER + "1,0,0.5\n", name="data.txt")

        with self.assertRaisesRegex(ValueError, "不是 CSV 文件"):
            csv_reader(path)

    def test_missing_file_raises(self):
        missing = str(self.tmpdir / "nope.csv")

        with self.assertRaises(FileNotFoundError):
            csv_reader(missing)


class TestHeaderValidation(CsvReaderTestBase):
    """表头层面的错误。"""

    def test_duplicate_column_raises(self):
        path = self._write_csv(
            "task_id,task_id,temperature_C,parameter_value\n1,1,0,0.5\n"
        )

        with self.assertRaisesRegex(ValueError, "字段重复"):
            csv_reader(path)

    def test_missing_column_raises(self):
        path = self._write_csv("task_id,temperature_C\n1,0\n")

        with self.assertRaisesRegex(ValueError, "缺少字段"):
            csv_reader(path)

    def test_extra_column_raises(self):
        path = self._write_csv(
            "task_id,temperature_C,parameter_value,remark\n1,0,0.5,x\n"
        )

        with self.assertRaisesRegex(ValueError, "多余字段"):
            csv_reader(path)

    def test_missing_and_extra_columns_reported_together(self):
        path = self._write_csv("task_id,remark\n1,x\n")

        with self.assertRaises(ValueError) as ctx:
            csv_reader(path)

        message = str(ctx.exception)
        self.assertIn("缺少字段", message)
        self.assertIn("多余字段", message)

    def test_empty_file_raises(self):
        path = self._write_csv("")

        with self.assertRaises(ValueError):
            csv_reader(path)

    def test_header_only_raises(self):
        path = self._write_csv(HEADER)

        with self.assertRaisesRegex(ValueError, "没有数据行"):
            csv_reader(path)


class TestRowValidation(CsvReaderTestBase):
    """数据行层面的错误。"""

    def test_empty_cell_raises(self):
        path = self._write_csv(HEADER + "1,,0.5\n")

        with self.assertRaisesRegex(ValueError, "为空"):
            csv_reader(path)

    def test_non_numeric_task_id_raises(self):
        path = self._write_csv(HEADER + "abc,0,0.5\n")

        with self.assertRaisesRegex(ValueError, "task_id 格式错误"):
            csv_reader(path)

    def test_float_task_id_raises(self):
        path = self._write_csv(HEADER + "1.5,0,0.5\n")

        with self.assertRaisesRegex(ValueError, "task_id 格式错误"):
            csv_reader(path)

    def test_negative_task_id_format_raises(self):
        path = self._write_csv(HEADER + "-1,0,0.5\n")

        with self.assertRaisesRegex(ValueError, "task_id 格式错误"):
            csv_reader(path)

    def test_zero_task_id_raises(self):
        """'0' 能通过正则，但违反 > 0 的约束。"""
        path = self._write_csv(HEADER + "0,0,0.5\n")

        with self.assertRaises(ValueError):
            csv_reader(path)

    def test_duplicate_task_id_raises(self):
        path = self._write_csv(HEADER + "1,0,0.5\n1,3,0.6\n")

        with self.assertRaisesRegex(ValueError, "重复"):
            csv_reader(path)

    def test_non_numeric_temperature_raises(self):
        path = self._write_csv(HEADER + "1,abc,0.5\n")

        with self.assertRaisesRegex(ValueError, "temperature_C 格式错误"):
            csv_reader(path)

    def test_non_numeric_parameter_value_raises(self):
        path = self._write_csv(HEADER + "1,0,abc\n")

        with self.assertRaisesRegex(ValueError, "parameter_value 格式错误"):
            csv_reader(path)

    def test_infinite_temperature_raises(self):
        """1e400 能通过正则，但 float() 会溢出成 inf。"""
        path = self._write_csv(HEADER + "1,1e400,0.5\n")

        with self.assertRaisesRegex(ValueError, "不是有限数"):
            csv_reader(path)

    def test_infinite_parameter_value_raises(self):
        path = self._write_csv(HEADER + "1,0,1e400\n")

        with self.assertRaisesRegex(ValueError, "不是有限数"):
            csv_reader(path)

    def test_parameter_value_above_range_raises(self):
        path = self._write_csv(HEADER + "1,0,1.5\n")

        with self.assertRaisesRegex(ValueError, "不在"):
            csv_reader(path)

    def test_parameter_value_below_range_raises(self):
        path = self._write_csv(HEADER + "1,0,-0.1\n")

        with self.assertRaisesRegex(ValueError, "不在"):
            csv_reader(path)


if __name__ == "__main__":
    unittest.main()