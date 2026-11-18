import argparse
import sys
from result_store import save_run_result
from process_runner import run_job


def status_judge(timeout:bool,exit_code:int|None):
    if timeout is True:
        return "timeout"
    elif exit_code == 0:
        return "success"
    else:
        return "failed"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将内容存放为json")


    parser.add_argument("action",type=str,choices=["success", "failure", "slow", "unknown"],help="存为json")

    args = parser.parse_args()

    result = run_job(args.action)
    status = status_judge(result["timed_out"],result["exit_code"])
    save_run_result(
        action  = result["action"],
        status  = status,
        attempts = 1,
        exit_code = result["exit_code"],
        timed_out = result["timed_out"]
    )

    if status == "success":
        sys.exit(0)
    else: sys.exit(1)




