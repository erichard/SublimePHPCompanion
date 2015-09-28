import sublime, sublime_plugin
from ..padawan import client


def sel_end(sel):
    return max(sel.a, sel.b)


def is_php_file(view):
    return view.score_selector(sel_end(view.sel()[0]), "source.php") > 0


class PadawanCompleter(sublime_plugin.EventListener):

    def run_completion(self, view):
        view.run_command('auto_complete', {
            'api_completions_only': True,
            'disable_auto_insert': True
            })

    def on_modified_async(self, view):
        if not is_php_file(view):
            return
        cursor = view.sel()[0].b
        if cursor < 1:
            return

        while cursor > 0:
            curChar = view.substr(sublime.Region(cursor-1, cursor))
            if curChar == '\\':
                return self.run_completion(view)
            if curChar == '$':
                return self.run_completion(view)
            if curChar == '(':
                return self.run_completion(view)
            if cursor > 1:
                curChar = view.substr(sublime.Region(cursor-2, cursor))
                if curChar == '->':
                    return self.run_completion(view)
                if curChar == '::':
                    return self.run_completion(view)
            if cursor > 3:
                curChar = view.substr(sublime.Region(cursor-4, cursor))
                if curChar == 'use ':
                    return self.run_completion(view)
                if curChar == 'new ':
                    return self.run_completion(view)
                if cursor > 9:
                    curChar = view.substr(sublime.Region(cursor-10, cursor))
                    if curChar == 'namespace ':
                        return self.run_completion(view)
            cursor -= 1

    def on_query_completions(self, view, prefix, locations):
        if not is_php_file(view):
            return None
        fname = view.file_name()
        if fname is None:
            return None
        column = 16
        line = 35
        line, column = view.rowcol(locations[0])
        contents = view.substr(sublime.Region(0, view.size()))
        completions = client.GetCompletion(
            fname,
            line+1,
            column+1,
            contents
            )["completion"]
        return (
            [self.format_menu_item(c) for c in completions],
            sublime.INHIBIT_WORD_COMPLETIONS
            )

    def format_menu_item(self, c):
        return [c["menu"] if c["menu"] else c["name"], c["name"]]
