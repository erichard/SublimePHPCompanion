import sublime

import re
import mmap
import contextlib
import subprocess
import json

from .settings import filename as settings_filename

def normalize_to_system_style_path(path):
    if sublime.platform() == "windows":
        path = re.sub(r"/([A-Za-z])/(.+)", r"\1:/\2", path)
        path = re.sub(r"/", r"\\", path)
    return path

def find_symbol(symbol, window):
    files = window.lookup_symbol_in_index(symbol)
    namespaces = []
    pattern = re.compile(b'^\s*namespace\s+([^;]+);', re.MULTILINE)
    settings = sublime.load_settings(settings_filename()).get

    def filter_file(file):
        if settings('exclude_dir'):
            for pattern in settings('exclude_dir'):
                pattern = re.compile(pattern)
                if pattern.match(file[1]):
                    return False

        return file

    for file in files:
        if filter_file(file):
            with open(normalize_to_system_style_path(file[0]), "rb") as f:
                with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
                    for match in re.findall(pattern, m):
                        namespaces.append([match.decode('utf-8') + "\\" + symbol, file[1]])
                        break

    if settings('allow_use_from_global_namespace'):
        namespaces += find_in_global_namespace(symbol)

    return namespaces

def find_in_global_namespace(symbol):
    definedClasses = subprocess.check_output(["php", "-r", "echo json_encode(get_declared_classes());"]);
    definedClasses = definedClasses.decode('utf-8')
    definedClasses = json.loads(definedClasses)
    definedClasses.sort()

    matches = []
    for phpClass in definedClasses:
        if symbol == phpClass:
            matches.append([phpClass, phpClass])

    return matches
