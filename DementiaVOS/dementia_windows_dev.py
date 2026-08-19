import os
import shlex
import base64
import secrets
import string
import subprocess
from datetime import datetime
from getpass import getpass

class VFile:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content
        self.created = datetime.now()

class VFolder:
    def __init__(self, name):
        self.name = name
        self.items = {}

class DementiaVOS:
    def __init__(self):
        self.system = VFolder("system_folder")
        self.cwd = self.system
        self.path = []
        self.history = []

        documents = VFolder("documents")
        workstation = VFolder("workstation")

        projects = VFolder("projects")
        documents.items["projects"] = projects

        temporary = VFolder("temporary")
        temporaryhidden = VFolder(".temporary_hidden")

        archives = VFolder("archives")
        self.system.items["workstation"] = workstation
        self.system.items["documents"] = documents
        self.system.items["temporary"] = temporary
        self.system.items[".temporary_hidden"] = temporaryhidden
        self.system.items["archives"] = archives

        self.system.items[".dev_selfie"] = VFile(".dev_selfie", """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⢀⣴⠟⠉⠀⠀⠀⠈⠻⣦⡀⠀⠀⠀⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣀⢀⣾⠿⠻⢶⣄⠀⠀⣠⣶⡿⠶⣄⣠⣾⣿⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⢻⣿⣿⡿⣿⠿⣿⡿⢼⣿⣿⡿⣿⣎⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠉⠛⢛⣛⡉⠀⠀⠙⠛⠻⠛⠑⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣧⣤⣴⠿⠿⣷⣤⡤⠴⠖⠳⣄⣀⣹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣀⣟⠻⢦⣀⡀⠀⠀⠀⠀⣀⡈⠻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠉⡇⠀⠀⠛⠛⠛⠋⠉⠉⠀⠀⠀⠹⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡟⠀⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠈⠑⠪⠷⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣦⣼⠛⢦⣤⣄⡀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⠢⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠲⠖⠛⠻⣿⡿⠛⠉⠉⠻⠷⣦⣽⠿⠿⠒⠚⠋⠉⠁⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⠛⠁⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢣⠀⠀⠀
⠀⠀⠀⠀⣰⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⠀
⠀⠀⠀⣰⣿⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣧⣄⠀⠀⠀⠀⠀⠀⢳⡀⠀
⠀⠀⠀⣿⡾⢿⣀⢀⣀⣦⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⣫⣿⡿⠟⠻⠶⠀⠀⠀⠀⠀⢳⠀
⠀⠀⢀⣿⣧⡾⣿⣿⣿⣿⣿⡷⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⢀⡴⢿⣿⣧⠀⡀⠀⢀⣀⣀⢒⣤⣶⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠀⠀⡾⠁⠙⣿⡈⠉⠙⣿⣿⣷⣬⡛⢿⣶⣶⣴⣶⣶⣶⣤⣤⠤⠾⣿⣿⣿⡿⠿⣿⠿⢿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠀⣸⠃⠀⠀⢸⠃⠀⠀⢸⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⠟⡉⠀⠀⠀⠈⠙⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠀⣿⠀⠀⢀⡏⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⠛⠉⠁⠀⠀⠀⠀⠀⠉⠠⠿⠟⠻⠟⠋⠉⢿⣿⣦⡀⢰⡀⠀⠀⠀⠀⠀⠀⠁
⢀⣿⡆⢀⡾⠀⠀⠀⠀⣾⠏⢿⣿⣿⣿⣯⣙⢷⡄⠀⠀⠀⠀⠀⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣻⢿⣷⣀⣷⣄⠀⠀⠀⠀⢸⠀
⢸⠃⠠⣼⠃⠀⠀⣠⣾⡟⠀⠈⢿⣿⡿⠿⣿⣿⡿⠿⠿⠿⠷⣄⠈⠿⠛⠻⠶⢶⣄⣀⣀⡠⠈⢛⡿⠃⠈⢿⣿⣿⡿⠀⠀⠀⠀⠀⡀
⠟⠀⠀⢻⣶⣶⣾⣿⡟⠁⠀⠀⢸⣿⢅⠀⠈⣿⡇⠀⠀⠀⠀⠀⣷⠂⠀⠀⠀⠀⠐⠋⠉⠉⠀⢸⠁⠀⠀⠀⢻⣿⠛⠀⠀⠀⠀⢀⠇
⠀⠀⠀⠀⠹⣿⣿⠋⠀⠀⠀⠀⢸⣧⠀⠰⡀⢸⣷⣤⣤⡄⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡆⠀⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⢼⡇
⠀⠀⠀⠀⠀⠙⢻⠄⠀⠀⠀⠀⣿⠉⠀⠀⠈⠓⢯⡉⠉⠉⢱⣶⠏⠙⠛⠚⠁⠀⠀⠀⠀⠀⣼⠇⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⡇
⠀⠀⠀⠀⠀⠀⠻⠄⠀⠀⠀⢀⣿⠀⢠⡄⠀⠀⠀⣁⠁⡀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⢀⣐⡟⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⢠⡇
        """)

        self.system.items[".debug"] = VFile(".debug", """
        color <color>
        history clear
        devmode
        devmode off
        """)

        self.opened_file = None
        self.dev_password = "fuckingdev"
        
        self.system.items[".dev"] = VFile(".dev", """
        try w
        try .
        try c
        try v
        """)

        self.opened_file = None
        self.dev_password = "fuckingdev"

    def current_path(self):
        if not self.path:
            return "system"

        return "system/" + "/".join(self.path)

    def find_item(self, name):
        return self.resolve_item(name)

    def resolve_path(self, path):
        if not path:
            return self.cwd, ""

        path = path.replace("\\", "/")

        if path == "system":
            return None, "system"

        if path.startswith("system/"):
            current = self.system
            parts = path.split("/")[1:]
        elif path.startswith("/"):
            current = self.system
            parts = path.strip("/").split("/")
        else:
            current = self.cwd
            parts = path.split("/")

        parts = [part for part in parts if part not in ("", ".")]

        for part in parts[:-1]:
            if part == "..":
                current = self.system
                continue

            item = current.items.get(part)

            if item is None:
                return None, parts[-1]

            if not isinstance(item, VFolder):
                return None, parts[-1]

            current = item

        if parts:
            final_name = parts[-1]

            if final_name == "..":
                return None, final_name

            return current, final_name

        return current, ""


    def resolve_item(self, path):
        if not path:
            return self.cwd

        path = path.replace("\\", "/")

        if path == "system":
            return self.system

        if path.startswith("system/"):
            current = self.system
            parts = path.split("/")[1:]
        elif path.startswith("/"):
            current = self.system
            parts = path.strip("/").split("/")
        else:
            current = self.cwd
            parts = path.split("/")

        parts = [part for part in parts if part not in ("", ".")]

        for part in parts:
            if part == "..":
                current = self.system
                continue

            item = current.items.get(part)

            if item is None:
                return None

            current = item

        return current

    def check_dev_password(self):
        if getattr(self, "devmode", False):
            return True

        password = getpass("Password: ")

        if password != self.dev_password:
            print("User Error.")
            return False

        return True

    def ls(self, show_hidden=False, target=None):
        folder = self.cwd

        if target:
            item = self.resolve_item(target)

            if item is None:
                print(f"ls: cannot access '{target}': No such file or directory")
                return

            if isinstance(item, VFile):
                print(f"  📄 {item.name}")
                return

            folder = item

        if not folder.items:
            print("  (empty)")
            return

        visible_items = []

        for name, item in folder.items.items():
            if not show_hidden and name.startswith("."):
                continue

            visible_items.append((name, item))

        if not visible_items:
            print("  (empty)")
            return

        for name, item in sorted(visible_items):
            if isinstance(item, VFolder):
                print(f"  📁 {name}/")
            else:
                print(f"  📄 {name}")

    def cd(self, target):
        if not target:
            print(self.current_path())
            return

        target = target.replace("\\", "/")

        if target == "..":
            if self.path:
                self.path.pop()

                self.cwd = self.system

                for part in self.path:
                    self.cwd = self.cwd.items[part]
            return

        if target == "/" or target == "system":
            self.cwd = self.system
            self.path = []
            return

        if target.startswith("/"):
            current = self.system
            new_path = []

            parts = [part for part in target.strip("/").split("/") if part not in ("", ".")]

            for part in parts:
                if part == "..":
                    if new_path:
                        new_path.pop()
                        current = self.system

                        for path_part in new_path:
                            current = current.items[path_part]
                    continue

                item = current.items.get(part)

                if item is None:
                    print(f"cd: '{target}': folder not found")
                    return

                if not isinstance(item, VFolder):
                    print(f"cd: '{target}': not a folder")
                    return

                current = item
                new_path.append(part)

            self.cwd = current
            self.path = new_path
            return

        parts = [part for part in target.split("/") if part not in ("", ".")]

        current = self.cwd
        new_path = self.path.copy()

        for part in parts:
            if part == "..":
                if new_path:
                    new_path.pop()

                current = self.system

                for path_part in new_path:
                    current = current.items[path_part]

                continue

            item = current.items.get(part)

            if item is None:
                print(f"cd: '{target}': folder not found")
                return

            if not isinstance(item, VFolder):
                print(f"cd: '{target}': not a folder")
                return

            current = item
            new_path.append(part)

        self.cwd = current
        self.path = new_path

    def mkdir(self, name):
        if not name:
            print("Usage: mkdir <folder>")
            return

        folder, final_name = self.resolve_path(name)

        if folder is None or not final_name:
            print("Invalid folder path.")
            return

        if final_name in folder.items:
            print("That name already exists.")
            return

        folder.items[final_name] = VFolder(final_name)
        print(f"Created folder '{name}'")

    def touch(self, name):
        if not name:
            print("Usage: touch <filename>")
            return

        folder, final_name = self.resolve_path(name)

        if folder is None or not final_name:
            print("Invalid file path.")
            return

        if final_name in folder.items:
            print("That file already exists.")
            return

        folder.items[final_name] = VFile(final_name)
        print(f"Created '{name}'")

    def write(self, name, text):
        folder, final_name = self.resolve_path(name)

        if folder is None or not final_name:
            print(f"write: '{name}': invalid file path")
            return

        item = folder.items.get(final_name)

        if item is None:
            item = VFile(final_name)
            folder.items[final_name] = item

        if isinstance(item, VFolder):
            print("Cannot write to a folder.")
            return

        if final_name == ".dev":
            if not self.check_dev_password():
                return

        item.content = text
        print(f"Saved '{name}'")

    def librewolf(self, url=None):
        try:
            if url:
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url

                subprocess.Popen(["librewolf", url])
            else:
                subprocess.Popen(["librewolf"])

        except FileNotFoundError:
            print("librewolf: executable not found")
        except Exception as e:
            print(f"librewolf: failed to open: {e}")

    def cat(self, name):
        item = self.resolve_item(name)

        if item is None:
            print(f"cat: '{name}': file not found")
            return

        if isinstance(item, VFolder):
            print("Cannot read a folder.")
            return

        if item.name == ".debug":
            if not self.check_dev_password():
                return

        if item.name == ".dev":
            if not self.check_dev_password():
                return

        print()
        print(item.content if item.content else "(empty file)")
        print()

    def edit(self, name):
        item = self.resolve_item(name)

        if item is None:
            print(f"edit: '{name}': file not found")
            return

        if isinstance(item, VFolder):
            print("Cannot edit a folder.")
            return

        if item.name == ".dev":
            if not self.check_dev_password():
                return

        print()
        print(f"--- Editing {name} ---")
        print("Current contents:")
        print(item.content if item.content else "(empty file)")
        print()
        print("Enter the new contents.")
        print("Type .save on a new line to save.")
        print("Type .cancel on a new line to cancel.")
        print()

        lines = []

        while True:
            try:
                line = input("> ")
            except (KeyboardInterrupt, EOFError):
                print("\nEdit cancelled.")
                return

            if line == ".save":
                item.content = "\n".join(lines)
                print(f"Saved '{name}'")
                return

            if line == ".cancel":
                print("Edit cancelled.")
                return

            lines.append(line)

    def rm(self, name):
        if not name:
            print("Usage: rm <name>")
            return

        if name == "system" or name == "/":
            if not self.check_dev_password():
                return

            confirmation = input("Type DELETE to confirm: ").strip()

            if confirmation != "FUCK YOU":
                print("User Error.")
                return

            self.system = VFolder("system")
            self.cwd = self.system
            self.path = []
            self.opened_file = None

            print("System folder deleted.")
            return

        folder, final_name = self.resolve_path(name)

        if folder is None or not final_name:
            print("File or folder not found.")
            return

        item = folder.items.get(final_name)

        if item is None:
            print("File or folder not found.")
            return

        if final_name == "archives":
            print("You cannot remove archives.")
            return

        archives = self.system.items["archives"]
        archives.items[final_name] = item
        del folder.items[final_name]

        print(f"Removed '{name}'.")

    def rename(self, old, new):
        source_folder, source_name = self.resolve_path(old)

        if source_folder is None or not source_name:
            print(f"'{old}' not found.")
            return

        if source_name not in source_folder.items:
            print(f"'{old}' not found.")
            return

        destination_folder, destination_name = self.resolve_path(new)

        if destination_folder is None or not destination_name:
            print(f"'{new}' is not a valid destination.")
            return

        if destination_name in destination_folder.items:
            print(f"'{new}' already exists.")
            return

        item = source_folder.items.pop(source_name)
        item.name = destination_name
        destination_folder.items[destination_name] = item

        print(f"Renamed '{old}' to '{new}'")

    def mv(self, source, destination):
        if not source or not destination:
            print("Usage: mv <file> <folder>")
            return

        source_folder, source_name = self.resolve_path(source)

        if source_folder is None or source_name not in source_folder.items:
            print(f"mv: '{source}': file or folder not found")
            return

        item = source_folder.items[source_name]
        target = self.resolve_item(destination)

        if target is None:
            print(f"mv: '{destination}': destination folder not found")
            return

        if not isinstance(target, VFolder):
            print(f"mv: '{destination}': not a folder")
            return

        if item is target:
            print("User Error.")
            return

        if source_name in target.items:
            print(f"mv: '{source}' already exists in '{destination}'")
            return

        del source_folder.items[source_name]
        target.items[source_name] = item

        print(f"Moved '{source}' to '{destination}'")

    def cp(self, source, destination):
        if not source or not destination:
            print("Usage: cp <file> <newname>")
            return

        item = self.resolve_item(source)

        if item is None:
            print(f"cp: '{source}': file or folder not found")
            return

        if isinstance(item, VFolder):
            print("cp: copying folders is not supported.")
            return

        destination_folder, destination_name = self.resolve_path(destination)

        if destination_folder is None or not destination_name:
            print(f"cp: '{destination}': invalid destination")
            return

        if destination_name in destination_folder.items:
            print(f"cp: '{destination}' already exists.")
            return

        copied_file = VFile(destination_name, item.content)
        destination_folder.items[destination_name] = copied_file

        print(f"Copied '{source}' to '{destination}'")

    def show_history(self, number=None):
        if number is not None:
            if number < 1 or number > len(self.history):
                print(f"history: '{number}': command not found")
                return

            print(f"  {number}  {self.history[number - 1]}")
            return

        if not self.history:
            print("No command history.")
            return

        for number, command in enumerate(self.history, 1):
            print(f"  {number}  {command}")

    def rmhelp(self):
        print("Removed content will first move to /archives. Removing content in archives will move them to the void.")

    def w(self):
        print("4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOA4qOg4qOA4qOA4qOA4qOA4qKA4qO04qOm4qCA4qKA4qCA4qOA4qOY4qO/4qCC4qCA4qCg4qOA4qOA4qCA4qKk4qOk4qOk4qOk4qOk4qOk4qCA4qOt4qGE4qCI4qCJ4qCb4qC54qC/4qC/4qC/4qC/4qC34qC+4qCP4qCb4qCP4qK74qG/4qC/4qK/4qG/4qK/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kgv+Kgv+Kgi+KjoOKhjOKipeKjjOKggeKggOKggOKggOKhkOKgoOKjjeKgkuKgpOKiv+Kgt+KiuOKjv+Kjv+Kjv+Kjv+Kjv+KjpOKjt+KjjOKggOKjpOKjgOKhpOKigOKjgOKjgOKjgOKjgOKhgOKigOKjgOKjiOKjvOKjgeKjpOKjuOKjv+Kjvwrio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioL/ioIPiooDio5DiorDioL7ioIvioqDio6TiobTioJ7io5vioZvioIDioLjio7fio77io7/io7/io6bioZHioIjior/iob/ioL/io7/io7/io7/io7/io7/io7/ioa/io7/io7/io7/io6Xio6Xio7/io4jio73io7jio63io63io6zio63io63io73io7/io78K4qCA4qCI4qCJ4qCJ4qCJ4qCJ4qCB4qCJ4qCJ4qCJ4qCL4qCB4qCA4qCA4qCA4qCA4qKA4qO04qOP4qO/4qC/4qCW4qOh4qCf4qOp4qO04qO/4qO/4qG/4qCX4qCA4qC/4qO/4qC/4qO/4qO/4qC/4qOM4qGC4qCY4qCm4qOw4qO24qO24qO24qO24qO24qGE4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKjgOKjgOKjgOKjgOKjgOKjgOKjgOKjgOKjgOKjgOKjgOKjgOKjgOKggOKggOKggOKgm+KioeKhhuKggOKgguKggOKgoeKjvuKgv+Kgv+Kii+KjpeKghuKggOKjtuKhgOKgueKjhuKiu+Kjv+Kjt+KhnOKjv+Kjt+KjhOKgueKjv+Kjv+Kjv+Kjv+Kjv+Khh+KjveKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjvwrioIDio4Dio4DiooDioIDio4Dio4Dio4Dio4Dio6Dio6Tio4TioYDioIDio4DioZnioJPioIDioIHioIDioIDio6Dio6TioIDioqDio7bioJ/ioIviooDio7zio7/ioIPioYTio7/ioYbiorvio7/io7fiobjio7/io7/ioYTiornio7/io7/io7/io7/io6fio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qG/4qCB4qKg4qO/4qCA4qCG4qCA4qCG4qCA4qOw4qGf4qCA4qOk4qGk4qCA4qKA4qOA4qOa4qGb4qCb4qOw4qO/4qK44qO/4qCY4qO/4qO/4qGH4qK54qO/4qGE4qCY4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Khh+KggOKjuOKii+KhtuKggOKjpOKhgOKjgOKhv+KggeKgkOKgkuKgtuKjtuKjn+Kjm+Kju+Khn+KioOKjv+Kgj+KjvuKhj+KggOKjueKjv+Khh+KiuOKjv+Khh+KggOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjvwrio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYfiooDio7/io7jioIPiorjio7/io6fiob/ioqfio7fioKDioIDioIDioIDioozioJnio7/ioYfio7/iob/ioqDiob/ioIHioIbio7/io7/ioqPio77io7/ioIfioIDio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io78K4qCb4qCb4qCb4qCb4qCb4qCb4qCb4qCb4qCb4qCb4qCD4qCD4qCI4qO/4qO/4qCA4qCY4qOP4qC74qCA4qC44qO/4qO34qO/4qO/4qO34qO24qO/4qO/4qOn4qCY4qKB4qO/4qCA4qCe4qO44qG/4qKD4qG84qO/4qO/4qCA4qCA4qCb4qCb4qCb4qCb4qCb4qCb4qCb4qCb4qO74qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKhhuKggOKggOKggOKggOKggOKjtuKjtuKhtuKgtuKjtuKhgOKggOKguOKiu+KggOKhgOKjjOKgm+Kih+KiseKjvOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KiqOKggOKggOKjvuKgn+KjoeKhv+Kio+Kjv+KggeKggOKggOKggOKggOKjv+KjvuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjvwrioIPioIDioIDioIDioIDio7Tiorvio7/io6Tio77io7/io7fioYbioIDioIjioKPioIDiorjio6fioJjior7io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7fio6TiobzioIvio7DioJ7ioIHioIDioIDioIDioIDioIDio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io78K4qCg4qCA4qCA4qOE4qG+4qKB4qCO4qO44qO/4qO/4qO/4qO/4qO/4qGE4qKg4qCA4qCA4qCY4qK/4qGH4qCA4qC74qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qG/4qCB4qCA4qCA4qOA4qOg4qO24qO/4qCA4qCR4qCA4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKhhuKggOKjsOKjv+Kjt+Kjn+KjsOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjtOKhgOKggOKggOKgiOKgh+KiuOKjt+KjjOKgu+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kgn+KggeKigOKjpOKjvuKjv+Kjv+Khv+Kjv+Kjh+KggOKggOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjvwrioYfioqDio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioL/ioJvioJvioJvioIDioILioIDioIDio7jio7/io7/io7fio4Tio5nioLvioL/ioL/ioJ/ioJvio4nio6Tio7bio7/io7/io7/io7/io7/io7/io6fioYjio7/ioIDioIDio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io78K4qGH4qK44qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCf4qOh4qO24qO/4qO/4qO/4qO34qO24qOE4qGA4qC/4qK/4qO/4qO/4qO/4qO/4qO34qGG4qCA4qC/4qC+4qC/4qC/4qC/4qC/4qC/4qC/4qC/4qC/4qK/4qO/4qGH4qO/4qCA4qCA4qK54qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKjgeKjvuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Khv+KigeKjvuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjpuKjpOKjreKjneKjm+Kju+Kgh+KikOKjkuKjguKjpOKjtOKjtuKjv+Kjv+Kjv+Kjv+KjtuKjhOKhmeKgh+KimOKjgOKggOKiuOKhh+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjvwrio7/io7/io7/io7/io7/io7/io7/io7/ioYfiorjio7/io7/io7/io7/io7/io7/io7/ioZ/ioLriopvio7/io7/io7/io7fio7bio7bio7bio7bio6Tio6zio5nioLvior/io7/io5/io6Pio63io63io63io53io5vioYTioIjioJviorfio6zioYfio7/io7/io7/io7/io7/io7/io7/io7/iorjio7/io7/io7/io7/io7/io7/io7/io7/io78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCA4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCH4qO04qO/4qO/4qO/4qO/4qO/4qO/4qO/4qG/4qK/4qO/4qO/4qO/4qO/4qOm4qGZ4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO24qOM4qGZ4qCH4qK44qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCY4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KhgOKiv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Khj+KiuOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjt+KhgOKiiOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjjOKiu+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Khv+KipuKgmOKgv+KgiOKjv+Kjv+Kjv+Kjv+Kjv+KhhOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjvwrio7/io7/io7/io7/io7/io7/io7/io7/io6fioLjio7/io7/io7/io7/io7/io7/ioIDio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io77ioYzio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io6bio6bioIDioIDio7/io7/io7/io7/io7/io4fio7/io7/io7/io7/io7/io7/io7/io7/io78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qGG4qK74qO/4qO/4qO/4qO/4qO/4qGE4qK74qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCH4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qGG4qCA4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kgm+KggeKggOKhmOKjv+Kjv+Kjv+Kjv+Kjv+Kjt+KhmOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kgj+KgkOKiv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kgg+KggOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjvwrio7/io7/io7/io7/io7/io7/ioY/ioIDioIDioKDioIHiornio7/io7/io7/io7/io7/io7fioYjioLvio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioL/ioJvio4nio7Tio7fio6biobnior/io7/io7/io7/io7/io7/io7/io7/io7/ioZ/ioqDioYDio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io78K4qO/4qO/4qO/4qO/4qO/4qO/4qGH4qCA4qCE4qCg4qCA4qCI4qO/4qO/4qO/4qO/4qO/4qO/4qGH4qKz4qOs4qOZ4qCb4qCb4qCb4qCb4qOb4qOb4qOp4qOl4qO04qO+4qO/4qO/4qO/4qO/4qO/4qO/4qOm4qGZ4qC/4qO/4qO/4qO/4qO/4qO/4qGf4qKB4qO84qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KggOKggOKggOKggOKggOKiu+Kjv+Kjv+Kjv+Kjv+Kjv+Kjp+KiuOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjpuKhhOKgm+Kgm+Kii+KjoeKjtOKguOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KggOKggOKggOKggArio7/io7/io7/io7/io7/io7/io7/ioIDioIDiooHioIDioIDioIjio7/io7/io7/io7/io7/io7/ioIDio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYbiorDio7bio7/io7/io7/ioYTio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYbioIDio7zio78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCA4qCI4qCA4qCA4qCA4qCA4qK74qO/4qO/4qO/4qO/4qO/4qCA4qCY4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qK54qO/4qO/4qGH4qCY4qO/4qO/4qO/4qO/4qGH4qO/4qO/4qK/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qGH4qKw4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Khv+KggOKggOKggOKggOKggOKggOKgiOKjv+Kjv+Kjv+Kjv+Kjv+KjtuKhgOKggeKgm+Kii+KjvOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjvuKjv+Kjv+Kjt+KggOKgmeKjv+Kjv+Kjv+Khh+Kjv+Kjv+KgmOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjp+KgmOKjv+Kjvwrio7/io7/io7/io7/io7/io7/io7fioIDioIDioIDioIDioIDioIDioIDiornio7/io7/io7/io7/ioYfioIDiooDio7Tio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io6bioZjior/io7/ioYfio7/io7/ioIDio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/iorjio7/io78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCB4qCA4qCI4qCC4qCA4qCA4qKA4qKw4qO/4qO/4qO/4qO/4qCP4qOw4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qOm4qGZ4qCH4qK44qO/4qCA4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KghOKggOKggOKgguKgoOKjpuKjieKiuOKjv+Kjv+Kjv+Kgj+KjuOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjpuKhmOKiv+KggOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kgm+Kjv+Kjvwrio7/io7/io7/io7/io7/io7/io7/ioIDiorjio4Pio7DiobfioInioIHioIjio7/io7/ioY/iorjio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io6bioYDioL/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/iob/io7/io78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCA4qCI4qK74qOm4qGA4qCA4qCA4qCk4qCo4qO/4qKj4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qC34qOM4qK/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qOf4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjhuKjgOKjgOKjoOKjgOKjoOKjhOKjpOKhgOKii+KjvOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjt+KhuOKjhOKiu+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjvwrio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYfiorjio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioZ/io7/io7/io7/io7/io7/ioYbiorvio7/ioIvio7/io7/io7/io7/io7/io7/io78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qKg4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qC/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qGf4qOw4qO/4qO/4qO/4qO/4qO/4qO/4qGG4qK74qGG4qO/4qO/4qO/4qO/4qO/4qO/4qO/CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kgh+KjvuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjt+KjrOKhm+Kiv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Khn+KisOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KhhuKgg+Kiu+Kjv+Kjv+Kjv+Kjv+Khj+Kjvwrio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/iob/iorDio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io6bio5nioL/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/iob/iorHio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYbiorjio7/io7/io7/io7/ioYfio78K4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qGH4qO+4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qOm4qGM4qK74qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qGD4qO84qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qOn4qC44qO/4qO/4qO/4qO/4qOH4qK7CuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Khh+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjp+KhmOKiv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kig+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KggOKjv+Kjv+Kjv+Kjv+Khl+KgoArio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYfior/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYbiorvio7/io7/io7/io7/iob/iorjio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYbio7/io7/io7/io7/io7/io7wK4qO/4qO/4qO/4qK/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qC44qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qOG4qCZ4qO/4qO/4qCL4qCB4qO84qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO34qO/4qO/4qO/4qO/4qO/4qO/CuKjh+KgueKjv+KjhOKgmeKiv+Kjv+Kjv+Kjv+Kgn+Kgm+Kgu+Kjv+Kjv+KhhuKiv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjhOKgmeKjgeKjgeKjvOKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjvwrio7/io6fioZjior/io7fio77io7/iob/ioL/ioIDioIDioIDio7/io7/io7/ioJjio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYTior/io63io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io78K4qO/4qO/4qO/4qO24qO/4qO/4qO/4qO/4qCA4qCA4qCA4qGG4qO/4qO/4qO/4qOn4qC44qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCI4qK/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qG/")

    def version(self):
        print("version 2.0.1")

    def whoami(self):
        print("system")

    def echo(self, args):
        print(" ".join(args))

    def base64_tool(self):
        print()
        print("--- Base64 Encoder / Decoder ---")
        print("Type 'encode' to encode text.")
        print("Type 'decode' to decode Base64.")
        print("Type 'exit' to close Base64.")
        print()

        while True:
            try:
                mode = input("> ").strip().lower()
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
                    text = input("> ")
                    encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")

                    print()
                    print("Encoded:")
                    print(encoded)
                    print()

                else:
                    encoded = input("> ").strip()
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
            except (ValueError, base64.binascii.Error):
                print("Error: invalid Base64 input.")
            except (KeyboardInterrupt, EOFError):
                print("\nLeaving Base64.")
                return

    def pass_tool(self):
        print()
        print("--- Password Generator ---")
        print("Type 'generate' to create a password.")
        print("Type 'exit' to close Password Generator.")
        print()

        while True:
            try:
                mode = input("> ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print("\nLeaving Password Generator.")
                return

            if mode in ("exit", "quit"):
                print("Leaving Password Generator.")
                return

            if mode != "generate":
                print("Usage: generate or exit")
                continue

            try:
                length_input = input("Length (default 20): ").strip()

                if length_input:
                    length = int(length_input)
                else:
                    length = 20

                if length < 8:
                    print("Error: password length must be at least 8.")
                    continue

                if length > 256:
                    print("Error: password length cannot exceed 256.")
                    continue

                alphabet = string.ascii_letters + string.digits + string.punctuation
                password = "".join(secrets.choice(alphabet) for _ in range(length))

                print()
                print("Generated password:")
                print(password)
                print()

                try:
                    copy = input("Copy to clipboard? [y/N]: ").strip().lower()
                except (KeyboardInterrupt, EOFError):
                    print("\nPassword generated, but not copied.")
                    continue

                if copy in ("y", "yes"):
                    try:
                        if os.name == "nt":
                            subprocess.run(
                                ["clip"],
                                input=password,
                                text=True,
                                check=True
                            )

                        elif os.system("command -v pbcopy >/dev/null 2>&1") == 0:
                            subprocess.run(
                                ["pbcopy"],
                                input=password,
                                text=True,
                                check=True
                            )

                        elif os.system("command -v xclip >/dev/null 2>&1") == 0:
                            subprocess.run(
                                ["xclip", "-selection", "clipboard"],
                                input=password,
                                text=True,
                                check=True
                            )

                        elif os.system("command -v xsel >/dev/null 2>&1") == 0:
                            subprocess.run(
                                ["xsel", "--clipboard", "--input"],
                                input=password,
                                text=True,
                                check=True
                            )

                        else:
                            raise RuntimeError("No supported clipboard utility found.")

                        print("Password copied to clipboard.")

                    except Exception:
                        print("Could not copy password to clipboard.")
                        print("The generated password is still shown above.")

                print()

            except ValueError:
                print("Error: length must be a whole number.")
            except (KeyboardInterrupt, EOFError):
                print("\nLeaving Password Generator.")
                return

    def help(self):
        print("""
        ls                   List visible files and folders
        ls -a                List all files, including hidden files
        ls <folder>          List files inside a folder

        cd <folder>          Enter a folder
        cd ..                Go back
        ..                   Go back one folder
        pwd                  Show current location

        mkdir <name>         Create a folder
        touch <name>         Create an empty file
        write <file> <text>  Write text into a file

        cat <file>           Read a file
        edit <file>          Fake-edit a file from inside DementiaVOS
        rename <old> <new>   Rename content
        mv <file> <folder>   Move a file or folder
        cp <file> <newname>  Copy a file
        rm <name>            Move content to archives
        rm-help              Understand rm

        touch .secret.txt    Create a hidden file
        write .secret.txt    This is hidden
        mkdir .hidden        Create a hidden folder

        history              Show command history
        history <number>     Show a specific command from history

        clear                Clear the terminal
        version              Show current version
        date                 Show the virtual system time
        whoami               Show current user

        tool base64          Open the Base64 encoder/decoder
        tool passgen         Open the secure password generator
        debug                Turn on debug mode
        debug off            Turn off debug mode
        librewolf            Open librewolf
        librewolf <domain>   Search domain with librewolf (exemple: youtube.com)

        echo <text>          Print text
        help                 Show this help
        exit/quit/shutdown   Shut down DementiaVOS
""")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def c():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    vfs = DementiaVOS()
    vfs.devmode = False
    debug_mode = False
    devmode = False

    prompt_color = "\033[91m"


    clear()

    print("""
----------------------------------------------------------------------------------------------
DementiaVOS Python, Windows Edition

Type 'help' to see available commands or 'exit/quit/shutdown' to safely close the application.
To force quit, press 'ctrl + c'.
----------------------------------------------------------------------------------------------
""")

    while True:
        try:
            command = input(
                        f"{prompt_color}{vfs.current_path()}\033[0m" + (
                "%debug " if debug_mode else "$dementia "
            )

        ).strip()

        except (KeyboardInterrupt, EOFError):
            print("\nShutting down...")
            break

        if not command:
            continue

        vfs.history.append(command)

        try:
            args = shlex.split(command)
        except ValueError as e:
            print(f"Syntax error: {e}")
            continue

        cmd = args[0].lower()
        args = args[1:]

        if cmd == "debug":
            if args and args[0].lower() == "off":
                debug_mode = False
            else:
                debug_mode = True

        elif cmd == "color":
            if not debug_mode:
                print("color: command not found")
            elif not args:
                print("Usage: color <red|green|yellow|blue|magenta|cyan|white>")
            else:
                colors = {
                    "red": "\033[91m",
                    "green": "\033[92m",
                    "yellow": "\033[93m",
                    "blue": "\033[94m",
                    "magenta": "\033[95m",
                    "cyan": "\033[96m",
                    "white": "\033[97m"
                }

                color = args[0].lower()

                if color in colors:
                    prompt_color = colors[color]
                else:
                    print("Unknown color.")

        elif cmd == "help":
            vfs.help()

        elif cmd == "ls":
            if args and args[0] == "-a":
                if len(args) > 1:
                    vfs.ls(show_hidden=True, target=args[1])
                else:
                    vfs.ls(show_hidden=True)
            elif len(args) == 1:
                vfs.ls(target=args[0])
            elif not args:
                vfs.ls()
            else:
                print("Usage: ls [-a] [folder]")

        elif cmd == "cd":
            vfs.cd(args[0] if args else "")

        elif cmd == "..":
            vfs.cd("..")

        elif cmd == "mkdir":
            vfs.mkdir(args[0] if args else "")

        elif cmd == "devmode":
            if not debug_mode:
                print("devmode: command not found")
            elif args and args[0].lower() == "off":
                devmode = False
                vfs.devmode = False
                print("Developer mode disabled.")
            else:
                devmode = True
                vfs.devmode = True
                print("Developer mode enabled.")


        elif cmd == "touch":
            vfs.touch(args[0] if args else "")

        elif cmd == "write":
            if len(args) < 2:
                print("Usage: write <file> <text>")
            else:
                vfs.write(args[0], " ".join(args[1:]))

        elif cmd == "cat":
            vfs.cat(args[0] if args else "")

        elif cmd == "edit":
            vfs.edit(args[0] if args else "")

        elif cmd == "rm":
            vfs.rm(args[0] if args else "")

        elif cmd == "rename":
            if len(args) != 2:
                print("Usage: rename <old> <new>")
            else:
                vfs.rename(args[0], args[1])

        elif cmd == "mv":
            if len(args) != 2:
                print("Usage: mv <file> <folder>")
            else:
                vfs.mv(args[0], args[1])

        elif cmd == "cp":
            if len(args) != 2:
                print("Usage: cp <file> <newname>")
            else:
                vfs.cp(args[0], args[1])

        elif cmd == "history":
            if args and args[0].lower() == "clear":
                if not debug_mode:
                    print("history clear: command not found")
                else:
                    vfs.history.clear()
                    print("Command history cleared.")
            elif args:
                if len(args) != 1:
                    print("Usage: history [number]")
                else:
                    try:
                        number = int(args[0])
                        vfs.show_history(number)
                    except ValueError:
                        print(f"history: '{args[0]}': invalid number")
            else:
                vfs.show_history()

        elif cmd == "tool":
            if args and args[0].lower() == "base64":
                vfs.base64_tool()
            elif args and args[0].lower() == "passgen":
                vfs.pass_tool()
            else:
                print("Usage: tool base64 or tool passgen")

        elif cmd == "pwd":
            print(vfs.current_path())

        elif cmd == "rm-help":
            vfs.rmhelp()

        elif cmd == "w":
            vfs.w()

        elif cmd == "version":
            vfs.version()

        elif cmd == "whoami":
            vfs.whoami()

        elif cmd == "librewolf":
            vfs.librewolf(args[0] if args else None)

        elif cmd == "v":
            vfs.version()

        elif cmd == "echo":
            vfs.echo(args)

        elif cmd == "date":
            print(datetime.now().strftime("%A, %B %d %Y %H:%M:%S"))

        elif cmd == "clear":
            clear()

        elif cmd == "c":
            clear()


        elif cmd == ".":
            clear()

        elif cmd in ("exit", "quit", "shutdown", "fuck"):
            print("\nShutting down DementiaVOS...")
            break

        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    main()
