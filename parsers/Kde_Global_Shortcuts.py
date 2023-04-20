
import os
import configparser
import re
import libs.Groups as Groups
import libs.Group as Group
import libs.Shortcut as Shortcut
import libs.Parser as Parser

class Kde_Global_Shortcuts(Parser.Parser):
    def __init__(self):
        description = {
            "name" : "KDE Global Shortcuts",
            "category": "Desktop environment",
            "desktop": "KDE",
            "file": '~/.config/kglobalshortcutsrc',
            "groups_supported": True,
        }
        super(Kde_Global_Shortcuts, self).__init__(description)

    def parse(self, default_group = None, overriden_file=None):
        super().parse(default_group, overriden_file)
        if self.error:
            return False

        config = configparser.ConfigParser(interpolation=None)
        config.read(self.file)

        if default_group:
           group = Group.Group(default_group)
           # self.groups.add_group(group)
        for section in config.sections():
            if not default_group:
                group = Group.Group(config[section]['_k_friendly_name'])
                # self.groups.add_group(group)

            for key in config[section]:
                value = config[section][key]
                params = value.split(',')
                if len(params) > 2:
                    if (params[0] not in ['none', '']):
                        shortcut = Shortcut.Shortcut()
                        shortcut.set_label(params[2])
                        shortcut.set_shortcut(params[0])
                        shortcut.set_source(self.name)
                        group.add_shortcut(shortcut)

            self.groups.add_group(group)
        return True
