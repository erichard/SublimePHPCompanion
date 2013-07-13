import sublime
import sublime_plugin

import re

from ..utils import find_symbol

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