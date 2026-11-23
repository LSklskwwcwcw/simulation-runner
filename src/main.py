import argparse
import sys
import uuid
import datetime
from history_store import append_run_history
from result_store import save_run_result
from process_runner import run_with_retry



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将内容存放为json")


    parser.add_argument("action",type=str,choices=["success", "failure", "slow", "unknown"],help="存为json")

    parser.add_argument("--max--attempts",type=int,default=3,help="最大重试次数")

    args = parser.parse_args()
    try:
        result = run_with_retry(args.action,args.max_attempts)
        job_id = str(uuid.uuid4())
        timestamp_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

        result["job_id"] = job_id
        result["timestamp_utc"] = timestamp_utc
        save_run_result(
            action  = result["action"],
            status  = result["status"],
            attempts = result["attempts"],
            exit_code = result["exit_code"],
            timed_out = result["timed_out"]
        )

        history_saved = True
        try:
            append_run_history(result)
        except (TypeError,OSError) as e:
            history_saved = False
            print(f"历史记录保存失败，原因：{e}")

        if result["status"] == "success" and history_saved:
            sys.exit(0)
        else: sys.exit(1)
    except ValueError as e:
        print(f"参数错误: {e}")
        sys.exit(1)




