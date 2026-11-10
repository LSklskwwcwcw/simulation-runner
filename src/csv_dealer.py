import csv
import os
import math
import re

_TASK_ID_RE = re.compile(r"\d+")
_FLOAT_RE   = re.compile(r"-?\d+(\.\d+)?")

def csv_reader(csv_path:str) -> list[dict]:
    """读取 CSV，按 design.md 转换类型并校验。

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 某一行数据不合法
    """

    records: list[dict] = []
    seen: dict[int,int] = {}

    if not csv_path.endswith(".csv"):
        raise ValueError(f"文件 {csv_path} 不是 CSV 文件")
    elif not os.path.exists(csv_path):
        raise FileNotFoundError(f"文件 {csv_path} 不存在")
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        #print(reader.fieldnames)
        EXPECTED = {"task_id", "temperature_C", "parameter_value"}
        got = set(reader.fieldnames or [])
        if len(got) != len(set(reader.fieldnames or [])):
            raise ValueError(f"CSV 文件 {csv_path} 字段不合法，字段重复")
        if got != EXPECTED:
            missing = EXPECTED - got
            extra = got - EXPECTED
            #print(got)
            #print(extra)
            len_missing = len(missing)
            #print(len_missing)
            len_extra = len(extra)
            #print(len_extra)
            if len_missing > 0 and len_extra <=0:
                raise ValueError(f"CSV 文件 {csv_path} 字段不合法，缺少字段 {missing}")
            elif len_missing <= 0 and len_extra > 0:
                raise ValueError(f"CSV 文件 {csv_path} 字段不合法，多余字段 {extra}")
            elif len_missing > 0 and len_extra > 0:
                raise ValueError(f"CSV 文件 {csv_path} 字段不合法，缺少字段 {missing}，多余字段 {extra}")
        #print(len(reader.fieldnames))
        #print(len(set(reader.fieldnames)))
        for rownum,row in enumerate(reader, start=2):
            for k,v in row.items():
                if v == "" or v is None:
                    raise ValueError(f"第 {rownum} 行数据不合法，字段 {k} 为空")
            if not _TASK_ID_RE.fullmatch(row["task_id"]):
                raise ValueError(f"第 {rownum} 行 task_id 格式错误: {row['task_id']!r}")
            if not _FLOAT_RE.fullmatch(row["temperature_C"]):
                raise ValueError(f"第 {rownum} 行 temperature_C 格式错误: {row['temperature_C']!r}")
            if not _FLOAT_RE.fullmatch(row["parameter_value"]):
                raise ValueError(f"第 {rownum} 行 parameter_value 格式错误: {row['parameter_value']!r}")
            try:
                task_id = int(row["task_id"])
                temperature = float(row["temperature_C"])
                value = float(row["parameter_value"])
            except ValueError as e:
                raise ValueError(f"第 {rownum} 行数据不合法，字段类型错误: {e}") from e

            if task_id in seen:
                raise ValueError(f"第 {rownum} 行数据不合法，task_id {task_id} 重复")
            seen[task_id] = rownum

            if task_id <= 0:
                raise ValueError(f"第 {rownum} 行数据不合法，task_id {task_id} 小于 0")
            if not math.isfinite(temperature):
                raise ValueError(f"第 {rownum} 行数据不合法，temperature_C {temperature} 不是有限数")
            if not math.isfinite(value):
                raise ValueError(f"第 {rownum} 行数据不合法，parameter_value {value} 不是有限数")
            if value < 0 or value > 1:
                raise ValueError(f"第 {rownum} 行数据不合法，parameter_value {value} 不在 [0,1] 范围内")

            records.append({
                "task_id": task_id,
                "temperature_C": temperature,
                "parameter_value": value
            })
    if not records:
        raise ValueError(f"CSV 文件 {csv_path} 没有数据行")
    return records
