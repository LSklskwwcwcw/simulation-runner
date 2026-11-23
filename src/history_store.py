import json
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
output_dir = os.path.join(ROOT_DIR, "outputs")
filepath = os.path.join(output_dir, "run_history.jsonl")


def append_run_history(record:dict):

    os.makedirs(output_dir, exist_ok=True)
    with open(filepath,"a",encoding="utf-8") as f:
        json_str = json.dumps(record,ensure_ascii=False) + "\n"
        f.write(json_str)


    return True