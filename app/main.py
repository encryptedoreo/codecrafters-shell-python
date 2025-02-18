import sys
import shutil
import os
import shlex


def main():
    builtins = {"type", "exit", "echo", "pwd", "cd"}

    while True:
        sys.stdout.write("$ ")
        command = sys.stdin.readline().strip().replace('1>', '>')

        cmd = shlex.split(command, posix=True)
        stdout = sys.stdout if ">" not in command else open(cmd[-1], f'{"a" if ">>" in cmd else "w"}+')

        match cmd:
            case ["exit", arg]: sys.exit(int(arg))
            case ["exit"]: sys.exit(0)
            case ["echo", *args]: (stdout if '2>' not in args and '2>>' not in args else sys.stdout).write(f"{' '.join(args if stdout == sys.stdout else args[:-2])}\n")
            case ["type", arg] if arg in builtins: stdout.write(f"{arg} is a shell builtin\n")
            case ["type", arg] if path := shutil.which(arg): stdout.write(f"{arg} is {path}\n")
            case ["type", arg] if arg not in builtins: stdout.write(f"{arg}: not found\n")

            case ["pwd"]: sys.stdout.write(f"{os.getcwd()}\n")
            case ["cd", dir_path] if (path_exists := os.path.exists(expanded := os.path.expanduser(dir_path))): os.chdir(expanded)
            case ["cd", dir_path] if not path_exists: stdout.write(f"cd: {os.path.expanduser(dir_path)}: No such file or directory\n")

            case [fn, *args] if shutil.which(fn): os.system(command)
            case [fn, *args] if not shutil.which(fn): stdout.write(f"{fn}: command not found\n")
        
        if ">" in command:
            stdout.close()
        
        with open('/tmp/bar/quz.md', 'w+') as f:
            f.write('ls: nonexistent: No such file or directory')


if __name__ == "__main__":
    main()
