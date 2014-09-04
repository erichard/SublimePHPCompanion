import sublime
import sublime_plugin

import os
import re

from ..settings import get_setting

class ImportNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        region = self.view.find(r"^(<\?php){0,1}\s*namespace\s[\w\\]+;", 0)

        if not region.empty():
            return sublime.status_message('namespace definition already exist !')

        # Filename to namespace
        filename = self.view.file_name()

        if (not filename.endswith(".php")):
            sublime.error_message("No .php extension")
            return

        region = self.view.find(r"<\?php", 0)
        if not region.empty():

            # namespace begin at first camelcase dir
            namespaceStmt = os.path.dirname(filename)

            pattern = re.compile(get_setting("start_dir_pattern", "^.*?((?:\/[A-Z][^\/]*)+)$"))

            namespaceStmt = re.sub(pattern, '\\1', namespaceStmt)
            namespaceStmt = re.sub('/', '\\\\', namespaceStmt)
            namespaceStmt = namespaceStmt.strip("\\")

            # Add an optional prefix - may be per project
            if get_setting("namespace_prefix", None):
                namespaceStmt = get_setting("namespace_prefix", '') + "\\" + namespaceStmt

            line_contents = "namespace " + namespaceStmt + ";"
            if "inline" == get_setting("namespace_position", "newline"):
                line_contents = " " + line_contents
            else:
                line_contents = '\n\n' + line_contents

            line = self.view.line(region)
            self.view.insert(edit, line.end(), line_contents)
            return True
