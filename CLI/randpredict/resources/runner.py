import os
import sys
import shutil
from typing import Any
from colorama import Fore, Back, init

cls = lambda: os.system("cls" if os.name == "nt" else "clear")
columns = shutil.get_terminal_size().columns


def rio(mode: str, content: str):
    match mode.lower():
        case "info":
            content = content.replace(
                "\n", f"\n{Back.GREEN}{Fore.BLACK} INFO {Fore.RESET+Back.RESET} "
            )
            print(f"{Back.GREEN}{Fore.BLACK} INFO {Fore.RESET+Back.RESET} " + content)
            return
        case "error":
            content = content.replace(
                "\n", f"\n{Back.RED}{Fore.BLACK} ERROR {Fore.RESET+Back.RESET} "
            )
            print(f"{Back.RED}{Fore.BLACK} ERROR {Fore.RESET+Back.RESET} " + content)
            return
        case "fault":
            content = content.replace(
                "\n", f"\n{Back.YELLOW}{Fore.BLACK} FAULT {Fore.RESET+Back.RESET} "
            )
            print(f"{Back.YELLOW}{Fore.BLACK} FAULT {Fore.RESET+Back.RESET} " + content)
            return
        case "input":
            return input(
                f"{Back.YELLOW+Fore.BLACK} INPUT {Back.RESET+Fore.RESET} {content}"
            )
        case _:
            raise UnknownOptionError("That rio mode does not exist")

class UnknownOptionError(NameError):
    if sys.version_info >= (3, 10):
        name: str

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)

_dirs = os.listdir("../randpredict")
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
if os.path.exists("../randpredict/main.py"):
    rio("info", "Located 'main.py'")
else:
    rio("error", "Could not find 'main.py'. Exiting...")
    exit()
run = input("Run(Y/n)? ")
match run.lower():
    case "y":
        cls()
        os.system("python ../randpredict/main.py")
        print()
        rio("info", "Process finished")
    case "n":
        cls()
        rio("info", "Will not run")
        exit()
    case _:
        cls()
        raise UnknownOptionError("Unknown run option")
