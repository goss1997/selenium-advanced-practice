import subprocess, time

print("데이터 끄기")
subprocess.call("adb shell svc data disable", shell=True)

time.sleep(3)

print("데이터 켜기")
subprocess.call("adb shell svc data enable", shell=True)
