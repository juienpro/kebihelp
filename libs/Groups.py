import libs.Group as Group
import libs.Shortcut as Shortcut
from prettytable import PrettyTable

class Groups():
    def __init__(self):
        self.groups = {}

    def add_group(self, group):
        if group.label not in self.groups:
            self.groups[group.label] = group

    def remove_group(self, name):
        if name in self.groups:
            del self.groups[name]

    def filter(self, filter_group, filter_name, filter_value):
        new_groups = {}
        for group_name in self.groups:
            if filter_group and group_name != filter_group:
                continue
            new_groups[group_name] = Group.Group(group_name)
            for shortcut in self.groups[group_name].shortcuts:
                if filter_name and filter_name not in shortcut.label:
                    continue
                if filter_value and filter_value not in shortcut.value:
                    continue
                new_groups[group_name].add_shortcut(shortcut)
        self.groups = new_groups

    def set_prefix(self, prefix):
        new_groups = {}
        for group_name in self.groups:
            new_name = "{}-{}".format(prefix, group_name)
            new_groups[new_name] = self.groups[group_name]
        self.groups = new_groups

    def output_table(self, group = None, source = None, name=None, key=None, show_disabled=None, tab=None):
        table = PrettyTable(["\033[33mID\033[0m", "\033[33mGroup\033[0m", "\033[33mLabel\033[0m", "\033[33mKey\033[0m", "\033[33mEnabled\033[0m", "\033[33mSource\033[0m"])
        index = 1
        for group_name in self.groups:
            if not self.groups[group_name].is_in_tab(tab):
                continue
            if group and (group not in group_name):
                continue
            for shortcut in self.groups[group_name].shortcuts:
                if source and source not in shortcut.source:
                    continue
                if name and name not in shortcut.label:
                    continue
                if key and key not in shortcut.value:
                    continue
                if not show_disabled and not shortcut.enabled:
                    continue
                table.add_row([index, group_name, shortcut.label, shortcut.value, shortcut.enabled, shortcut.source])
                index += 1
        print(table)
