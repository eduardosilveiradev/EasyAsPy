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
    crctname = input(f"Project name is '{args.folder}' is this correct(Y/n)? ")
    match crctname.lower():
        case "y":
            pass
        case "n":
            print("Closing")
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

    try:
        os.mkdir(args.folder)
    except FileExistsError:
        createmsg = f"Project {args.folder} regenerated"
        if not grabDefault("regen_project"):
            rio(
                "error",
                f"Project '{args.folder}' already exists. Regenerating will NOT clear project content",
            )
            proceed = input(
                f"{Fore.BLACK+Back.BLUE} INPUT {Fore.RESET+Back.RESET} Proceed(Y/n/default)? "
            )
            match proceed.lower():
                case "y":
                    rio("info", createmsg)
                case "n":
                    exit()
                case "default":
                    try:
                        with open("defaults.json", "r") as f:
                            parsed = json.loads(f.read())
                        parsed["defaults"].append("regen_project")
                        with open("defaults.json", "w") as f:
                            f.write(json.dumps(parsed))
                    except OSError or FileNotFoundError:
                        rio("error", "Could not add default")
                        return
                    rio("info", "Added default")
                case _:
                    raise UnknownOptionError("Unknown option for project regeneration")
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
    load("Creating codeworkspace.code-workspace")
    with open(os.path.join(args.folder, "codeworkspace.code-workspace"), "t+w") as f:
        f.write(
            Resources.getresource("codeworkspace.code-workspace").replace(
                "gid912", args.folder
            )
        )
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
        delete = rio("input", "Input your projects name to delete: ")
        if delete != args.folder:
            rio("error", "Incorrect name try again")
            input()
    cls()
    if os.path.exists(args.folder):
        shutil.rmtree(args.folder, onerror=rmv_hdn_fl)
        rio("info", f"Project {args.folder} deleted")
    else:
        rio("error", f"Project {args.folder} does not exist")


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
