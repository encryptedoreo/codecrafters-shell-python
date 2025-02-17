import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        match command.split()[0]:
            case "exit": exit(int(command.split()[1]))
            case _: sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
