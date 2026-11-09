import argparse
from csv_dealer import csv_reader
import sys







if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="读取 CSV 文件并打印内容")

    parser.add_argument("csv_path", type=str, help="CSV 文件路径")

    args = parser.parse_args()

    try:
        records = csv_reader(args.csv_path)
        print("CSV 文件内容:")
        for record in records:
            print(record)
    except FileNotFoundError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)



