import os
import configparser
import re
import libs.Groups as Groups
import libs.Group as Group
import libs.Shortcut as Shortcut
import libs.Parser as Parser

class Kde_Custom_Shortcuts(Parser.Parser):
    def __init__(self):
        description = {
            "name" : "KDE Custom Shortcuts",
            "category": "Desktop environment",
            "desktop": "KDE",
            "file": '~/.config/khotkeysrc',
            "groups_supported": False,
        }
        super(Kde_Custom_Shortcuts, self).__init__(description)

    def parse(self, default_group = None, overriden_file=None):
        super().parse(default_group, overriden_file)
        if self.error:
            return False

        # config = configparser.ConfigParser(interpolation=None, allow_no_value=True)
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(self.file)

        main_sections = {}
        for section in config.sections():
            if config.has_option(section, 'Name') and config.has_option(section, 'Enabled'):
                if config[section]['Enabled'] == 'true':
                    if config[section]['Type'] == 'SIMPLE_ACTION_DATA':
                        main_sections[section] = {'name': config[section]['Name']}

        for section in main_sections:
            if config.has_section(section+'Triggers0'):
                if config.has_option(section+'Triggers0', 'KEY'):
                    key = config[section+'Triggers0']['KEY']
                    if key.strip() != '':
                        main_sections[section]['key'] = key.strip()

        group = Group.Group(default_group)
        for section in main_sections:
            if 'key' in main_sections[section]:
                if main_sections[section]['key'] != '':
                    shortcut = Shortcut.Shortcut()
                    shortcut.set_label(main_sections[section]['name'])
                    shortcut.set_shortcut(main_sections[section]['key'])
                    shortcut.set_source(self.name)
                    group.add_shortcut(shortcut)
        self.groups.add_group(group)
        return True
