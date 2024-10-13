import os
import sys
import shutil
import time
from typing import Any
from colorama import Fore, Back, init

cls = lambda: os.system("cls" if os.name == "nt" else "clear")
columns = shutil.get_terminal_size().columns


"gid102"
_dirs = os.listdir("gid912")
_dirs.sort()
_dirs.pop(0)
_dirs.pop(0)
dirs = "\n"
for i in _dirs:
    dirs += f"{_dirs.index(i)+1}. " + i + "\\"
dirs.replace("__pycache__", "")

cls()
rio("info", f"Found existing directories in project folder")
parseddirs = dirs.split("\\")
for i in parseddirs:
    print(i)
rio("info", "Locating 'main.py'...")
if os.path.exists("gid912/main.py"):
    rio("info", "Located 'main.py'")
else:
    rio("error", "Could not find 'main.py'. Exiting...")
    exit()
rio("info", "Started program")
time.sleep(1.25)
os.system("python gid912/main.py")
print()
rio("info", "Process finished")
