import sublime
import sublime_plugin

class ReplaceFqcnCommand(sublime_plugin.TextCommand):
    def run(self, edit, region_start, region_end, namespace, leading_separator):
        region = sublime.Region(region_start, region_end)

        if (leading_separator):
            namespace = '\\' + namespace

        self.view.replace(edit, region, namespace)

        return True