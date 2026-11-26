import json
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
output_dir = os.path.join(ROOT_DIR, "outputs")
filepath = os.path.join(output_dir, "run_history.jsonl")


def append_run_history(record:dict,file_path:str |None = None):
    if file_path is None:
        file_path = filepath
    dirna = os.path.dirname(file_path)
    if dirna:
        os.makedirs(dirna, exist_ok=True)
    json_str = json.dumps(record,ensure_ascii=False) + "\n"
    with open(file_path,"a",encoding="utf-8") as f:
        f.write(json_str)


    return True