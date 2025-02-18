import sys
import shutil
import os
import shlex


def main():
    while True:
        sys.stdout.write("$ ")
        command = sys.stdin.readline().strip()

        match shlex.split(command):
            case ["exit", arg]: sys.exit(int(arg))
            case ["echo", *args]: sys.stdout.write(f"{' '.join(args).strip('\'"')}\n")
            case ["type", arg] if arg in {"type", "exit", "echo", "pwd", "cd"}: sys.stdout.write(f"{arg} is a shell builtin\n")
            case ["type", arg] if path := shutil.which(arg): sys.stdout.write(f"{arg} is {path}\n")
            case ["type", arg] if arg not in {"type", "exit", "echo"}: sys.stdout.write(f"{arg}: not found\n")

            case ["pwd"]: sys.stdout.write(f"{os.getcwd()}\n")
            case ["cd", dir_path] if (path_exists := os.path.exists(expanded := os.path.expanduser(dir_path))): os.chdir(expanded)
            case ["cd", dir_path] if not path_exists: sys.stdout.write(f"cd: {os.path.expanduser(dir_path)}: No such file or directory\n")

            case [fn, *args] if shutil.which(fn.strip('\'"')): os.system(command)
            case [fn, *args] if not shutil.which(fn.strip('\'"')): sys.stdout.write(f"{fn}: command not found\n")


if __name__ == "__main__":
    main()
