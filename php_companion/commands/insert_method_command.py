import sublime
import sublime_plugin
import re

class InsertMethodCommand(sublime_plugin.TextCommand):
    # Runs the plugin
    def run(self, edit, stub, offset):
        self.view.insert(edit, offset, stub)