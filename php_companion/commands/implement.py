import sublime, sublime_plugin

class ImplementCommand(sublime_plugin.TextCommand):

    # Gets the currently selected symbol
    #
    def get_selected_symbol(self):
        point = self.view.sel()[0]
        region = self.view.word(point)
        return self.view.substr(region)

    # Gets files with names that match the currently selected symbol
    #
    def get_matching_files(self):
        window = self.view.window()
        selected_symbol = self.get_selected_symbol()
        locations = window.lookup_symbol_in_index(selected_symbol)

        files = []
        for location in locations:
            files.append(location[0])
        return files

    # Handles the selection of a quick panel item
    #
    def on_done(self, index):
        if index == -1:
            return

        self.view.run_command("parse", {"path": self.files[index]})

    # Runs the plugin
    #
    def run(self, edit):
        self.files = self.get_matching_files()

        if (len(self.files) == 1):
            self.view.run_command("parse", {"path": self.files[0]})

        if (len(self.files) > 1):
            self.view.window().show_quick_panel(self.files, self.on_done)
