import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        match command.split()[0]:
            case "exit": sys.exit(int(command.split()[1]))
            case "echo": sys.stdout.write(f"{' '.join(command.split()[1:])}\n")
            case _: sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
