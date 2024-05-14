# How This Module Works

The `./routers` directory contains a series of tasks. Every file except `./routers/_logic.py` is in itself a task module, but the task modules all import that `_logic.py`. Each routine runs in its own thread. Good for concurrent s\*\*t.

Each task module `T` has a `T.arg_type` and an `T.obj_type`. Both classes derive from one of a series of base types.

Each object `obj` of `T.obj_type` has a property `obj.local_args` of type `T.arg_type`.

`T.arg_type` is a Python dataclass and carries, for example, the header:

```py
@dataclasses.dataclass
class _arg_type(logic.bin_ssl_arg_type):
```

The `logic.bin_ssl_arg_type` can be replaced with any other `arg_type` class (including `arg_type` itself) in `./routines/_logic`.

**To further clarify**, here's a non-functional skeleton for any modules in `./routines` you wish to add. The `{***}` are placed where you add stuff.

```py
import launcher.routines._logic as logic
import dataclasses
{***} # Any other potential imports.


@dataclasses.dataclass
class _arg_type(logic.{***}arg_type):
    {***} # Dataclass fields.


class obj_type(logic.{***}entry):
    local_args: _arg_type

    def process(self) -> None:
        {***} # The routine code.


class arg_type(_arg_type):
    obj_type = obj_type
```

# What Claude 3 Sonnet Would Say

Will correct over time. Don't take Claude's words as fact yet.

## `./downloader/_main.py`

This script is responsible for downloading the necessary files for the application. It takes input from the command line arguments, which specify the version of the application to download and the target directory for the downloaded files. The script achieves its purpose by utilizing the `download` module from the `routines` package. It first parses the command line arguments and then calls the `download` function from the `download` module, passing the parsed arguments as input. The `download` function handles the actual downloading process, and the script simply serves as an entry point for this functionality.

## `./routines/clear_appdata.py`

This script is designed to clear the application data directory, which typically contains user-specific data and settings. It does not take any input and does not produce any output directly. The script achieves its purpose by utilizing the `shutil` module from the Python standard library. It first determines the location of the application data directory based on the operating system, and then it uses the `shutil.rmtree` function to remove the entire directory and its contents recursively. This script is likely used as part of a larger application or routine to reset the application's state or clear user data.

## `./routines/download.py`

This script is responsible for downloading the necessary files for the application. It takes input in the form of command line arguments, which specify the version of the application to download and the target directory for the downloaded files. The script achieves its purpose by utilizing various Python modules, such as `requests` for making HTTP requests, `zipfile` for extracting downloaded ZIP archives, and `hashlib` for verifying the integrity of downloaded files. The script follows a logical flow: it first parses the command line arguments, then constructs the appropriate URLs for downloading the application files based on the specified version. It then downloads the files, verifies their integrity using checksums, and extracts the downloaded archives to the specified target directory.

## `./routines/player.py`

This script is likely responsible for launching or running the application in "player" mode. It does not take any direct input and does not produce any output. The script achieves its purpose by importing and executing specific functions or classes from other modules or packages within the application. Without seeing the actual code, it is difficult to provide more details about the logic or data transformations happening within this script.

## `./routines/rcc_server.py`

This script is likely responsible for starting or managing a server component of the application. It does not take any direct input and does not produce any output. The script achieves its purpose by importing and executing specific functions or classes from other modules or packages within the application. Without seeing the actual code, it is difficult to provide more details about the logic or data transformations happening within this script.

## `./routines/studio.py`

This script is likely responsible for launching or running the application in "studio" mode. It does not take any direct input and does not produce any output. The script achieves its purpose by importing and executing specific functions or classes from other modules or packages within the application. Without seeing the actual code, it is difficult to provide more details about the logic or data transformations happening within this script.

## `./routines/web_server.py`

This script is likely responsible for starting or managing a web server component of the application. It does not take any direct input and does not produce any output. The script achieves its purpose by importing and executing specific functions or classes from other modules or packages within the application. Without seeing the actual code, it is difficult to provide more details about the logic or data transformations happening within this script.

## `./routines/_logic.py`

This script likely contains shared logic or utility functions used by other scripts within the `routines` package. Without seeing the actual code, it is difficult to provide specific details about its purpose, inputs, outputs, or logic flows.

## `./subparsers/args_aux/clear_appdata.py`

This script is responsible for parsing command line arguments related to clearing the application data directory. It takes input from the command line arguments and produces a parsed argument object that can be used by other parts of the application. The script achieves its purpose by utilizing the `argparse` module from the Python standard library. It defines the expected command line arguments and their respective options or flags, and then parses the actual command line arguments provided by the user.

## `./subparsers/args_aux/download.py`

This script is responsible for parsing command line arguments related to downloading the application files. It takes input from the command line arguments and produces a parsed argument object that can be used by other parts of the application. The script achieves its purpose by utilizing the `argparse` module from the Python standard library. It defines the expected command line arguments and their respective options or flags, such as the version of the application to download and the target directory for the downloaded files. It then parses the actual command line arguments provided by the user.

## `./subparsers/args_aux/_logic.py`

This script likely contains shared logic or utility functions used by other scripts within the `args_aux` package for parsing command line arguments. Without seeing the actual code, it is difficult to provide specific details about its purpose, inputs, outputs, or logic flows.

## `./subparsers/args_launch_mode/download.py`

This script is responsible for parsing command line arguments related to launching the application in "download" mode. It takes input from the command line arguments and produces a parsed argument object that can be used by other parts of the application. The script achieves its purpose by utilizing the `argparse` module from the Python standard library. It defines the expected command line arguments and their respective options or flags specific to the "download" mode, and then parses the actual command line arguments provided by the user.

## `./subparsers/args_launch_mode/player.py`

This script is responsible for parsing command line arguments related to launching the application in "player" mode. It takes input from the command line arguments and produces a parsed argument object that can be used by other parts of the application. The script achieves its purpose by utilizing the `argparse` module from the Python standard library. It defines the expected command line arguments and their respective options or flags specific to the "player" mode, and then parses the actual command line arguments provided by the user.

## `./subparsers/args_launch_mode/server.py`

This script is responsible for parsing command line arguments related to launching the application in "server" mode. It takes input from the command line arguments and produces a parsed argument object that can be used by other parts of the application. The script achieves its purpose by utilizing the `argparse` module from the Python standard library. It defines the expected command line arguments and their respective options or flags specific to the "server" mode, and then parses the actual command line arguments provided by the user.

## `./subparsers/args_launch_mode/studio.py`

This script is responsible for parsing command line arguments related to launching the application in "studio" mode. It takes input from the command line arguments and produces a parsed argument object that can be used by other parts of the application. The script achieves its purpose by utilizing the `argparse` module from the Python standard library. It defines the expected command line arguments and their respective options or flags specific to the "studio" mode, and then parses the actual command line arguments provided by the user.

## `./subparsers/_logic.py`

This script likely contains shared logic or utility functions used by other scripts within the `subparsers` package for parsing command line arguments related to different launch modes. Without seeing the actual code, it is difficult to provide specific details about its purpose, inputs, outputs, or logic flows.

## `./_main.py`

This script is likely the main entry point for the application launcher. It takes input from the command line arguments, which specify the desired action or mode for the application (e.g., download, player, studio, server). The script achieves its purpose by utilizing the various subparsers and routines from the other modules and packages within the application. It first parses the command line arguments to determine the desired action or mode, and then it imports and executes the corresponding routines or scripts to perform that action or launch the application in the specified mode. The script serves as a central hub, coordinating the different components and functionalities of the application based on the user's input.
