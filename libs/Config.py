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
                "test": "toto"
            },
            'Templates': {
                'default': {
                    'n_columns': 3,
                    'spacing': 3,
                    'background_color': '#282C34',
                    'width': 1200,
                    'height': 900,
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
                    'include': 'All',
                    'exclude': [],
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

    def get_templates(self):
        return self.config['Templates']
    
    def get_template(self, template_name):
        if template_name in self.config['Templates']:
            return self.config['Templates'][template_name]
        else:
            print("Error: cannot find the template {}".format(template_name))
            exit(1)

    def get_current_template(self, template=None):
        if template:
            if template in self.config['Templates']:
                return self.config['Templates'][template]
            else:
                print("Error: cannot find the template {}".format(template))
                exit(1)
        else:
            try:
                ret = subprocess.check_output(self.config['Parameters']['cmd_focused_window'], shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                print("Command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                exit(1)
            ret = ret.decode('utf-8')
            print(ret)
            for window_name in self.config['Rules']:
                if ret in window_name:
                    if self.config['Rules'][window_name] in self.config['Templates']:
                        return self.config['Templates'][window_name]
                    else:
                        print("The template {} cannot be found".format(window_name))
            return self.config['Templates']["default"]

    # def get_window_layout(self):
    #     return self.config['Options']['window_layout']

    # def get_groups_layout(self):
    #     return self.config['Options']['groups_layout']

    def save_groups(self, groups):
        for group_name in groups.groups:
            print(groups.groups[group_name].label)
            if not group_name in self.config['Shortcuts']:
                self.config['Shortcuts'][group_name] = {
                    '_enabled': True
                }
            for shortcut in groups.groups[group_name].shortcuts:
                self.config['Shortcuts'][group_name][shortcut.label] = [shortcut.value, shortcut.enabled, shortcut.source]
                self.save()

    def get_groups(self, template):
        groups = Groups.Groups()
        for group_name in self.config['Shortcuts']:
            group = Group.Group(group_name, self.config['Shortcuts'][group_name]['_enabled'])
            if not group.is_in_template(template):
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

