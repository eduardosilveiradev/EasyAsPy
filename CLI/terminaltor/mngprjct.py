import argparse
import os
import sys
from typing import Any
from colorama import Fore, Back, init

"""###################################################################################################################################################################################################################
WARNING: DO NOT MESS WITH THIS FILE IF BROKEN IT BREAKS YOUR PROJECT TOO
##################################################################################################"""
cls = lambda: os.system("cls" if os.name == "nt" else "clear")
init()

defaultpath = __file__.replace("mngprjct.py", "")


def grabpath(id):
    return defaultpath + f"RESOURCES\\{id}.py"


class Resources:
    def getresource(id) -> str:
        return open(grabpath(id), "r").read()


def parsermanager(args):
    match args.command:
        case "compile":
            try:
                compilestring = f"pyinstaller --onefile {__file__.replace('terminaltor/mngprjct.py', '')}"
                os.system(compilestring)
            except Exception as e:
                rio("error", f"Exception: {e}")
        case "run":
            runpath = grabpath("runner")
            print(runpath)
            os.system(f"python {runpath}")
        case _:
            rio("error", "Unknown command")


def grabinfo(args, project="terminaltor"):
    print(open("prjctinfo.log", "r").read())


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

    def __init__(self, message: str):
        super().__init__(message)



def main():
    cls()
    parser = argparse.ArgumentParser(description=f"Your project manager CLI")
    subparsers = parser.add_subparsers()

    manager = subparsers.add_parser("manage", help="Manage your project")
    manager.add_argument("command", help="Command to manage project")
    manager.set_defaults(func=parsermanager)

    info = subparsers.add_parser("info", help="Show info about the project")
    info.set_defaults(func=grabinfo)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
