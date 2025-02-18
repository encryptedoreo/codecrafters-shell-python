import sys
import shutil
import os
import subprocess
import shlex


def main():
    builtins = {"type", "exit", "echo", "pwd", "cd"}

    while True:
        sys.stdout.write("$ ")
        command = sys.stdin.readline().strip().replace('1>', '>')

        cmd = shlex.split(command, posix=True)
        stdout = sys.stdout if ">" not in command else open(cmd[-1], 'a')
        output = ''

        match cmd:
            case ["exit", arg]: sys.exit(int(arg))
            case ["exit"]: sys.exit(0)
            case ["echo", *args]: output += f"{' '.join(args)}\n"
            case ["type", arg] if arg in builtins: output += f"{arg} is a shell builtin\n"
            case ["type", arg] if path := shutil.which(arg): output += f"{arg} is {path}\n"
            case ["type", arg] if arg not in builtins: output += f"{arg}: not found\n"

            case ["pwd"]: output += f"{os.getcwd()}\n"
            case ["cd", dir_path] if (path_exists := os.path.exists(expanded := os.path.expanduser(dir_path))): os.chdir(expanded)
            case ["cd", dir_path] if not path_exists: output += f"cd: {os.path.expanduser(dir_path)}: No such file or directory\n"

            case [fn, *args] if shutil.which(fn): output += subprocess.check_output(cmd).rstrip()
            case [fn, *args] if not shutil.which(fn): output += f"{fn}: command not found\n"
        
        stdout.write(output)
        if ">" in command:
            stdout.close()


if __name__ == "__main__":
    main()
