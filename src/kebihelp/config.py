import os
import json
import subprocess
from prettytable import PrettyTable
# import libs.Groups as Groups
# import libs.Group as Group
# import libs.Shortcut as Shortcut

CONFIG_FILE = "~/.config/kebihelp/conf.json"

class Config():
    def __init__(self):
        config_file = os.path.expanduser(CONFIG_FILE)
        if (not os.path.isfile(config_file)):
            self.config = self.default()
            self.save()
        with open(config_file) as f:
            self.config = json.load(f)

    def default(self):
        return {
            'Parameters': {
                'cmd_focused_window': "hyprctl activewindow",
                "importer": {
                      "match_line": ".*::(.+?)::(.+?)::(.+?)::.*",
                      "position_group": 1,
                      "position_keybinding": 2,
                      "position_label": 3
                },
                "keys": {
                    "tab_previous": "Backtab", 
                    "tab_next": "Tab",
                    "scroll_down": "Down",
                    "scroll_up": "Up",
                    "quit": "Esc"
                },
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
            'Rules': {
                'default': 'default'
            },
            'Keybindings': {}
        }
    def save(self):
        config_file = os.path.expanduser(CONFIG_FILE)
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def add_keybinding(self, tab, group, keybinding, description):
        print("Importing keybinding to tab {}: Group {} - {} - {}".format(tab, group, keybinding, description))
        if not tab in self.config['Keybindings']:
            self.config['Keybindings'][tab] = {
                '_hidden': False,
            }

        if not group in self.config['Keybindings'][tab]:
            self.config['Keybindings'][tab][group] = { '_hidden': False, 'keybindings': [] } 
        
        found = False
        for idx, k in enumerate(self.config['Keybindings'][tab][group]['keybindings']):
            if k['value'] == keybinding:
                found = True
                self.config['Keybindings'][tab][group]['keybindings'][idx]['label'] = description
        if not found: 
            self.config['Keybindings'][tab][group]['keybindings'].append({
                'value': keybinding,
                'label': description
        })

    
    def output_table(self, tab_selection):
        table = PrettyTable(["\033[33mTab\033[0m", "\033[33mGroup\033[0m", "\033[33mKey\033[0m", "\033[33mLabel\033[0m", "\033[33mHidden\033[0m"])
        for tab_name, tab_conf in self.config['Keybindings'].items():
            if tab_selection != None and tab_selection != tab_name:
                continue
            hidden = False
            if '_hidden' in tab_conf and tab_conf['_hidden']:
                hidden = True 
            for group_name, group_conf in self.config['Keybindings'][tab_name].items():
                if group_name == '_hidden':
                    continue
                if '_hidden' in group_conf and group_conf['_hidden']:
                    hidden = True
                for keybinding in group_conf['keybindings']:
                    if '_hidden' in keybinding and keybinding['_hidden']:
                        hidden = True
                    table.add_row([tab_name, group_name, keybinding['value'], keybinding['label'], hidden])
        print(table)

