import os
import shlex
import msvcrt
import time
import base64
import binascii
from datetime import datetime


class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content
        self.modified = time.time()


class Directory:
    def __init__(self, name):
        self.name = name
        self.items = {}


class OpenVOS:
    def __init__(self):
        self.root = Directory("/")
        self.cwd = []
        self.history = []

    def normalize(self, path):
        if not path:
            return self.cwd[:]

        parts = [] if path.startswith("/") else self.cwd[:]

        for part in path.split("/"):
            if not part or part == ".":
                continue

            if part == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(part)

        return parts

    def get(self, path):
        current = self.root

        for part in self.normalize(path):
            if not isinstance(current, Directory):
                return None

            current = current.items.get(part)

            if current is None:
                return None

        return current

    def parent(self, path):
        parts = self.normalize(path)

        if not parts:
            return None, None

        current = self.root

        for part in parts[:-1]:
            current = current.items.get(part)

            if not isinstance(current, Directory):
                return None, None

        return current, parts[-1]

    def pwd(self):
        return "/" + "/".join(self.cwd) if self.cwd else "/"

    def mkdir(self, path):
        parent, name = self.parent(path)

        if parent is None:
            return False, "No such directory"

        if name in parent.items:
            return False, "File exists"

        parent.items[name] = Directory(name)

        return True, ""

    def touch(self, path):
        parent, name = self.parent(path)

        if parent is None:
            return False, "No such directory"

        if name in parent.items:
            if isinstance(parent.items[name], Directory):
                return False, "Is a directory"

            return True, ""

        parent.items[name] = File(name)

        return True, ""

    def write(self, path, content):
        parent, name = self.parent(path)

        if parent is None:
            return False, "No such directory"

        item = parent.items.get(name)

        if isinstance(item, Directory):
            return False, "Is a directory"

        if item is None:
            item = File(name)
            parent.items[name] = item

        item.content = content
        item.modified = time.time()

        return True, ""

    def remove(self, path, recursive=False):
        parent, name = self.parent(path)

        if parent is None or name not in parent.items:
            return False, "No such file or directory"

        item = parent.items[name]

        if isinstance(item, Directory):
            if item.items and not recursive:
                return False, "Directory not empty"

        del parent.items[name]

        return True, ""

    def change_directory(self, path):
        item = self.get(path)

        if not isinstance(item, Directory):
            return False

        self.cwd = self.normalize(path)

        return True

    def ls(self, args):
        path = "."

        for arg in reversed(args):
            if not arg.startswith("-"):
                path = arg
                break

        show_hidden = "-a" in args or "--all" in args

        item = self.get(path)

        if item is None:
            print(f"ls: {path}: No such file or directory")
            return

        if isinstance(item, File):
            print(item.name)
            return

        for name in sorted(item.items):
            if name.startswith(".") and not show_hidden:
                continue

            if isinstance(item.items[name], Directory):
                print(name + "/")
            else:
                print(name)

    def version(self, args):
        print("OpenVOS v. 1.9")

    def whoami(self, args):
        print(">")

    def cd(self, args):
        path = args[0] if args else "/"

        if not self.change_directory(path):
            print(f"cd: {path}: No such file or directory")

    def pwd_command(self, args):
        print(self.pwd())

    def mkdir_command(self, args):
        if not args:
            print("mkdir: missing operand")
            return

        for path in args:
            if path.startswith("-"):
                continue

            success, error = self.mkdir(path)

            if not success:
                print(f"mkdir: {path}: {error}")

    def touch_command(self, args):
        if not args:
            print("touch: missing operand")
            return

        for path in args:
            if path.startswith("-"):
                continue

            success, error = self.touch(path)

            if not success:
                print(f"touch: {path}: {error}")

    def cat(self, args):
        if not args:
            print("cat: missing operand")
            return

        for path in args:
            item = self.get(path)

            if item is None:
                print(f"cat: {path}: No such file or directory")
                continue

            if isinstance(item, Directory):
                print(f"cat: {path}: Is a directory")
                continue

            print(item.content, end="")

    def write_command(self, args):
        if len(args) < 2:
            print("Usage: write <file> <text>")
            return

        path = args[0]
        content = " ".join(args[1:]) + "\n"

        success, error = self.write(path, content)

        if not success:
            print(f"write: {path}: {error}")

    def rm(self, args):
        if not args:
            print("rm: missing operand")
            return

        recursive = "-r" in args or "-rf" in args

        paths = [
            arg for arg in args
            if not arg.startswith("-")
        ]

        if not paths:
            print("rm: missing operand")
            return

        for path in paths:
            success, error = self.remove(path, recursive)

            if not success:
                print(f"rm: {path}: {error}")

    def base64_tool(self):
        print()
        print("--- Base64 Encoder / Decoder ---")
        print("Type 'encode' to encode text.")
        print("Type 'decode' to decode Base64.")
        print("Type 'exit' to close Base64.")
        print()

        while True:
            try:
                mode = input("base64> ").strip().lower()

            except (KeyboardInterrupt, EOFError):
                print("\nLeaving Base64.")
                return

            if mode in ("exit", "quit"):
                print("Leaving Base64.")
                return

            if mode not in ("encode", "decode"):
                print("Usage: encode, decode, or exit")
                continue

            try:
                if mode == "encode":
                    text = input("Text> ")

                    encoded = base64.b64encode(
                        text.encode("utf-8")
                    ).decode("ascii")

                    print()
                    print("Encoded:")
                    print(encoded)
                    print()

                else:
                    encoded = input("Base64> ").strip()

                    decoded = base64.b64decode(
                        encoded.encode("ascii"),
                        validate=True
                    ).decode("utf-8")

                    print()
                    print("Decoded:")
                    print(decoded)
                    print()

            except UnicodeDecodeError:
                print("Error: decoded data is not valid UTF-8 text.")

            except (ValueError, binascii.Error):
                print("Error: invalid Base64 input.")

            except (KeyboardInterrupt, EOFError):
                print("\nLeaving Base64.")
                return

    def mv(self, args):
        if len(args) != 2:
            print("Usage: mv <source> <destination>")
            return

        source, destination = args

        source_parent, source_name = self.parent(source)

        if source_parent is None:
            print(f"mv: {source}: No such file or directory")
            return

        if source_name not in source_parent.items:
            print(f"mv: {source}: No such file or directory")
            return

        item = source_parent.items[source_name]

        destination_item = self.get(destination)

        if isinstance(destination_item, Directory):
            if source_name in destination_item.items:
                print(
                    f"mv: {destination}/{source_name}: "
                    "File exists"
                )
                return

            destination_item.items[source_name] = item

        else:
            destination_parent, destination_name = self.parent(
                destination
            )

            if destination_parent is None:
                print(
                    f"mv: {destination}: "
                    "No such directory"
                )
                return

            if destination_name in destination_parent.items:
                print(f"mv: {destination}: File exists")
                return

            item.name = destination_name
            destination_parent.items[destination_name] = item

        del source_parent.items[source_name]

    def cp(self, args):
        if len(args) != 2:
            print("Usage: cp <source> <destination>")
            return

        source, destination = args

        item = self.get(source)

        if item is None:
            print(f"cp: {source}: No such file or directory")
            return

        if isinstance(item, Directory):
            print(f"cp: {source}: Is a directory")
            return

        destination_item = self.get(destination)

        if isinstance(destination_item, Directory):
            destination_parent = destination_item
            destination_name = item.name

        else:
            destination_parent, destination_name = self.parent(
                destination
            )

        if destination_parent is None:
            print(f"cp: {destination}: No such directory")
            return

        if destination_name in destination_parent.items:
            print(f"cp: {destination}: File exists")
            return

        destination_parent.items[destination_name] = File(
            destination_name,
            item.content,
        )

    def echo(self, args):
        print(" ".join(args))

    def clear(self, args):
        os.system(
            "cls" if os.name == "nt" else "clear"
        )

    def date(self, args):
        print(
            datetime.now().strftime(
                "%a %b %d %H:%M:%S %Y"
            )
        )

    def history_command(self, args):
        for number, command in enumerate(
            self.history,
            1,
        ):
            print(f"{number:5}  {command}")

    def nano(self, args):
        if not args:
            print("nano: missing file operand")
            return

        path = args[0]
        item = self.get(path)

        if item is None:
            success, error = self.touch(path)

            if not success:
                print(f"nano: {path}: {error}")
                return

            item = self.get(path)

        if isinstance(item, Directory):
            print(f"nano: {path}: Is a directory")
            return

        print("Enter text.")
        print("Use .save to save or .cancel to cancel.")

        lines = []

        while True:
            try:
                line = input()

            except (KeyboardInterrupt, EOFError):
                print()
                return

            if line == ".save":
                item.content = "\n".join(lines) + "\n"
                item.modified = time.time()

                print("Saved.")
                return

            if line == ".cancel":
                print("Cancelled.")
                return

            lines.append(line)

    def help(self, args):
        print("""
ls [-a] [path]        List files
cd [path]             Change directory
pwd                   Print current directory

mkdir <dir>           Create directory
touch <file>          Create file
cat <file>            Read file
write <file> <text>   Write file
nano <file>           Edit file
tool base64           Encoder and decode in base64 using tool

cp <src> <dst>        Copy file
mv <src> <dst>        Move or rename
rm [-r] <path>        Remove file/directory

echo <text>           Print text
clear                 Clear screen
date                  Show date/time
history               Show command history
version               Show current OVOS version
whoami                Show current user

help                  Show commands
exit                  Exit
shutdown              Exit
""")

    def get_completion_candidates(self, text):
        """
        Find possible command/file/directory completions.
        """

        commands = [
            "ls",
            "cd",
            "pwd",
            "mkdir",
            "touch",
            "cat",
            "write",
            "nano",
            "rm",
            "mv",
            "cp",
            "echo",
            "clear",
            "date",
            "history",
            "help",
            "version",
            "whoami",
            "tool",
            "exit",
            "quit",
            "shutdown",
        ]

        if " " not in text:
            prefix = text.lower()

            return [
                command
                for command in commands
                if command.lower().startswith(prefix)
            ]

        parts = text.split()

        if not parts:
            return []

        partial = parts[-1]

        if "/" in partial:
            directory_part = partial.rsplit("/", 1)[0]
            name_part = partial.rsplit("/", 1)[1]

            if directory_part == "":
                directory = "/"
            else:
                directory = directory_part

        else:
            directory = "."
            name_part = partial

        item = self.get(directory)

        if not isinstance(item, Directory):
            return []

        candidates = []

        for name in sorted(item.items):

            if name.startswith(".") and not name_part.startswith("."):
                continue

            if name.lower().startswith(name_part.lower()):
                if isinstance(item.items[name], Directory):
                    name += "/"

                candidates.append(name)

        return candidates

    def autocomplete(self, text):
        """
        Complete the current command.
        Returns:
            completed_text, candidates
        """

        candidates = self.get_completion_candidates(text)

        if not candidates:
            return text, []

        if len(candidates) == 1:
            candidate = candidates[0]

            if " " not in text:
                return candidate, candidates

            parts = text.split()

            parts[-1] = candidate

            return " ".join(parts), candidates

        if " " not in text:
            prefix = text

            common = candidates[0]

            for candidate in candidates[1:]:
                while not candidate.lower().startswith(
                    common.lower()
                ):
                    common = common[:-1]

                    if not common:
                        break

            if len(common) > len(prefix):
                return common, candidates

        else:
            parts = text.split()
            prefix = parts[-1]

            common = candidates[0]

            for candidate in candidates[1:]:
                while not candidate.lower().startswith(
                    common.lower()
                ):
                    common = common[:-1]

                    if not common:
                        break

            if len(common) > len(prefix):
                parts[-1] = common
                return " ".join(parts), candidates

        return text, candidates

    def terminal_input(self, prompt):
        """
        Custom Windows input that supports TAB autocomplete.
        """

        text = ""
        tab_candidates = []
        tab_index = 0

        print(prompt, end="", flush=True)

        while True:
            key = msvcrt.getwch()

            if key in ("\r", "\n"):
                print()
                return text

            if key == "\x03":
                print("^C")
                return ""

            if key == "\x08":
                if text:
                    text = text[:-1]

                    print("\b \b", end="", flush=True)

                tab_candidates = []
                tab_index = 0
                continue

            if key == "\t":
                completed, candidates = self.autocomplete(text)

                if not candidates:
                    continue

                if completed == text:
                    if len(candidates) > 1:
                        print()
                        print("  ".join(candidates))

                        print(prompt + text, end="", flush=True)

                        tab_index = 0
                        tab_candidates = candidates

                    continue

                print("\r" + " " * (len(prompt) + len(text)), end="")
                print("\r" + prompt, end="")

                text = completed

                print(text, end="", flush=True)

                tab_candidates = candidates
                tab_index = 0

                continue

            if key in ("\x00", "\xe0"):
                msvcrt.getwch()
                continue

            if key.isprintable():
                text += key
                print(key, end="", flush=True)

                tab_candidates = []
                tab_index = 0

    def shell_input(self, prompt):
        """
        Wrapper for terminal input.
        """

        return self.terminal_input(prompt)


    def execute(self, command):
        try:
            parts = shlex.split(command)

        except ValueError as error:
            print(f"sh: {error}")
            return True

        if not parts:
            return True

        name = parts[0]
        args = parts[1:]

        try:
            if name in ("shutdown", "exit", "quit"):
                return False

            if name == "ls":
                self.ls(args)

            elif name == "cd":
                self.cd(args)

            elif name == "pwd":
                self.pwd_command(args)

            elif name == "mkdir":
                self.mkdir_command(args)

            elif name == "touch":
                self.touch_command(args)

            elif name == "cat":
                self.cat(args)

            elif name == "write":
                self.write_command(args)

            elif name == "nano":
                self.nano(args)

            elif name == "rm":
                self.rm(args)

            elif name == "mv":
                self.mv(args)

            elif name == "cp":
                self.cp(args)

            elif name == "echo":
                self.echo(args)

            elif name == "clear":
                self.clear(args)

            elif name == "date":
                self.date(args)

            elif name == "history":
                self.history_command(args)

            elif name == "help":
                self.help(args)

            elif name == "version":
                self.version(args)

            elif name == "whoami":
                self.whoami(args)

            elif name == "tool":
                if args and args[0].lower() == "base64":
                    self.base64_tool()
                else:
                    print("Usage: tool base64")

            else:
                print(f"{name}: command not found")

        except Exception as error:
            print(
                f"{name}: {type(error).__name__}: {error}"
            )

        return True


def main():
    system = OpenVOS()

    print("Open Virtual OS")
    print("Type 'help' for commands.")
    print()

    while True:
        try:
            command = system.shell_input(
                f"{system.pwd()}> "
            ).strip()


        except (KeyboardInterrupt, EOFError):
            print("\nExiting OpenVOS.")
            break

        if not command:
            continue

        system.history.append(command)

        if not system.execute(command):
            print("Shutting down OpenVOS.")
            break


if __name__ == "__main__":
    main()
