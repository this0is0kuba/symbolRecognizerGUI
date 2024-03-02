from sys import platform
import subprocess

if platform == "win32":
    subprocess.run("code", shell=True)

elif platform == "darwin" or platform == "linux":
    subprocess.run("code")