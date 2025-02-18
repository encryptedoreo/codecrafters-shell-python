import os
import sys
import termios
from pathlib import Path
from subprocess import run
from shlex import split
from contextlib import suppress
from functools import cache


class Shell:
    def __init__(self):
        self.builtins = {
            "echo": self.handle_echo,
            "type": self.handle_type,
            "exit": self.handle_exit,
            "pwd": self.handle_pwd,
            "cd": self.handle_cd,
        }
        self.paths = [Path(p) for p in os.getenv("PATH", "").split(":")]
        self._executables = None

    def run(self):
        while True:
            try:
                self.prompt()
                command = self.get_input()
                if not command.strip():
                    continue
                cmd_parts = split(command)
                cmd_parts, stdout, stderr = self.parse_redirects(cmd_parts)
                self.execute_command(cmd_parts, stdout, stderr)
            except KeyboardInterrupt:
                sys.exit(0)

    def prompt(self):
        sys.stdout.write("$ ")
        sys.stdout.flush()

    def get_input(self):
        command = ""
        tab_count = 0

        while True:
            ch = self.readchar()
            if ord(ch) == 9:  # Tab key
                tab_count += 1
                matches, completion = self.complete(command)
                self.handle_tab_completion(tab_count, matches, completion, command)
            elif ord(ch) == 10:  # Enter key
                sys.stdout.write("\n")
                return command
            else:
                tab_count = 0
                sys.stdout.write(ch)
                command += ch
            sys.stdout.flush()

    def complete(self, prefix):
        matches = set()
        # Check builtins
        for cmd in self.builtins:
            if cmd.startswith(prefix):
                matches.add(cmd)
        # Check executables
        for exe in self.get_executables():
            if exe.startswith(prefix):
                matches.add(exe)
        if not matches:
            return [], ""
        # Find longest common prefix
        matches = sorted(matches)
        max_len = len(prefix)
        while True:
            try:
                chars = {m[max_len] for m in matches if len(m) > max_len}
                if len(chars) != 1:
                    break
                max_len += 1
            except IndexError:
                break
        return matches, matches[0][:max_len]

    @cache
    def get_executables(self):
        executables = []
        for path in self.paths:
            with suppress(PermissionError, FileNotFoundError):
                executables.extend(f.name for f in path.iterdir() if f.is_file())
        return sorted(executables)

    def find_executable(self, cmd):
        for path in self.paths:
            if (path / cmd).is_file():
                return path / cmd
        return None

    def parse_redirects(self, parts):
        def pop_redirect(ops):
            for op in ops:
                try:
                    idx = parts.index(op)
                    path = parts.pop(idx + 1)
                    parts.pop(idx)
                    mode = "a" if op.endswith(">>") else "w"
                    return open(path, mode)
                except (ValueError, IndexError):
                    continue
            return None

        stderr = pop_redirect(["2>>", "2>"]) or sys.stderr
        stdout = pop_redirect(["1>>", ">>", "1>", ">"]) or sys.stdout
        return parts, stdout, stderr

    def execute_command(self, parts, stdout, stderr):
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]

        if handler := self.builtins.get(cmd):
            handler(args, stdout, stderr)
        elif exe_path := self.find_executable(cmd):
            run([exe_path, *args], stdout=stdout, stderr=stderr)
        else:
            stderr.write(f"{cmd}: command not found\n")

    def handle_echo(self, args, stdout, _):
        stdout.write(" ".join(args) + "\n")

    def handle_type(self, args, stdout, stderr):
        if not args:
            stderr.write("type: missing argument\n")
            return
        for cmd in args:
            if cmd in self.builtins:
                stdout.write(f"{cmd} is a shell builtin\n")
            elif exe := self.find_executable(cmd):
                stdout.write(f"{cmd} is {exe}\n")
            else:
                stderr.write(f"{cmd}: not found\n")

    def handle_exit(self, args, _, stderr):
        code = 0
        if len(args) > 1:
            stderr.write("exit: too many arguments\n")
            return
        if args:
            try:
                code = int(args[0])
            except ValueError:
                stderr.write(f"exit: {args[0]}: numeric argument required\n")
                code = 255
        sys.exit(code)

    def handle_pwd(self, _, stdout, __):
        stdout.write(f"{Path.cwd()}\n")

    def handle_cd(self, args, _, stderr):
        if len(args) > 1:
            stderr.write("cd: too many arguments\n")
            return
        path = Path(args[0]).expanduser() if args else Path.home()
        if not path.is_dir():
            stderr.write(f"cd: {path}: No such directory\n")
            return
        os.chdir(path)

    @staticmethod
    def readchar():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            new = termios.tcgetattr(fd)
            new[3] &= ~(termios.ICANON | termios.ECHO)
            termios.tcsetattr(fd, termios.TCSADRAIN, new)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def handle_tab_completion(self, tab_count, matches, completion, command):
        if not matches:
            sys.stdout.write("\a")
            return
        if len(matches) == 1:
            completion = matches[0][len(command):] + " "
            sys.stdout.write(completion)
            return
        if tab_count == 1:
            sys.stdout.write(completion[len(command):])
        elif tab_count > 1:
            sys.stdout.write(f"\n{'  '.join(matches)}\n$ {command}")


if __name__ == "__main__":
    Shell().run()
    