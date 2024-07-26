#! /usr/bin/python3

import src.utils as utils
import shutil,sys,os

PACKAGES = "./packages.json"
REPO = "https://github.com/shubhamkode/.dotfiles.git"
will_update_system: bool = False
HOME_DIR = os.path.expanduser("~")


def update_system():
    utils.sys_call(["sudo","apt","update"])
    utils.sys_call(["sudo","apt","upgrade" ,"-y"])


def install():
    packages = utils.read_json(PACKAGES)
    utils.install_apt_packages(packages["apt"])
    utils.install_snap_packages(packages["snap"])


def stow_config():
    os.chdir(HOME_DIR + "/.dotfiles")
    utils.sys_call(["stow",".","--adopt"])
    # utils.sys_call(["git","reset","--hard"])


def clone_repository():
    os.chdir(HOME_DIR)
    utils.sys_call(["git","clone",REPO,])

def set_system():
    utils.run("\tCloning Repository")(clone_repository)
    utils.run(f"\tStowing Configuration")(stow_config)

    # clone github repository
    # set fish as default shell
    fish_dir = shutil.which("fish")
    assert fish_dir != None, "Fish not installed"
    utils.sys_call(["chsh" ,"-s", fish_dir])

    # set kitty as default terminal
    # kitty_dir = shutil.which("kitty")
    # assert kitty_dir != None, "Kitty not installed"

def set_keyboard():
    utils.sys_call(["setxkbmap","-layout","us","-variant","dvorak"])



def app():
    global will_update_system
    
    step = 1
    utils.run(f"Step {step}: Setting Keyboard")(set_keyboard)

    if(will_update_system):
        utils.run(f"Step {(step:=step+1)}: Updating System")(update_system)

    utils.run(f"Step {(step:=step+1)}: Installing Packages")(install)
    utils.run(f"Step {(step:=step+1)}: Setting System")(set_system)
    print("Setup Completed\nRestart your session with i3.")



def main():
    global will_update_system

    argsList = sys.argv[1:]


    if("--no-update" in argsList):
        will_update_system = False
    else:
        will_update_system = True

    app()


if __name__ == "__main__":
    main()