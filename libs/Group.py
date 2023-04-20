import libs.Config as Config

class Group():
    def __init__(self, label, enabled = True):
        self.label = label
        self.enabled = enabled
        self.shortcuts = []

    def add_shortcut(self, shortcut):
        if not self.is_shortcut_exists(shortcut):
            self.shortcuts.append(shortcut)

    def is_shortcut_exists(self, shortcut):
        for sh in self.shortcuts:
            if shortcut.label == sh.label:
                return True
        return False

    def remove_shortcut(self, shortcut):
        for i, s in enumerate(self.shortcuts):
            if s.label == shortcut.label:
               del self.shortcuts[i]

    def is_in_template(self, template):
        if template == None:
            return True
        config = Config.Config()
        template_config = config.get_template(template)
        include = template_config['include']
        exclude = template_config['exclude']

        if isinstance(include, str):
            if include == 'All':
                if template in exclude:
                    return False
                return True
            else:
                print("Error: Invalid value for the include parameter in template {}".format(template))
                exit(1)
        else:
            if template in include:
                return True
        return False

