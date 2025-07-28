
from __future__ import annotations
import os
import sys

from pathlib import Path
from typing import TYPE_CHECKING

import ujson as json


sys.path.append(str(Path(__file__).absolute().parent))
if TYPE_CHECKING:
    import typing

import shlex
import subprocess as sp

from time import sleep

from colorama import Back, Fore, Style


CURRENT_DIR = Path.cwd().absolute()

def toterm(x, color:str="red"):
    if color == "red":
        return Fore.RED + Style.BRIGHT + x + Style.RESET_ALL
    if color == "blue":
        return Fore.BLUE + Style.BRIGHT + x + Style.RESET_ALL
    if color == "green":
        return Fore.GREEN + Style.BRIGHT + x + Style.RESET_ALL
    if color == "yellow":
        return Fore.YELLOW + Style.BRIGHT + x + Style.RESET_ALL
    if color == "magenta":
        return Fore.MAGENTA + Style.BRIGHT + x + Style.RESET_ALL
    if color == "cyan":
        return Fore.CYAN + Style.BRIGHT + x + Style.RESET_ALL
    if color == "white":
        return Fore.WHITE + Style.BRIGHT + x + Style.RESET_ALL
    return Fore.BLACK + Style.BRIGHT + x + Style.RESET_ALL


class CommandError(Exception):
    """Custom exception for command errors."""

    def __init__(self,cmd: str | None = None, errcode:int | None = None, *args,**kwds):
        super().__init__(*args)
        self.error_code = errcode
        self.command = cmd
        self.message = f"Command '{self.command}' failed with error: {self.error_code} {args[0] if args else ''}\n {' '.join(f"{k}={v}" for k, v in kwds.items())}" if args else f"Command '{self.command}' failed with error: {self.error_code}"
        self.args = args

    def __str__(self):
        return f"CommandError: {self.message}"

    def __iter__(self):
        """Iterate over the error message."""
        args = self.command, self.error_code, self.args, self.message
        yield from args
    def __repr__(self):
        """Return a string representation of the error."""
        return f"CommandError(command={self.command!r}, message={self.message!r}, args={self.args!r})"
class Command:
    def __init__(self, command: str, cwd: Path | str | None = None):
        self.command = command
        self.text = command.strip()
        self.cwd = Path(cwd).absolute() if cwd else CURRENT_DIR
        self.args = shlex.split(self.command.strip())
        self.name = self.args[0]
        self.error_code = 0
        self.error = None

    def __str__(self):
        return self.text
    def __repr__(self):
        return f"Command(command={self.command!r}, cwd={self.cwd!r})"
    def __iter__(self):
        """Iterate over the command attributes."""
        yield self.command
        yield self.cwd
        yield self.text
        yield self.args
        yield self.name
        yield self.error_code
        yield self.error

    def __get__(self, instance, owner):
        """Get the command text."""
        return self.text

    def __set__(self, instance, value):
        """Set the command text."""
        if isinstance(value, str):
            self.command = value
            self.text = value.strip()
            self.args = shlex.split(self.text)
            self.name = self.args[0]
        else:
            raise ValueError("Command must be a string.")
        self.error_code = 0
        self.error = None

    def __enter__(self):
        """Enter the command context."""
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the command context."""
        if exc_type is not None:
            self.error_code = 1
            self.error = exc_value
            print(toterm(f"Command '{self.command}' failed with error: {exc_value}", "red"))
        return False


    def __call__(self, *args, **kwargs):
        with self:
            extra_args = list(args) + [f"{k}={v}" for k, v in kwargs.items()]
            full_cmd = self.args + list(map(str, extra_args))
            return self.run(full_cmd)

    def run(self, args=None) -> int | str:
        if args is None:
            args = self.args
        try:
            proc = sp.run(
                args, check=True, capture_output=True, cwd=self.cwd, text=True
            )
            proc.check_returncode()

        except sp.CalledProcessError as e:
            print(toterm(f"Command failed: {e}"))
            self.error_code = e.returncode
            self.error = e
            raise CommandError(self.text, e.returncode, error=self.error) from e
        except FileNotFoundError as e:
            self.error_code = e.errno
            self.error = e
            print(toterm(f"Command Failed: {self.text}"), f"File not found: {e}")
            raise CommandError(
                self.text,
                e.errno,
                filename=e.filename,
                other_filename=e.filename2,
                error=self.error,
            ) from e
        except Exception as e:
            self.error_code = 1
            self.error = e
            print(toterm(f"An error occurred: {e}"))
            raise CommandError(self.text, 1, error=self.error) from e
        else:
            if proc and proc.stderr:
                print(toterm(f"Command stderr: {proc.stderr.strip()}", "yellow"))
            if proc and proc.returncode == 0:
                print(toterm(f"Command succeeded: {self.text}", "blue"))
                return proc.stdout.strip()
            self.error_code = proc.returncode if proc else 69
            self.error = f"Command Error: {self.text} did not complete successfully."
            raise CommandError(
                self.text,
                self.error_code,
                toterm(f"Command failed with return code: {self.error_code}", "red"),
                error=self.error,
            )


        finally:
            sleep(1)  # Give some time for the command to complete

def cmd(command: str | Command, cwd: str | Path | None = None) -> int | str:
    """Run a shell command."""
    proc = None
    cwd = Path(cwd).absolute() if cwd else CURRENT_DIR
    command = Command(command=command, cwd=cwd) if isinstance(command, str) else command

    try:
        with command as com:
            proc = com.run()
            if isinstance(proc, int):
                if proc != 0:
                    print(toterm(f"Command failed with return code: {proc}", "red"))
                    raise CommandError(com.text, proc, error=com.error)
            elif isinstance(proc, str):
                if proc:
                    print(toterm(f"Command output: {proc}", "green"))
                else:
                    print(toterm("Command executed successfully with no output.", "blue"))
            return proc
    except CommandError as e:
        print(toterm(f"Command Error: {e.message}", "red"))
        if e.error_code == 1:
            print(toterm("Command failed. Please check the command and try again.", "yellow"))
        raise e

def main(args:str | list[str]=""):
    if isinstance(args, list | tuple):
        args = " ".join(shlex.quote(arg) for arg in args)
    return cmd(args)


if __name__ == "__main__":
    try:
        output = main(sys.argv[1:])
        if isinstance(output, str):
            print(output)
    except Exception:
        sys.exit(1)
