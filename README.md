# CommandCompiler

A Python library for executing shell commands with enhanced features such as colorized output, error handling, and command management.

## Features

* Execute shell commands with proper error handling
* Colorized terminal output for better readability
* Context manager support for command execution
* Detailed command execution information (output, errors, return codes)
* Built-in delay option for command execution sequencing

## Installation



## Usage

### Basic Example

cd CommandCompiler

python -m pip install -e .

pip install -r requirements.txt

from command import Command

#Simple command executioncmd = Command("echo hello").run()
print(cmd.output)  # Prints: hello


### Using the Context Manager

from command import cmd

#Using the context manager

with cmd("echo hello")as command:

print(command.output)

print(f"Return code: {command.return_code}")


### Error Handling

from command import cmd, CommandError

try:

with cmd("non_existent_command")as command:

print(command.output)

except CommandError ase:

print(f"Command failed: {e}")


### Colorized Output


from command import viz

#Print colorized output

viz("This will be red by default",color="red")

viz("This will be green",color="green")

viz("This will be blue",color="blue")


## API Reference

### [Command](vscode-file://vscode-app/Applications/Visual%20Studio%20Code%20-%20Insiders.app/Contents/Resources/app/out/vs/code/electron-browser/workbench/workbench.html) Class

Main class for executing shell commands.

cmd=Command(command="ls -la",cwd="/path/to/dir",delay=1).run()


### [cmd](vscode-file://vscode-app/Applications/Visual%20Studio%20Code%20-%20Insiders.app/Contents/Resources/app/out/vs/code/electron-browser/workbench/workbench.html) Context Manager


with cmd("echo hello",cwd="/path/to/dir",delay=1)as command:

#work with command object


### Helper Functions

* [toterm(text, color)](vscode-file://vscode-app/Applications/Visual%20Studio%20Code%20-%20Insiders.app/Contents/Resources/app/out/vs/code/electron-browser/workbench/workbench.html): Format text with ANSI color
* [viz(*args, color=&#34;red&#34;)](vscode-file://vscode-app/Applications/Visual%20Studio%20Code%20-%20Insiders.app/Contents/Resources/app/out/vs/code/electron-browser/workbench/workbench.html): Print colorized output

## License

Copyright (c) 2025 Steven Kellum
Licensed under the Personal Use License v1.0.
See [LICENSE.txt](vscode-file://vscode-app/Applications/Visual%20Studio%20Code%20-%20Insiders.app/Contents/Resources/app/out/vs/code/electron-browser/workbench/workbench.html) for full terms. For commercial use, contact [sk@perfectatrifecta.com](vscode-file://vscode-app/Applications/Visual%20Studio%20Code%20-%20Insiders.app/Contents/Resources/app/out/vs/code/electron-browser/workbench/workbench.html)

## Requirements

* Python 3.13+
* colorama==0.4.6
