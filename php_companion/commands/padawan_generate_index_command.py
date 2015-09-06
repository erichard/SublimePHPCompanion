import sublime_plugin
from ..padawan import client


class PadawanGenerateIndexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        fname = self.view.file_name()
        if fname is None:
            return None
        client.Generate(fname)

