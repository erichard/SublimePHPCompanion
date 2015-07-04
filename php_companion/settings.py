import sublime

def filename():
    return 'PHP Companion.sublime-settings'

def get_setting(name, default=None):
    project_data = sublime.active_window().project_data()

    if (project_data and 'phpcompanion' in project_data and
            name in project_data['phpcompanion']):
        return project_data['phpcompanion'][name]

    return sublime.load_settings(filename()).get(name, default)
