import sys
import shutil
import os
import subprocess
import shlex


def main():
    builtins = {"type", "exit", "echo", "pwd", "cd"}

    while True:
        sys.stdout.write("$ ")
        command = sys.stdin.readline().strip()

        cmd = shlex.split(command.replace('1>', '>'), posix=True)
        stdout = sys.stdout if ">" not in command else open(cmd[-1], 'w')

        match cmd:
            case ["exit", arg]: sys.exit(int(arg))
            case ["exit"]: sys.exit(0)
            case ["echo", *args]: stdout.write(f"{' '.join(args)}\n")
            case ["type", arg] if arg in builtins: stdout.write(f"{arg} is a shell builtin\n")
            case ["type", arg] if path := shutil.which(arg): stdout.write(f"{arg} is {path}\n")
            case ["type", arg] if arg not in builtins: stdout.write(f"{arg}: not found\n")

            case ["pwd"]: sys.stdout.write(f"{os.getcwd()}\n")
            case ["cd", dir_path] if (path_exists := os.path.exists(expanded := os.path.expanduser(dir_path))): os.chdir(expanded)
            case ["cd", dir_path] if not path_exists: stdout.write(f"cd: {os.path.expanduser(dir_path)}: No such file or directory\n")

            case [fn, *args] if shutil.which(fn): stdout.write(subprocess.run(cmd, stdout=subprocess.PIPE, text=True).stdout.rstrip())
            case [fn, *args] if not shutil.which(fn): stdout.write(f"{fn}: command not found\n")
        
        if ">" in command:
            stdout.close()


if __name__ == "__main__":
    main()
