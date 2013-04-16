import sublime
import sublime_plugin
import re
import mmap
import contextlib
import os

setting = sublime.load_settings('PHP Companion.sublime-settings').get

def find_symbol(symbol, window):
    files = window.lookup_symbol_in_index(symbol)
    namespaces = []
    pattern = re.compile(b'namespace\s+([^;]+);')

    def filter_file(file):
        if setting('exclude_dir'):
            for dir in setting('exclude_dir'):
                if dir in file[1]:
                    return False

        return file

    for file in files:
        if filter_file(file):
            with open(file[0], "r+b") as f:
                with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
                    for match in re.findall(pattern, m):
                        namespaces.append([match.decode('utf-8') + "\\" + symbol, file[1]])
                        break

    return namespaces


class ImportUseCommand(sublime_plugin.TextCommand):
    def run(self, edit, namespace):
        view = self.view
        use_stmt = "use " + namespace + ";"

        region = view.find(use_stmt.replace('\\','\\\\'), 0)
        if not region.empty():
            return sublime.status_message('Use already exist !')

        uses = []
        regions = view.find_all(r"^(use\s+.+[;])", 0, '$1', uses)
        uses.append(use_stmt)
        uses = list(set(uses))
        uses.sort()
        uses = "\n".join(uses)


        if len(regions) > 0:
            region = regions[0]
            for r in regions:
                region = region.cover(r)

            view.replace(edit, region, uses)
            return True

        region = view.find(r"^\s*namespace\s+[\w\\]+[;{]", 0)
        if not region.empty():
            line = view.line(region)
            view.insert(edit, line.end(), "\n" + uses)
            return True

        region = view.find(r"<\?php", 0)
        if not region.empty():
            line = view.line(region)
            view.insert(edit, line.end(), "\n" + uses)
            return True

class FindUseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        symbol = view.substr(view.word(view.sel()[0]))

        if re.match(r"\w", symbol) is None:
            return sublime.status_message('Not a valid symbol "%s" !' % symbol)

        self.namespaces = find_symbol(symbol, view.window())

        if len(self.namespaces) == 1:
            self.view.run_command("import_use", {"namespace": self.namespaces[0][0]})

        if len(self.namespaces) > 1:
            view.window().show_quick_panel(self.namespaces, self.on_done)

    def on_done(self, index):
        if index == -1:
            return

        self.view.run_command("import_use", {"namespace": self.namespaces[index][0]})


class ReplaceFqdnCommand(sublime_plugin.TextCommand):
    def run(self, edit, region_start, region_end, namespace):
        region = sublime.Region(region_start,region_end)
        self.view.replace(edit, region, namespace)
        return True

class ExpandFqdnCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        self.region = view.word(view.sel()[0])
        symbol = view.substr(self.region)

        if re.match(r"\w", symbol) is None:
            return sublime.status_message('Not a valid symbol "%s" !' % symbol)

        self.namespaces = find_symbol(symbol, view.window())

        if len(self.namespaces) == 1:
            self.view.run_command("replace_fqdn", {"region_start": self.region.begin(), "region_end": self.region.end(), "namespace": self.namespaces[0][0]})

        if len(self.namespaces) > 1:
            view.window().show_quick_panel(self.namespaces, self.on_done)

    def on_done(self, index):
        if index == -1:
            return

        self.view.run_command("replace_fqdn", {"region_start": self.region.begin(), "region_end": self.region.end(), "namespace": self.namespaces[index][0]})


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
