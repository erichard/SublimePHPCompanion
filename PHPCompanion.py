import sublime
import sublime_plugin

import re
import mmap
import contextlib
import os

from php_companion import import_use_command, find_use_command

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

class ReplaceFqcnCommand(sublime_plugin.TextCommand):
    def run(self, edit, region_start, region_end, namespace, leading_separator):
        region = sublime.Region(region_start, region_end)

        if (leading_separator):
            namespace = '\\' + namespace

        self.view.replace(edit, region, namespace)

        return True


class ExpandFqcnCommand(sublime_plugin.TextCommand):
    def run(self, edit, leading_separator=False):
        view = self.view
        self.region = view.word(view.sel()[0])
        symbol = view.substr(self.region)

        if re.match(r"\w", symbol) is None:
            return sublime.status_message('Not a valid symbol "%s" !' % symbol)

        self.namespaces = find_symbol(symbol, view.window())
        self.leading_separator = leading_separator

        if len(self.namespaces) == 1:
            self.view.run_command("replace_fqcn", {"region_start": self.region.begin(), "region_end": self.region.end(), "namespace": self.namespaces[0][0], "leading_separator": self.leading_separator})

        if len(self.namespaces) > 1:
            view.window().show_quick_panel(self.namespaces, self.on_done)

    def on_done(self, index):
        if index == -1:
            return

        self.view.run_command("replace_fqcn", {"region_start": self.region.begin(), "region_end": self.region.end(), "namespace": self.namespaces[index][0], "leading_separator": self.leading_separator})


class ImportNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        region = self.view.find(r"^\s*namespace\s[\w\\]+;", 0)

        if not region.empty():
            return sublime.status_message('namespace definition already exist !')

        # Filename to namespace
        filename = self.view.file_name()

        if (not filename.endswith(".php")):
            sublime.error_message("No .php extension")
            return

        # namespace begin at first camelcase dir
        namespaceStmt = os.path.dirname(filename)

        if (setting("start_dir_pattern")):
            pattern = re.compile(setting("start_dir_pattern"))
        else:
            pattern = r"^.*?((?:\/[A-Z][^\/]*)+)$"

        namespaceStmt = re.sub(pattern, '\\1', namespaceStmt)
        namespaceStmt = re.sub('/', '\\\\', namespaceStmt)
        namespaceStmt = namespaceStmt.strip("\\")

        region = self.view.find(r"<\?php", 0)
        if not region.empty():
            line = self.view.line(region)
            line_contents = '\n\n' + "namespace " + namespaceStmt + ";"
            self.view.insert(edit, line.end(), line_contents)
            return True
