import os
import configparser
import re
import libs.Groups as Groups
import libs.Group as Group
import libs.Shortcut as Shortcut
import libs.Parser as Parser

class KDE_Dolphin(Parser.Parser):
    def __init__(self):
        description = {
            "name" : "KDE Dolphin shortcut",
            "category": "Desktop environment",
            "desktop": "KDE",
            "file": '',
            "groups_supported": False,
        }
        super(KDE_Dolphin, self).__init__(description)

    def parse(self, default_group = None, overriden_file=None):
        super().parse(default_group, overriden_file)
        if self.error:
            return False
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(self.file)
        group = Group.Group(default_group)
        for desc in config['Shortcuts']:
            nice_name = desc.replace('_', ' ').capitalize()
            key = config['Shortcuts'][desc]
            if key != 'none':
                shortcut = Shortcut.Shortcut()
                shortcut.set_label(nice_name)
                shortcut.set_shortcut(key)
                shortcut.set_source(self.name)
                group.add_shortcut(shortcut)
        self.groups.add_group(group)
        return True
