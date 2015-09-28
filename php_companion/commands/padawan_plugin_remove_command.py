import sublime, sublime_plugin
from ..padawan import client

class PadawanPluginRemoveCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        items = client.GetInstalledPlugins()

        def success(index):
            if index >= len(items):
                return
            name = items[index]
            if not name:
                return
            client.RemovePlugin(name)

        sublime.active_window().show_quick_panel(
                items,
                success,
                )
