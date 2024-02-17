import argparse
import os
import sys
import json
import shutil
import inspect
import logging as lg
import loading
from pylogger import logdec, clear
from pylogger import init as initpylogger
from typing import Any
from colorama import Fore, Back, init
initpylogger(__file__.replace(r"\easyaspy.py", r"\logs\clilog.log"), "Main")
init()
cls = lambda: os.system("cls" if os.name == 'nt' else 'clear')
'''
This is an internal library DO NOT USE unless you want all your projects to break
'''

defaultpath = __file__.replace("CLI\\easyaspy.py", "")
clear(False)
@logdec
def grabPath(id):
  return defaultpath+f"RESOURCES\\{id}.py"

class Resources:
  def getresource(id) -> str:
    if "." not in [*id]:
      return open(grabPath(id), 'r').read()
    else:
      return open(os.path.join(defaultpath, "RESOURCES", id), 'r').read()

@logdec
def getPrjctInfo(folder):
  pyversion = ''
  vrsnlist = [*sys.version]
  for item in vrsnlist:
    if vrsnlist.index(item) <= 6:
      pyversion += item
    else:
      break
  return f"Project name: {folder}\nPython version: {pyversion}"

@logdec
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

def rprint(mode: str, content: str):
  match mode.lower():
    case "info":
      content = content.replace("\n", f"\n{Back.GREEN}{Fore.BLACK} INFO {Fore.RESET+Back.RESET} ")
      print(f"{Back.GREEN}{Fore.BLACK} INFO {Fore.RESET+Back.RESET} "+content)
      return
    case "error":
      content = content.replace("\n", f"\n{Back.RED}{Fore.BLACK} ERROR {Fore.RESET+Back.RESET} ")
      print(f"{Back.RED}{Fore.BLACK} ERROR {Fore.RESET+Back.RESET} "+content)
      return
    case "fault":
      content = content.replace("\n", f"\n{Back.YELLOW}{Fore.BLACK} FAULT {Fore.RESET+Back.RESET} ")
      print(f"{Back.YELLOW}{Fore.BLACK} FAULT {Fore.RESET+Back.RESET} "+content)
      return
    case _:
      raise UnknownOptionError("That rprint mode does not exist")

@logdec
def parsecfg(file) -> str:
  try:
    with open(file, 'r') as f:
      content = f.read()
  except OSError or FileNotFoundError:
    raise FileNotFoundError
  try:
    parsed = json.loads(content)
    return parsed
  except Exception as e:
    rprint("Error", "Exception: "+e)
 
@logdec
def install(lib: str, dest: str):
  path = sys.path
  path = path[5]
  try:
    shutil.copytree(os.path.join(path, lib), os.path.join(dest, "libraries", lib))
  except FileExistsError:
    return

@logdec
def newProject(args):
  parsedcfg = parsecfg(args.cfg)
  libs = ''
  libraries = []
  for i in parsedcfg["libraries"]:
    path = sys.path
    path = path[5]
    paths = os.listdir(path)
    for e  in paths:
      if e == i:
        rprint("info", "Found libary: "+e)
        libraries.append(e)
      else:
        continue
  for item in libraries:
    if not libraries.index(item) == len(libraries) - 1:
      libs += item+', '
    else:
      libs += item
  rprint("info", "Attempting to install collected libraries: "+libs)
  path = sys.path
  path = path[5]
  try:
    shutil.copytree(os.path.join(path, "pylogger"), os.path.join(args.folder, "libraries", "pylogger"))
  except FileExistsError:
    pass
  for item in libraries:
    if item not in os.listdir(args.folder+"/libraries") and args.r is None:
      install(item, args.folder)
      rprint("info", f"Installed library {item}")
    elif item in os.listdir(args.folder+"/libraries") and args.r is None:
      rprint("fault", f"Library {item} already installed. Skipping...\nRun 'python -m easyaspy new config.json {args.folder} -r' to reinstall libraries")
    else:
      install(item, args.folder)
      rprint("info", f"Reinstalled library {item}")
  try:
    os.mkdir(args.folder)
    createmsg = f"Project {args.folder} generated"
    rprint("info", createmsg)
  except FileExistsError:
    createmsg = f"Project {args.folder} regenerated"
    if not grabDefault("regen_project"):
      rprint("error", f"Project '{args.folder}' already exists. Regenerating will NOT clear project content")
      proceed = input(f"{Fore.BLACK+Back.BLUE} INPUT {Fore.RESET+Back.RESET} Proceed(Y/n/default)? ")
      match proceed.lower():
        case "y":
          rprint("info", createmsg)
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
            rprint("error", "Could not add default")
            return
          rprint("info", "Added default")
        case _:
          raise UnknownOptionError("Unknown option for project regeneration")
    else:
      rprint("info", createmsg)
  with open(args.folder+"/mngprjct.py", 't+w') as f:
    f.write(Resources.getresource("defaultprojectcli").replace("gid912", args.folder))
  with open(args.folder+"/prjctinfo.log", "t+w") as f:
    f.write(getPrjctInfo(args.folder))
  try:
    os.mkdir(os.path.join(args.folder, "resources"))
  except FileExistsError:
    pass
  with open(os.path.join(args.folder, "resources")+"\\runner.py", 't+w') as f:
    f.write(Resources.getresource("runner").replace("gid912", args.folder).replace('"gid102"', inspect.getsource(rprint)+"\n"+inspect.getsource(UnknownOptionError)))
  codeworkspace = input("Would you like a VS Code workspace(Y/n)? ")
  cls()
  match codeworkspace.lower():
    case "y":
      rprint("info", "Attempting Code workspace generation")
      with open(os.path.join(args.folder, "codeworkspace.code-workspace"), "t+w") as f:
        f.write(Resources.getresource("codeworkspace.code-workspace").replace("gid912", args.folder))
      rprint("info", "Completed workspace generation")
      exit()
    case "n":
      cls()
      rprint("info", "Will not generate")
      exit()
    case _:
      raise UnknownOptionError("Unknown option for VS Code workspace generation")

def deletePrjct(args):
  if os.path.exists(args.folder):
    os.remove(args.folder)
    rprint("info", f"Project {args.folder} deleted")
  else:
    rprint("error", f"Project {args.folder} does not exist")


def main():
  cls()
  parser = argparse.ArgumentParser(description='The official CLI for EasyAsPy')
  subparsers = parser.add_subparsers()

  create_parser = subparsers.add_parser('new', help='Create a new project')
  create_parser.add_argument('cfg', help='Config file for project in JSON format')
  create_parser.add_argument('folder', help='Folder for project')
  create_parser.add_argument('-r', nargs='?', const="all", help="Reinstall libraries from config", required=False)
  create_parser.set_defaults(func=newProject)

  delete_parser = subparsers.add_parser('delete', help='Delete an existing project')
  delete_parser.add_argument('folder', help='Name of the project to delete')
  delete_parser.set_defaults(func=deletePrjct)

  args = parser.parse_args()
  args.func(args)


if __name__ == "__main__":
  main()
