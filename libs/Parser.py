import libs.Config as Config
import libs.Groups as Groups
import os

class Parser():
    def __init__(self, description):
        self.name = description['name']
        self.category = description['category']
        self.desktop = description['desktop']
        self.file = os.path.expanduser(description['file'])
        self.groups_supported = description['groups_supported']
        self.error = False
        self.error_reason = ""
        self.groups = Groups.Groups()

    def parse(self, default_group = None, overriden_file=None):
        if not self.groups_supported and default_group == None:
            self.error = True
            self.error_reason = "Error: No default group specified"
            return 
        filename = self.file
        print(overriden_file)
        if filename == '' and not overriden_file:
            self.error = True
            self.error_reason = "No file specified. You probably need to export the shortcuts and use it as the input with the -f option"
            return
        if overriden_file:
            filename = os.path.expanduser(overriden_file)
        if not os.path.isfile(filename):
            self.error = True
            self.error_reason = "Error: The file does not exist"
            return
        if overriden_file:
            self.file = filename

    def filter(self, filter_group, filter_name, filter_value):
        self.groups.filter(filter_group, filter_name, filter_value)

    def save(self):
        config = Config.Config()
        config.save_groups(self.groups)
