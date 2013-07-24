import sublime
import sublime_plugin

import re

class GotoDefinitionScopeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        run = GTDRun(self.view, self.view.window())
        run.do()

class GTDRun:
    def __init__(self, view, window):
        self.view = view
        self.window = window
        self.selected_region = self.view.word(self.view.sel()[0])

    def do(self):
        if self.in_class_scope():
            selected_str = self.view.substr(self.selected_region)
            for symbol in self.view.symbols():
                if symbol[1] == selected_str:
                    self.view.sel().clear()
                    self.view.sel().add(symbol[0])
                    self.view.show(symbol[0])
                    return

        # falls back to the original functionality
        self.window.run_command("goto_definition")

    def in_class_scope(self):
        selected_point = self.selected_region.begin()
        # the search area is 60 pts wide, maybe it is not enough
        search_str = self.view.substr(sublime.Region(selected_point - 60,selected_point))

        return re.search("(\$this->|self::|static::)(\s)*$", search_str) != None
