import sys
import time

def main():
    if len(sys.argv) < 2:
        print("参数错误")
        sys.exit(1)
    
    action = sys.argv[1]
    if action == "success":
        print("job done")
        sys.exit(0)

    elif action == "failure":
        sys.stderr.write("Error: Job failed intentionally!\n") 
        sys.exit(2)

    elif action == "slow":
        print("job sleeping...")
        time.sleep(3)
        print("job sleep done")
        sys.exit(0)

    else:
        print(f"未知的 action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
