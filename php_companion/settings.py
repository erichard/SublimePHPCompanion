import sublime

def filename():
    return 'PHP Companion.sublime-settings'

def get_setting(name, default=None):
    project_data = sublime.active_window().project_data()

    # setting in run time
    view_setting = sublime.active_window().active_view().settings().get(name, None)
    if view_setting != None:
        return view_setting

    if (project_data and 'phpcompanion' in project_data and
            name in project_data['phpcompanion']):
        return project_data['phpcompanion'][name]

    return sublime.load_settings(filename()).get(name, default)
