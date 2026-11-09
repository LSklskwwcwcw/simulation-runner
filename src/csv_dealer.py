import csv
import os
import math


def csv_reader(csv_path:str) -> list[dict]:
    """读取 CSV，按 design.md 转换类型并校验。

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 某一行数据不合法
    """

    records: list[dict] = []

    if not csv_path.endswith(".csv"):
        raise ValueError(f"文件 {csv_path} 不是 CSV 文件")
    elif not os.path.exists(csv_path):
        raise FileNotFoundError(f"文件 {csv_path} 不存在")
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for rownum,row in enumerate(reader, start=2):
            for k,v in row.items():
                if v == "" or v is None:
                    raise ValueError(f"第 {rownum} 行数据不合法，字段 {k} 为空")
            try:
                task_id = int(row["task_id"])
                temperature = float(row["temperature_C"])
                value = float(row["parameter_value"])
            except ValueError as e:
                raise ValueError(f"第 {rownum} 行数据不合法，字段类型错误: {e}") from e
            
            if task_id <= 0:
                raise ValueError(f"第 {rownum} 行数据不合法，task_id {task_id} 小于 0")
            if not math.isfinite(temperature):
                raise ValueError(f"第 {rownum} 行数据不合法，temperature_C {temperature} 不是有限数")
            if value < 0 or value > 1:
                raise ValueError(f"第 {rownum} 行数据不合法，parameter_value {value} 不在 [0,1] 范围内")
            if not math.isfinite(value):
                raise ValueError(f"第 {rownum} 行数据不合法，parameter_value {value} 不是有限数")

            records.append({
                "task_id": task_id,
                "temperature_C": temperature,
                "parameter_value": value
            })

    return records
