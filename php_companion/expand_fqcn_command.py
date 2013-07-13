import sublime_plugin

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