import argparse
import os
import random
import sys
import json
import shutil
import inspect
import stat
import logging as lg
import loading
import time
from pynput import keyboard
from pylogger import Logger
from typing import Any
import pyinputplus as pyip
from colorama import Fore, Back, init

mlg = Logger(__file__.replace(r"\easyaspy.py", r"\logs\clilog.log"), "Main")
init()
cls = lambda: os.system("cls" if os.name == "nt" else "clear")
"""
This is an internal library DO NOT MODIFY unless you want all your projects to break
"""

defaultpath = __file__.replace("CLI\\easyaspy.py", "")
mlg.clear("", False, False)


@mlg.logdec
def rmv_hdn_fl(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


@mlg.logdec
def grabPath(id):
    return defaultpath + f"RESOURCES\\{id}"


class Resources:
    def getresource(id) -> str:
        if "." not in [*id]:
            return open(grabPath(id), "r").read()
        else:
            return open(os.path.join(defaultpath, "RESOURCES", id), "r").read()


@mlg.logdec
def getPrjctInfo(folder):
    pyversion = ""
    vrsnlist = [*sys.version]
    for item in vrsnlist:
        if vrsnlist.index(item) <= 6:
            pyversion += item
        else:
            break
    return f"Project name: {folder} | Python version: {pyversion}"


@mlg.logdec
def grabDefault(id) -> bool:
    defaultfile = open("defaults.json", "r").read()
    defaultfile = json.loads(defaultfile)
    try:
        if id in defaultfile["defaults"]:
            return True
        return False
    except Exception:
        return False


class UnknownOptionError(NameError):
    if sys.version_info >= (3, 10):
        name: str

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)


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


@mlg.logdec
def parsecfg(file) -> str:
    try:
        with open(file, "r") as f:
            content = f.read()
    except OSError or FileNotFoundError:
        raise FileNotFoundError
    try:
        parsed = json.loads(content)
        return parsed
    except Exception as e:
        rio("Error", "Exception: " + e)


@mlg.logdec
def install(lib: str, dest: str):
    path = sys.path
    path = path[5]
    try:
        shutil.copytree(os.path.join(path, lib), os.path.join(dest, "libraries", lib))
    except FileExistsError:
        return


def _load(name, unit, pos):
    loader = loading.Loading(
        name,
        unit,
        pos,
    )
    for i in range(100):
        time.sleep(random.randint(0, 4) / 100)
        loader.prender(i)
    print("\n")


def load(name, dest=4096):
    path = sys.path
    path = path[5]
    path = f"{path}\\{dest}"
    _load(
        name,
        "bytes",
        4096 if dest == 4096 else os.stat(path).st_size,
    )


@mlg.logdec
def newProject(args):
    parsedcfg = parsecfg(args.cfg)
    libs = ""
    libraries = []
    alllibraries = []
    columns = shutil.get_terminal_size().columns

    print("╭" + " Confirm project info ".center(columns - 2, "─") + "╮")
    print(f"│{"".center(columns - 2)}│")
    print(f"│{f" Project name({args.folder}) ".center(columns - 2, " ")}│")
    print(f"│{f" Project config file({args.cfg}) ".center(columns - 2, " ")}│")
    print(
        f"│{f"Regenerate project({'True' if args.r == 'all' else 'False'})".center(
            columns - 2, " "
        )}│"
    )
    print(f"│{"".center(columns - 2)}│")
    print("╰" + "".center(columns - 2, "─") + "╯")
    print("\n")
    crctname = pyip.inputMenu(
        ["Confirm", f"Exit{Fore.LIGHTBLUE_EX}"],
        numbered=True,
        prompt=f"Choose{Fore.RESET}\n\n",
    )
    print(Fore.RESET)
    cls()
    match crctname.lower():
        case "confirm":
            pass
        case "exit":
            print("Exited")
            exit()
        case _:
            print("Invalid input")
            exit()
    for i in parsedcfg["libraries"]:
        path = sys.path
        path = path[5]
        paths = os.listdir(path)
        rio("info", "Found library: " + i)
        alllibraries.append(i)
        for e in paths:
            if e == i:
                libraries.append(e)
            else:
                continue
    print()
    _load("Parsing libraries", "libraries", len(alllibraries))
    for item in libraries:
        if not libraries.index(item) == len(libraries) - 1:
            libs += item + ", "
        else:
            libs += item
    rio("info", "Attempting to install collected libraries: " + libs)
    path = sys.path
    path = path[5]
    try:
        shutil.copytree(
            os.path.join(path, "pylogger"),
            os.path.join(args.folder, "libraries", "pylogger"),
        )
    except FileExistsError:
        pass
    rio(
        "info",
        "Note: Some libraries may be built-in to Python so they were not installed",
    )
    print()
    for item in libraries:
        load(f"Installing {item}", f"{item}\\__init__.py")
        if item not in os.listdir(args.folder + "/libraries") and args.r is None:
            install(item, args.folder)
        elif item in os.listdir(args.folder + "/libraries") and args.r is None:
            rio(
                "fault",
                f"Library {item} already installed. Skipping...\nRun 'python -m easyaspy new {args.cfg} {args.folder} -r' to reinstall libraries",
            )
        else:
            install(item, args.folder)
    rio("info", "Finished installing libraries")
    print()
    try:
        os.mkdir(args.folder)
    except FileExistsError:
        if not args.r:
            pass
    with open(args.folder + "/mngprjct.py", "t+w") as f:
        f.write(
            Resources.getresource("defaultprojectcli.py")
            .replace("gid912", args.folder)
            .replace(
                '"gid102"',
                inspect.getsource(rio) + "\n" + inspect.getsource(UnknownOptionError),
            )
        )
        _load(
            "Creating mngprjct.py",
            "bytes",
            os.stat(grabPath("defaultprojectcli.py")).st_size,
        )
    try:
        with open(os.path.join(args.folder, "main.py"), "w") as main_file:
            if not os.path.exists(os.path.join(args.folder, "main.py")):
                with open(os.path.join(args.folder, "main.py"), "w") as main_file:
                    main_file.write("")
    except FileExistsError:
        pass
    with open(args.folder + "/prjctinfo.log", "t+w") as f:
        f.write(getPrjctInfo(args.folder) + "\n\n" + open("logs/clilog.log").read())
        _load(
            "Creating prjctinfo.log",
            "bytes",
            f.tell(),
        )
    try:
        os.mkdir(os.path.join(args.folder, "resources"))
    except FileExistsError:
        pass
    with open(os.path.join(args.folder, "resources") + "\\runner.py", "t+w") as f:
        f.write(
            Resources.getresource("runner.py")
            .replace("gid912", args.folder)
            .replace(
                '"gid102"',
                inspect.getsource(rio) + "\n" + inspect.getsource(UnknownOptionError),
            )
        )
    _load(
        "Creating codeworkspace.code-workspace",
        "bytes",
        os.stat(grabPath("codeworkspace.code-workspace")).st_size,
    )
    with open(os.path.join(args.folder, "codeworkspace.code-workspace"), "t+w") as f:
        f.write(
            Resources.getresource("codeworkspace.code-workspace").replace(
                "gid912", args.folder
            )
        )
    rio("info", "Task completed")
    exit()


def deletePrjct(args):
    delete = rio("input", "Are you sure you want to delete(Y/n)? ")
    delete = delete.lower()
    if delete != "y":
        exit()
    delete = rio("input", "Are you really sure you want to delete(Y/n)? ")
    delete = delete.lower()
    if delete != "y":
        exit()
    while delete != args.folder:
        cls()
        delete = rio("input", f"Input your projects name({args.folder}) to delete: ")
        if delete != args.folder:
            rio("error", "Incorrect name try again")
            input()
    cls()
    if os.path.exists(args.folder):
        shutil.rmtree(args.folder, onerror=rmv_hdn_fl)
        rio("info", f"Project {args.folder} deleted")
    else:
        rio("error", f"Project {args.folder} was not found")
        rio("info", "Make sure you are executing the command in the correct path")


def main():
    cls()
    parser = argparse.ArgumentParser(description="The official CLI for EasyAsPy")
    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser("new", help="Create a new project")
    create_parser.add_argument("cfg", help="Config file for project in JSON format")
    create_parser.add_argument("folder", help="Folder for project")
    create_parser.add_argument(
        "-r",
        nargs="?",
        const="all",
        help="Reinstall libraries from config",
        required=False,
    )
    create_parser.set_defaults(func=newProject)

    delete_parser = subparsers.add_parser("delete", help="Delete an existing project")
    delete_parser.add_argument("folder", help="Name of the project to delete")
    delete_parser.set_defaults(func=deletePrjct)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
