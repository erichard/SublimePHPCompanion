import sublime_plugin

class ImportUseCommand(sublime_plugin.TextCommand):
    def run(self, edit, namespace):
        view = self.view
        use_stmt = "use " + namespace + ";"

        region = view.find(use_stmt.replace('\\', '\\\\'), 0)
        if not region.empty():
            return sublime.status_message('Use already exist !')

        uses = []
        regions = view.find_all(r"^(use\s+.+[;])", 0, '$1', uses)
        uses.append(use_stmt)
        uses = list(set(uses))
        uses.sort()
        uses = "\n".join(uses)

        if len(regions) > 0:
            region = regions[0]
            for r in regions:
                region = region.cover(r)

            view.replace(edit, region, uses)
            return sublime.status_message('Successfully imported' + namespace)

        region = view.find(r"^\s*namespace\s+[\w\\]+[;{]", 0)
        if not region.empty():
            line = view.line(region)
            view.insert(edit, line.end(), "\n" + uses)
            return sublime.status_message('Successfully imported' + namespace)

        region = view.find(r"<\?php", 0)
        if not region.empty():
            line = view.line(region)
            view.insert(edit, line.end(), "\n" + uses)
            return sublime.status_message('Successfully imported' + namespace)