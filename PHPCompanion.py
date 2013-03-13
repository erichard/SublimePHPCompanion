import sublime, sublime_plugin, re, mmap, contextlib, os

setting = sublime.load_settings('PHP Companion.sublime-settings').get

class ImportUseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        symbol = view.substr(view.word(view.sel()[0]))

        if re.match(r"\w", symbol) == None:
            return sublime.status_message('Not a valid symbol "%s" !' % symbol)

        exclude_dir = setting('exclude_dir')

        files = view.window().lookup_symbol_in_index(symbol)
        namespaces = []
        pattern = re.compile(rb'namespace\s+([^;]+);')

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
                        for match in re.findall(pattern,m):
                            namespaces.append(match.decode('utf-8') + "\\" + symbol)
                            break
            
        def import_use_in_view(view, edit, namespace):
            uses = []
            region = view.find_all(r"^\s*(use\s+[\w\\]+[;])", 0, '$1', uses)
            uses.append("use " + namespace + ";")
            uses = list(set(uses))
            uses.sort()

            print(edit)

            if len(region) > 0:
                region = sublime.Region(region[0].begin(),region.pop().end())
                view.replace(edit, region, "\n"+"\n".join(uses))
                return True

            region = view.find(r"^\s*namespace\s+[\w\\]+[;{]", 0)
            if not region.empty():
                line = view.line(region)
                line_contents = '\n\n' + "use " + namespace + ";"
                view.insert(edit, line.end(), line_contents)
                return True

            region = view.find(r"<\?php", 0)
            if not region.empty():
                line = view.line(region)
                line_contents = '\n\n' + "use " + namespace + ";"
                view.insert(edit, line.end(), line_contents)
                return True
        
        def on_select(index):
            import_use_in_view(self.view, edit, namespaces[index])
            return True

        if len(namespaces) == 1:
            import_use_in_view(view, edit, namespaces[0])
            return True

        if len(namespaces) > 1:
            view.window().show_quick_panel(namespaces, on_select, sublime.MONOSPACE_FONT)

        return True 






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
            pattern = r"[^A-Z]+(.*)"

        namespaceStmt = re.sub(pattern, '\\1', namespaceStmt)
        namespaceStmt = re.sub('/', '\\\\', namespaceStmt)

        region = self.view.find(r"<\?php", 0)
        if region != None:
            line = self.view.line(region)
            line_contents = '\n\n' + "namespace " + namespaceStmt + ";"
            self.view.insert(edit, line.end(), line_contents)
            return True
