
import libs.Config as Config


class Manage():
    def __init__(self):
        config = Config.Config()
        self.config = config.config

    def save(self):
        config = Config.Config()
        config.config = self.config
        config.save()

    def create_tab(self, tab_name):
        if tab_name not in self.config['Tabs']:
            self.config['Tabs'][tab_name] = { "visible": True, "include": []}

    def associate_to_tab(self, tab_name, group_mask):
        self.create_tab(tab_name)
        for group_name in self.config['Shortcuts']:
            if group_mask in group_name:
                self.config['Tabs'][tab_name]['include'].append(group_name)
        self.save()

    def dissociate_from_tab(self, tab_name, group_mask):
        if tab_name not in self.config['Tabs']:
            print("The tab {} does not exist".format(tab_name))
            exit(1)

        groups_to_add = []
        for group_name in self.config['Tabs'][tab_name]['include']:
            if group_mask not in group_name:
                groups_to_add.append(group_name)
        self.config['Tabs'][tab_name]['include'] = groups_to_add
        self.save()

    def hide_tab(self, tab_name):
        if tab_name not in self.config['Tabs']:
            print("The tab {} does not exist".format(tab_name))
            exit(1)
        self.config['Tabs'][tab_name]['visible'] = False
        self.save()

    def unhide_tab(self, tab_name):
        if tab_name not in self.config['Tabs']:
            print("The tab {} does not exist".format(tab_name))
            exit(1)
        self.config['Tabs'][tab_name]['visible'] = True
        self.save()

    def disable_group(self, group_name):
        for group in self.config['Shortcuts']:
            name = group
            if '-' in group:
                sections = group.split('-')
                name = sections[1]
            if group_name == group or group_name == name:
                self.config['Shortcuts'][group]['_enabled'] = False

        self.save()

    def enable_group(self, group_name):
        for group in self.config['Shortcuts']:
            name = group
            if '-' in group:
                sections = '-'.split(group)
                name = sections[1]
            if group_name == group or group_name == name:
                self.config['Shortcuts'][group]['_enabled'] = True

        self.save()
