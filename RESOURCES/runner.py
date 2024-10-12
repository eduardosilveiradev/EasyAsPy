import os
import sys
import shutil
from typing import Any
from colorama import Fore, Back, init

cls = lambda: os.system("cls" if os.name == "nt" else "clear")
columns = shutil.get_terminal_size().columns


"gid102"
_dirs = os.listdir("../gid912")
_dirs.sort()
dirs = "\n"
for i in _dirs:
    dirs += f"{_dirs.index(i)+1}. " + i + "\\"

cls()
rio("info", f"Found existing directories in project folder")
parseddirs = dirs.split("\\")
for i in parseddirs:
    print(i)
rio("info", "Locating 'main.py'...")
if os.path.exists("../gid912/main.py"):
    rio("info", "Located 'main.py'")
else:
    rio("error", "Could not find 'main.py'. Exiting...")
    exit()
run = input("Run(Y/n)? ")
match run.lower():
    case "y":
        cls()
        os.system("python ../gid912/main.py")
        print()
        rio("info", "Process finished")
    case "n":
        cls()
        rio("info", "Will not run")
        exit()
    case _:
        cls()
        raise UnknownOptionError("Unknown run option")
