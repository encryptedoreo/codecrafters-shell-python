import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        match command.split()[0]:
            case "exit": sys.exit(int(command.split()[1]))
            case "echo": sys.stdout.write(f"{' '.join(command.split()[1:])}\n")
            case "type": sys.stdout.write(
                f"{command.split()[1]} is a shell builtin\n"
                if command.split()[1] in {"exit", "echo", "type"}
                else f"{command.split()[1]}: not found\n"
            )
            case _: sys.stdout.write(f"{command.split()[0]}: command not found\n")


if __name__ == "__main__":
    main()
