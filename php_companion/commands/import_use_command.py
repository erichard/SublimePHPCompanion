import sublime
import sublime_plugin

from ..settings import get_setting

class ImportUseCommand(sublime_plugin.TextCommand):
    def run(self, edit, namespace):
        self.namespace = namespace

        if self.is_already_used():
            return self.view.show_popup('Use already exist!',
                                        flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY)

        self.insert_use(edit)

    def insert_use(self, edit):
        if self.is_first_use():
            for location in [r"^\s*namespace\s+[\w\\]+[;{]", r"<\?php"]:
                inserted = self.insert_first_use(location, edit)

                if inserted:
                    break
        else:
            self.insert_use_among_others(edit)

    def insert_first_use(self, where, edit):
        region = self.view.find(where, 0)
        if not region.empty():
            line = self.view.line(region)
            self.view.insert(edit, line.end(), "\n\n" + self.build_uses())
            self.view.show_popup('Successfully imported ' + self.namespace,
                                 flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY)
            return True

        return False

    def insert_use_among_others(self, edit):
        regions = self.view.find_all(r"^(use\s+.+[;])", 0)
        if len(regions) > 0:
            region = regions[0]
            for r in regions:
                region = region.cover(r)

            self.view.replace(edit, region, self.build_uses())
            self.view.show_popup('Successfully imported ' + self.namespace,
                                 flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY)

    def build_uses(self):
        uses = []
        use_stmt = "use " + self.namespace + ";"

        self.view.find_all(r"^(use\s+.+[;])", 0, '$1', uses)
        uses.append(use_stmt)
        uses = list(set(uses))
        uses.sort()
        if get_setting("use_sort_length"):
            uses.sort(key = len)

        return "\n".join(uses)

    def is_already_used(self):
        region = self.view.find(("use " + self.namespace + ";").replace('\\', '\\\\'), 0)
        return not region.empty()

    def is_first_use(self):
        return len(self.view.find_all(r"^(use\s+.+[;])", 0)) == 0
