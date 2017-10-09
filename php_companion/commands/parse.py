import sublime, sublime_plugin, re

from ..settings import get_setting

class ParseCommand(sublime_plugin.TextCommand):

    # Normalizes a given path to the current system style
    # -- This method is from the PHP Companion utils file
    #
    def normalize_to_system_style_path(self, path):
        if sublime.platform() == "windows":
            path = re.sub(r"/([A-Za-z])/(.+)", r"\1:/\2", path)
            path = re.sub(r"/", r"\\", path)
        return path

    # Runs the plugin
    #
    def run(self, edit, path):
        # Get the contents of the file at the given path
        with open(self.normalize_to_system_style_path(path), "r") as f:
            content = f.read()

        pattern = "(?<!\* )(?:abstract )?((?:public|protected|private)(?: static)?\s+function\s+[\w]+\s*\(.*?\)(?:\s*\:\s*\w+)?)(?:\s*;|.*?{)"
        # Get the methods from the content
        self.methods = re.findall(pattern, content, re.S)

        # find comment docblocks
        self.method_docblocks = {}
        for m in self.methods:
            pos = content.index(m)
            try:
                end = content.rindex("*/", 0, pos)
                if re.findall(pattern, content[end:pos], re.S) or re.findall("(interface|abstract([A-Z0-9\s]+)class)\s+[A-Z0-9]+", content[end:pos]):
                    self.method_docblocks[m] = None
                    continue

                start = content.rindex("/**", 0, end)
                self.method_docblocks[m] = content[start:end + 2]
            except ValueError:
                self.method_docblocks[m] = None

        self.methods.insert(0, 'Insert all methods')

        # Show the available methods in the quick panel
        if (len(self.methods) > 0):
            self.view.window().show_quick_panel(self.methods, self.on_done)

    # Handles selection of a quick panel item
    #
    def on_done(self, index):
        if index == -1:
            return

        # Find the closing brackets. We'll place the method
        # stubs just before the last closing bracket.
        closing_brackets = self.view.find_all("[}]")

        # Add the method stub(s) to the current file
        region = closing_brackets[-1]
        point = region.end() - 1

        # Choose format to indicate that the method body is yet to be implemented.
        if get_setting("use_todo_implement") == True:
            template = "\n\t{0}\n\t{{\n\t\t// TODO: Implement {1}() method.\n\t}}\n"
        else:
            template = "\n\t{0}\n\t{{\n\t\tthrow new \Exception('Method {1}() is not implemented');\n\t}}\n"

        # Better way to handle add all selection?
        if index == 0:
            methods = ""
            for method in self.methods[1:]:
                if self.method_docblocks[method] != None:
                    if get_setting("docblock_inherit") == True:
                        method = self.method_docblocks[method] + "\n\t" + method
                    elif get_setting("docblock_inherit") == "inheritdoc":
                        method = "\n\t".join(["/**", " * {@inheritdoc}", "*/"]) + "\n\t" + method

                pattern = ".+\s+function\s+([\w]+).+"
                methodname = re.findall(pattern, method)[0]
                methods += template.format(method, methodname)

            self.view.run_command("create", {"stub": methods, "offset": point})
        else:
            method = self.methods[index]
            if get_setting("docblock_inherit") == True:
                if self.method_docblocks[method] != None:
                    method = self.method_docblocks[method] + "\n\t" + method
            elif get_setting("docblock_inherit") == "inheritdoc":
                method = "\n\t".join(["/**", " * {@inheritdoc}", "*/"]) + "\n\t" + method

            method_stub = template.format(method)
            self.view.run_command("create", {"stub": method_stub, "offset": point})
