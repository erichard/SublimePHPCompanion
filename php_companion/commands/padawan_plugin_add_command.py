import sublime, sublime_plugin
from ..padawan import client

class PadawanPluginAddCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        def success(name):
            if not name or not isinstance(name, str):
                return
            client.AddPlugin(name)

        def on_change(name):
            return

        def on_cancel():
            return

        sublime.active_window().show_input_panel(
                "Plugin Name",
                "",
                success,
                on_change,
                on_cancel
                )
