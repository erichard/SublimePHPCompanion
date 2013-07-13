import sublime

import re
import mmap
import contextlib
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from php_companion import import_use_command
from php_companion import find_use_command
from php_companion import replace_fqcn_command
from php_companion import expand_fqcn_command
from php_companion import import_namespace_command

setting = sublime.load_settings('PHP Companion.sublime-settings').get

def normalize_to_system_style_path(path):
    if sublime.platform() == "windows":
        path = re.sub(r"/([A-Za-z])/(.+)", r"\1:/\2", path)
        path = re.sub(r"/", r"\\", path)
    return path


def find_symbol(symbol, window):
    files = window.lookup_symbol_in_index(symbol)
    namespaces = []
    pattern = re.compile(b'^\s*namespace\s+([^;]+);', re.MULTILINE)

    def filter_file(file):
        if setting('exclude_dir'):
            for pattern in setting('exclude_dir'):
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

    return namespaces