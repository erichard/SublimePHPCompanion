import sublime, sublime_plugin, re

class CreateCommand(sublime_plugin.TextCommand):

    # Runs the plugin
    def run(self, edit, stub, offset):
        self.view.insert(edit, offset, stub)
