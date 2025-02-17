import sys
import shutil
import os


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        match command.split():
            case ["exit", arg]: sys.exit(int(arg))
            case ["echo", *args]: sys.stdout.write(f"{' '.join(args)}\n")

            case ["type", arg] if arg in {"type", "exit", "echo"}: sys.stdout.write(f"{arg} is a shell builtin\n")
            case ["type", arg] if path := shutil.which(arg): sys.stdout.write(f"{arg} is {path}\n")
            case ["type", arg] if arg not in {"type", "exit", "echo"}: sys.stdout.write(f"{arg}: not found\n")

            case _: sys.stdout.write(f"{path := command.split()[0]}: command not found\n") if not os.path.isfile(path) else os.system(command)


if __name__ == "__main__":
    main()
