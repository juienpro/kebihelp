import os
import json
import subprocess
import libs.Groups as Groups
import libs.Group as Group
import libs.Shortcut as Shortcut

CONFIG_FILE = "~/.config/keybindingshelper.ini"

class Config():
    def __init__(self):
        config_file = os.path.expanduser(CONFIG_FILE)
        if (not os.path.isfile(config_file)):
            self.config = self.default()
            self.save()
        with open(config_file) as f:
            self.config = json.load(f)
        # self.config = ConfigObj(path, {"create_empty":True})
            
        # if 'Options' not in self.config:
        #     self.config['Options'] = {
        #         'window_layout': {
        #             'n_columns': 2,
        #             'fill_direction': 'horizontal'
        #         },
        #         'groups_layout': {
        #             'n_columns': 1,
        #             'fill_direction': 'vertical'
        #         },
        #         "background_color": 'rgba(0, 120, 185, 60)',
        #     }
            # self.config['Shortcuts'] = {}
        # self.config.write()

    def default(self):
        return {
            'Parameters': {
                'cmd_focused_window': "xdotool getwindowfocus getwindowname",
                "layout": {
                    'n_columns': 3,
                    'spacing': 3,
                    'background_color': '#282C34',
                    "opacity": 0.95,
                    "tabs": {
                        "background_color": "#30343D",
                        "background_color_current": "#4F5564",
                        "color": "#FFFFFF",
                        "font": "Lato",
                        "font_size": 8,
                        "padding": 0
                    },
                    'group_name': {
                        'background_color': '#FF0000',
                        'color': '#000000',
                        'bold': True,
                        'stretched': False,
                        "padding": "0px 5px 0px 2px",
                        "font": "Lato",
                        "font_size": 8
                    },
                    "shortcut": {
                        "label": {
                          "color": "#EEEEEE",
                          "bold": False,
                          "font": "Lato",
                          "font_size": 8
                        },
                        "value": {
                          "color": "#EEEEEE",
                          "bold": True,
                          "font": "Lato",
                          "font_size": 8
                        },
                        "spacing": 5
                    },
                }
            },
            'Tabs': {
                'Default': {
                    'visible': True,
                    'include': []
                }
            },
            'Rules': {
                'default': 'default'
            },
            'Shortcuts': {}
        }
    def save(self):
        config_file = os.path.expanduser(CONFIG_FILE)
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get_tabs(self):
        return self.config['Tabs']

    def is_tab_exists(self, name):
        if name in self.config['Tabs']:
            return True
        return False

    def get_tab(self, tab_name):
        if tab_name in self.config['Tabs']:
            return self.config['Tabs'][tab_name]
        else:
            print("Error: cannot find the Tab {}".format(tab_name))
            exit(1)

    def get_default_tab(self):
        should_get_window_name = False
        tab = "Default"
        for window_name in self.config['Rules']:
            if window_name != 'default':
                should_get_window_name = True
        if should_get_window_name:
            try:
                ret = subprocess.check_output(self.config['Parameters']['cmd_focused_window'], shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                print("Command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                exit(1)
            ret = ret.decode('utf-8')
            for window_name in self.config['Rules']:
                if window_name in ret:
                    tab = self.config['Rules'][window_name]

            if not self.is_tab_exists(tab):
                print("Tab name {} specified in rule does not exist".format(tab))
        return tab

    def save_groups(self, groups):
        for group_name in groups.groups:
            if not group_name in self.config['Shortcuts']:
                self.config['Shortcuts'][group_name] = {
                    '_enabled': True
                }
            for shortcut in groups.groups[group_name].shortcuts:
                self.config['Shortcuts'][group_name][shortcut.label] = [shortcut.value, shortcut.enabled, shortcut.source]
                self.save()

    def associate_groups_to_tab(self, tab, groups):
        include = self.config['Tabs'][tab]['include']
        for group_name in groups.groups:
            include.append(group_name)
        self.config['Tabs'][tab]['include'] = include
        self.save()

    def get_groups(self, tab = None):
        groups = Groups.Groups()
        for group_name in self.config['Shortcuts']:
            group = Group.Group(group_name, self.config['Shortcuts'][group_name]['_enabled'])
            if tab and not group.is_in_tab(tab):
                continue
            for shortcut_name in self.config['Shortcuts'][group_name]:
                if shortcut_name != '_enabled':
                    shortcut = Shortcut.Shortcut()
                    shortcut.set_label(shortcut_name)
                    shortcut.set_shortcut(self.config['Shortcuts'][group_name][shortcut_name][0])
                    shortcut.set_enabled(self.config['Shortcuts'][group_name][shortcut_name][1])
                    shortcut.set_source(self.config['Shortcuts'][group_name][shortcut_name][2])
                    group.add_shortcut(shortcut)
            groups.add_group(group)
        return groups

    def get_all_groups(self):
        tabs = self.get_tabs()
        all_groups = {}
        for t in tabs:
            all_groups[t] = self.get_groups(t)
        return all_groups
