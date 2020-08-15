"""
    Small script to create a SFML Project

    Usage: See -help
    ---
    Open-Source @ github.com/davidp-ro/create-sfml-project
    ---
    MIT License | SFML License in res/SFML_LICENSE

    TODO: Using the 'target' config option select between -d or normal libs
"""

__author__ = 'David Pescariu'
__version__ = 1.0

import os, sys, platform, json

class Creator:
    """
    This class handles the creation of a new project

    Args:
        _name (str): Project name
        _path (str): Project path
    """
    def __init__(self, _name: str, _path: str) -> None:
        self.name = _name
        self.path = _path
        self.configs = {}

    def run_creator(self):
        self.__check_or_create_folder()
        self.__get_configs()
        self.__generate()

    def __check_or_create_folder(self):
        """
        Check if a folder exists already at the given path

        If it exists, sys.exit()
        If it doesn't, create it.
        """
        if os.path.exists(self.path):
            print("FAIL! Folder with same name already exists!")
            sys.exit()
        else:
            os.system(f"mkdir {self.path}")
            os.system(f"mkdir {self.path}\\bin")
            os.system(f"mkdir {self.path}\\obj")

    def __get_configs(self) -> None:
        """
        Read config file and load into [dict] configs
        """
        with open("config.json", "r") as conf:
            self.configs = json.load(conf)

    def __generate(self) -> None:
        """
        Generate the project
        """
        if self.configs["DUMP-CONFIG"] == True:
            print(self.configs)
        
        self.bat_file = f':: Made with create-sfml-project - Version {__version__} | Open-Source @ github.com/davidp-ro/create-sfml-project ::\n' \
                        f'g++ -Wall -g -std=c++14 -I "C:\\Program Files\\Python37\\include" -I{self.configs["SFML-PATH"]}\\include -c "{self.path}\\main.cpp" -o obj\\main.o\n' \
                        f'g++ -L{self.configs["SFML-PATH"]}\\lib -o bin\\{self.name}.exe obj\\main.o -lsfml-graphics-d -lsfml-window-d -lsfml-system-d\n' \
                        f'bin\\{self.name}.exe\n' \
                        'pause' if self.configs["PAUSE-CMD"] else ""

        self.binaries = [
            "openal32",
            "sfml-audio-2",
            "sfml-audio-d-2",
            "sfml-graphics-2",
            "sfml-graphics-d-2",
            "sfml-network-2",
            "sfml-network-d-2",
            "sfml-system-2",
            "sfml-system-d-2",
            "sfml-window-2",
            "sfml-window-d-2",
        ]

        self.sources = [
            "main.cpp",
        ]

        self.objs = [
            "main.o",
        ]

        # Write run.bat
        with open(f"{self.path}/run.bat", "w") as run_file:
            run_file.write(self.bat_file)

        # Get the correct copy command
        _copy = "copy" if platform.system() == "Windows" else "cp"

        # Copy sources
        for source in self.sources:
            __cmd = f"{_copy} res\\src\\{source} {self.path}\\{source}"
            os.system(__cmd)

        # Copy objs
        for obj in self.objs:
            __cmd = f"{_copy} res\\obj\\{obj} {self.path}\\obj\\{obj}"
            os.system(__cmd)

        # Copy libs
        for binary in self.binaries:
            __cmd = f"{_copy} res\\bin\\{binary}.dll {self.path}\\bin\\{binary}.dll"
            os.system(__cmd)

#------------------------------------------------------------------------------#

def main(args: list) -> None:
    _name, _path = args[0], args[1]
    creator = Creator(
        _name= _name,
        _path= _path,
    )

    creator.run_creator()

if __name__ == "__main__":
    def __show_help() -> None:
        help = "Create a SFML project\n" \
               "Args:\n" \
               "\tProject name -> the actual name of the project\n" \
               "\tPath -> the path where to create the project\n" \
               "Commands:\n" \
               "\t-help -> Show this page\n" \
               "\t-info -> Show some info about this script\n" \
               "Example:\n" \
               "\tcreate-sfml-project Example example-project\n" \
               "\tWill create a project named 'Example' in a folder named 'example-project'\n" \
               "\tcreate-sfml-project Example example-project\\ex\n" \
               "\tWill create a project named 'Example' in a folder named 'ex' (within the 'example-project' folder)"
        print(help, end="\n")

    def __show_info() -> None:
        print(f"Open-Source @ github.com/davidp-ro/create-sfml-project | Version {__version__}", end="\n")

    args = sys.argv
    _len = len(args)

    if _len <= 2:
        if "-help" in args:
            __show_help()
            sys.exit()

        if "-info" in args:
            __show_info()
            sys.exit()

        print("FAIL! Required arguments: Project name and Path, see -help")
        sys.exit()
    
    try:
        main(args[1:_len])
    except KeyboardInterrupt:
        print("Stopped by Keystroke")
