import sublime_plugin
from ..padawan import client


class PadawanStartServerCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        client.StartServer()


class PadawanStopServerCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        client.StopServer()


class PadawanRestartServerCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        client.RestartServer()
