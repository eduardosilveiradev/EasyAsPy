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
rprint("info", f"Found existing directories in project folder")
print("\n"+" Directories ".center(columns, "=")+f"\n{"\n".join(dirs.split("\\"))}")
print(" Directories ".center(columns, "=")+"\n")
rprint("info", "Locating 'main.py'...")
if os.path.exists("../gid912/main.py"):
    rprint("info", "Located 'main.py'")
else:
    rprint("error", "Could not find 'main.py'. Exiting...")
    exit()
run = input("Run(Y/n)? ")
match run.lower():
    case "y":
        cls()
        os.system("python ../gid912/main.py")
        print()
        rprint("info", "Process finished")
    case "n":
        cls()
        rprint("info", "Will not run")
        exit()
    case _:
        cls()
        raise UnknownOptionError("Unknown run option")
