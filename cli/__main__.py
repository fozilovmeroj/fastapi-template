import sys

from cli.commands import COMMANDS

def main():
    args = sys.argv[1:]

    if len(args) < 1:
        print("Please provide a command to run")
        sys.exit(0)

    command = args[0]
    if ":" in command:
        command, subcommand = command.split(":")
        COMMANDS[command][subcommand](*args[1:])
    else:
        COMMANDS[command](*args[1:])

if __name__ == "__main__":
    main()