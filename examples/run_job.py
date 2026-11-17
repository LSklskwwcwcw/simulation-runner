import time 
import subprocess
import sys


def run_with_retry(action):
    max_retries = 3
    for i in range(max_retries):

        try:
            print(f"--- 第 {i+1} 次尝试执行 {action} ---")
            result = subprocess.run([sys.executable, "dummy_job.py", action],timeout=1, capture_output=True,text=True)
            if result.returncode == 0:
                print("success")
                break
            elif result.returncode != 0:
                raise ValueError("业务错误")

        except subprocess.TimeoutExpired:
            if i == max_retries - 1:
               print("重试次数已用完")
               return False
            else:
               print("超时准备重试")
               time.sleep(1)

run_with_retry("failure")