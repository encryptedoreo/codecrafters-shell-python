import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        match command.split():
            case ["exit", arg]: sys.exit(int(arg))
            case ["echo", *args]: sys.stdout.write(f"{' '.join(args)}\n")
            case ["type", arg] if arg in {"type", "exit", "echo"}: sys.stdout.write(f"{arg} is a shell builtin\n")
            case _: sys.stdout.write(f"{command.split()[0]}: command not found\n")


if __name__ == "__main__":
    main()
