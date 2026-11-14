import sys
import os
import subprocess

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

        return {
            "action": action,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "timed_out": False,
        }
    
    except subprocess.TimeoutExpired as e:
        return {
            "action": action,
            "exit_code": None,
            "stdout": "",
            "stderr":"",
            "timed_out": True,
        }

if __name__ == "__main__":
    for action in ["success", "failure", "slow", "unknown"]:
        res = run_job(action)

        if res["timed_out"]:
            print(f"Action: {action}, Result: Timed out")
        else:
            print(f"Action: {action}, Exit Code: {res['exit_code']}, Stdout: {res['stdout']}, Stderr: {res['stderr']}")