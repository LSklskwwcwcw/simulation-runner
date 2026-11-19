import argparse
import sys
from result_store import save_run_result
from process_runner import run_with_retry


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

    parser.add_argument("--max--attempts",type=int,default=3,help="最大重试次数")

    args = parser.parse_args()
    try:
        result = run_with_retry(args.action,args.max_attempts)
        save_run_result(
            action  = result["action"],
            status  = result["status"],
            attempts = result["attempts"],
            exit_code = result["exit_code"],
            timed_out = result["timed_out"]
        )

        if result["status"] == "success":
            sys.exit(0)
        else: sys.exit(1)
    except ValueError as e:
        print(f"参数错误: {e}")
        sys.exit(1)




