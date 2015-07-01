import sublime

def filename():
    return 'PHP Companion.sublime-settings'

def get_setting(name, default=None):
    project_data = sublime.active_window().project_data();

    if (project_data != None):
        v = project_data.get("phpcompanion", {}).get(name, None)
        if v != None:
            return v
        else:
            return sublime.load_settings(filename()).get(name, default)
    else:
        return None
