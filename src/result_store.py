import json
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)


def save_run_result(action:str,status:str,attempts:int,exit_code:int|None,timed_out:bool):
    output_dir = os.path.join(ROOT_DIR, "outputs")
    filepath = os.path.join(output_dir, "run_result.json")

    
    os.makedirs(output_dir,exist_ok=True)

    result_data = {
        "action":action,
        "status":status,
        "attempts":attempts,
        "exit_code":exit_code,
        "timed_out":timed_out
    }

    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(result_data,f,indent=4)

    print(f"已成功保存至{filepath}")


save_run_result(action="success", status="success", attempts=1, exit_code=0, timed_out=False)