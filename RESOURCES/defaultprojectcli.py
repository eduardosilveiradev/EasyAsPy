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
                compilestring = f"pyinstaller --onefile {__file__.replace('gid912/mngprjct.py', '')}"
                os.system(compilestring)
            except Exception as e:
                rio("error", f"Exception: {e}")
        case "run":
            runpath = grabpath("runner")
            print(runpath)
            os.system(f"python {runpath}")
        case _:
            rio("error", "Unknown command")


def grabinfo(args, project="gid912"):
    print(open("prjctinfo.log", "r").read())


"gid102"


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
