import sublime
import sublime_plugin
import re

class FindMethodsCommand(sublime_plugin.TextCommand):
    # Taken from the utils.py file. Is there a way to
    # import it instead of duplicating it here?
    def normalize_to_system_style_path(self, path):
        if sublime.platform() == "windows":
            path = re.sub(r"/([A-Za-z])/(.+)", r"\1:/\2", path)
            path = re.sub(r"/", r"\\", path)
        return path

    # Runs the plugin
    def run(self, edit, path):
        # Get the contents of the file at the given path
        with open(self.normalize_to_system_style_path(path), "r") as f:
            content = f.read()

        # Get the methods from the content
        self.methods = re.findall("(?<!\* )(?:abstract )?(?:public|protected|private)(?: static)? function [A-z0-9]*\([A-z0-9$=, ]*\)[A-z :]*", content)
        self.methods.insert(0, 'Import all methods')

        # Show the available methods in the quick panel
        if (len(self.methods) > 0):
            self.view.window().show_quick_panel(self.methods, self.on_done)

    # Handles selection of a quick panel item
    def on_done(self, index):
        if index == -1:
            return

        # Find the closing brackets. We'll place the method
        # stubs just before the last closing bracket.
        closing_brackets = self.view.find_all("[}]")

        # Add the method stub(s) to the current file
        region = closing_brackets[-1]
        point = region.end() - 1

        template = "\n\t{0}\n\t{{\n\t\tthrow new \Exception('Method not implemented');\n\t}}\n"

        # Add all method stubs
        if index == 0:            
            for method in self.methods[1:]:
                method_stub = template.format(method)
                self.view.run_command("insert_method", {"stub": method_stub, "offset": point})
                sublime.status_message('Successfully imported all methods')
        # Add selected method stub
        else:
            method_stub = template.format(self.methods[index])
            self.view.run_command("insert_method", {"stub": method_stub, "offset": point})
            sublime.status_message('Successfully imported method')