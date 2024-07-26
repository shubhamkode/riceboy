import subprocess
import json

def run(msg: str): # type: ignore
    def wrapper(fn): # type: ignore
        print(msg)
        fn()

    return wrapper # type: ignore


def sys_call(command: list[str]):
    # subprocess.run(command,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    try:
        subprocess.run(command)
    except:
        print(f"ERROR while running: {command.append(' ')}")
        exit(1)

def read_json(path: str):
    with open(path) as f:
        return json.load(f)

def install_snap_packages(packages:dict[str,list[str]]):
    command = ["sudo","snap","install"]


    for package in packages["common"]: 
        sys_call(command + [package])
    for package in packages["classic"]:
        sys_call(command+[package,"--classic"])



def install_apt_packages(packages:list[str]):
    command = ["sudo","apt","install"]
    command.extend(packages)
    command.append("-y")
    sys_call(command)



