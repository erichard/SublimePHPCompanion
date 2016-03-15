import sublime
import sublime_plugin

from ..settings import get_setting

class InsertPhpConstructorPropertyCommand(sublime_plugin.TextCommand):
    'Inserts a constructor argument that sets a property.'

    placeholder = 'PROPERTY'

    def description(self):
        'The description of the command.'
        return 'Insert a constructor argument.'

    def is_enabled(self):
        'Whether the command is available or not.'
        return 'php' in self.view.settings().get('syntax').lower()

    def run(self, edit):
        'Run the command.'
        self.edit = edit
        self.regions = []
        self.visibility = get_setting('visibility', 'private')

        self.add_property(self.placeholder)
        self.add_constructor(self.placeholder)

        # make a multiselect for all the variable names
        sel = self.view.sel()
        sel.clear()
        sel.add_all(self.regions)

        # scroll the view to the selections
        self.view.show(sel)

    def add_property(self, prop_name):
        'Add a property to the class we are editing.'
        text = prop_name + ";"
        properties = self.find_properties()

        # check if the class has existing properties. if not, we need an extra
        # newline to separate the property from any existing methods
        if properties:
            pos = properties[-1].end()
        else:
            pos = self.find_class_opening_bracket()
            text += "\n"

        pos += self.view_insert(pos, "\n\t"+self.visibility+" $")
        self.view_insert(pos, text)

        cursor_start = pos
        cursor_end = cursor_start + len(prop_name)
        self.add_region(cursor_start, cursor_end)

    def add_constructor(self, prop_name):
        'Add constructor argument and setter.'
        constructor = self.view.find(r'__construct\s*\(', 0)

        if constructor:
            constructor_start = constructor.end()
            constructor_end = self.view.find(r'\)', constructor_start).begin()
        # create the constructor if it does not exist
        else:
            text = "\n\tpublic function __construct()\n\t{\n\t}"
            properties = self.find_properties()

            # if the class has any properties, insert an extra newline and put
            # the constructor right after the last property
            if properties:
                pos = properties[-1].end()
                text = "\n" + text
            # otherwise, find the opening { of the class and put it there
            else:
                pos = self.find_class_opening_bracket()

            self.view_insert(pos, text)

            # easier than calculating the positions
            constructor = self.view.find(r'__construct\s*\(\)', 0)
            constructor_start = constructor_end = constructor.end() - 1

        constructor_args = self.view.substr(sublime.Region(constructor_start, constructor_end))
        arg_pos = constructor_end
        text = "$" + prop_name

        # figure out if the constructor is multiline
        last_newline = self.view.find_by_class(constructor_end, False, sublime.CLASS_LINE_END)
        last_word = self.view.find_by_class(constructor_end, False, sublime.CLASS_SUB_WORD_START)
        is_multiline_constructor = last_newline > last_word

        if is_multiline_constructor:
            arg_pos = last_newline

            # append a comma if there are any other arguments
            if constructor_args.strip() != '':
                arg_pos += self.view_insert(arg_pos, ",")

            # insert a newline and indent before inserting the argument
            arg_pos += self.view_insert(arg_pos, "\n\t\t")
            cursor_start = arg_pos + 1
        else:
            # when substitution is done, cursor will be past the point where the
            # closing parenthesis of the constructor currently is
            cursor_start = constructor_end + 1

            # prepend a comma if there are any other arguments
            if constructor_args.strip() != '':
                text = ", " + text
                cursor_start += 2

        # insert and add selection for the constructor argument name
        self.view_insert(arg_pos, text)
        cursor_end = cursor_start + len(prop_name)
        self.add_region(cursor_start, cursor_end)

        # add the line of code that sets the property
        constructor_close = self.view.find(r'\}', constructor_end).begin()
        last_newline = self.view.find_by_class(constructor_close, False, sublime.CLASS_LINE_START)
        cursor_start = last_newline + self.view_insert(last_newline, "\t\t$this->")
        self.view_insert(cursor_start, prop_name+' = $'+prop_name+";\n")

        # add selection for the property name
        cursor_end = cursor_start + len(prop_name)
        self.add_region(cursor_start, cursor_end)

        # add selection for the variable name
        cursor_start = cursor_end + 4
        cursor_end = cursor_start + len(prop_name)
        self.add_region(cursor_start, cursor_end)

    def find_class_opening_bracket(self):
        'Find the position of the opening bracket of the class block.'
        pos = self.view.find(r'class\s+[0-9A-Za-z_]+', 0).end()
        return self.view.find(r'\{', pos).end()

    def find_properties(self):
        'Find all the class properties defined in the current view.'
        return self.view.find_all(r'(public|protected|private)\s+\$[A-Za-z_]+;')

    def add_region(self, start, end):
        'Add a region to be edited later.'
        self.regions.append(sublime.Region(start, end))

    def view_insert(self, pos, text):
        'Insert a string into the view.'
        return self.view.insert(self.edit, pos, text)
