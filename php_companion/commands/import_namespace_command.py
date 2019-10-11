import sublime
import sublime_plugin

import os
import re

from ..settings import get_setting
from ..utils import get_namespace, get_active_project_path

class ImportNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        projectPath = get_active_project_path()
        file_name = self.view.file_name().replace(projectPath, '')
        if file_name.startswith('/'):
            file_name = file_name[1:]

        # Abort if the file is not PHP
        if not (file_name.endswith('.php') or file_name.endswith('.install') or file_name.endswith('.module')):
            sublime.error_message('No .php extension')
            return

        namespace_stmt = get_namespace(os.path.dirname(file_name))

        # Ensuring PHP tag presence
        php_tag = '<?php'
        php_regex = php_tag.replace('?', '\?')
        php_region = self.view.find(php_regex, 0)
        if php_region.empty():
            line = self.view.line(php_region)
            self.view.insert(edit, 0, php_tag)

        # Removing existing namespace
        namespace_region = self.view.find(r'\s*namespace\s[\w\\]+;', 0)
        if not namespace_region.empty():
            self.view.replace(edit, namespace_region, '')

        # Adding namespace
        namespace_position = get_setting('namespace_position')
        namespace_contents = ' '
        if namespace_position != 'inline':
            namespace_contents = '\n' * get_setting('namespace_blank_lines', 2)
        namespace_contents += 'namespace ' + namespace_stmt + ';'
        if namespace_position != 'inline':
            php_regex += r'(\s*\/\*(?:[^*]|\n|(?:\*(?:[^\/]|\n)))*\*\/)?'
        php_docblock_region = self.view.find(php_regex, 0)
        if not php_docblock_region.empty():
            line = self.view.line(php_docblock_region)
            self.view.insert(edit, line.end(), namespace_contents)
