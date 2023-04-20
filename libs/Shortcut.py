
class Shortcut():
    def __init__(self):
        self.label = ""
        self.value = ""
        self.source = ""
        self.enabled = True
        self.group = False

    def set_label(self, label):
        self.label = label

    def set_shortcut(self, value):
        self.value = value

    def set_enabled(self, enabled):
        self.enabled = enabled

    def set_source(self, name):
        self.source = name

    def add_to_group(self, group):
        self.group = group
        group.add_shortcut(self)
