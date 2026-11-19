import sys
import os
import subprocess
import time

def run_job(action: str):
    """运行 dummy_job.py，传入 action 参数，返回 (exit_code, stdout, stderr)"""
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scripts_path = os.path.join(basedir, "examples", "dummy_job.py")

    cmd = [sys.executable,scripts_path,action]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1,
        )
        current_status = "success" if result.returncode == 0 else "failed"
        return {
            "action": action,
            "status":current_status,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "timed_out": False,
        }
    
    except subprocess.TimeoutExpired as e:
        return {
            "action": action,
            "status":"timeout",
            "exit_code": None,
            "stdout": "",
            "stderr":"",
            "timed_out": True,
        }

def run_with_retry(action,max_attempts):
    if max_attempts <= 0 :
        raise ValueError("max_attempts必须大于0")
    
    final_result = None

    for attempt in range(1,max_attempts+1):

        result = run_job(action)
        result["attempts"] = attempt
        final_result = result

        if result["status"] == "success":
            return result
        
        elif result["status"] == "failed":
            if attempt == max_attempts:
                return result
            else:
                print(f"遇到业务失败，进行第 {attempt+1} 次尝试...")
                time.sleep(1)

        elif result["status"] == "timeout":
            if attempt == max_attempts:
                print("重试次数用完")
                return result
            else:
                print(f"超时，准备进行{attempt + 1}次尝试")
                time.sleep(1)
    return final_result
        

if __name__ == "__main__":
    for action in ["success", "failure", "slow", "unknown"]:
        res = run_job(action)

        if res["timed_out"]:
            print(f"Action: {action}, Result: Timed out")
        else:
            print(f"Action: {action}, Exit Code: {res['exit_code']}, Stdout: {res['stdout']}, Stderr: {res['stderr']}")