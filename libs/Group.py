import libs.Config as Config

class Group():
    def __init__(self, label, enabled = True):
        self.label = label
        self.enabled = enabled
        self.shortcuts = []

    def add_shortcut(self, shortcut):
        if not self.is_shortcut_exists(shortcut):
            self.shortcuts.append(shortcut)

    def is_shortcut_exists(self, shortcut):
        for sh in self.shortcuts:
            if shortcut.label == sh.label:
                return True
        return False

    def remove_shortcut(self, shortcut):
        for i, s in enumerate(self.shortcuts):
            if s.label == shortcut.label:
               del self.shortcuts[i]

    def is_in_tab(self, tab):
        if tab == None:
            return True
        config = Config.Config()
        tab_config = config.get_tab(tab)
        include = tab_config['include']
        return self.label in include

