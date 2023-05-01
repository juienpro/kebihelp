import libs.QuickRefParser as Parser

class Brave_Default(Parser.Parser):
    def __init__(self):
        description = {
            "name" : "Brave Browser Default Shortcuts",
            "category": "Browser",
            "desktop": "All",
            "url": 'https://quickref.me/brave',
        }
        super(Brave_Default, self).__init__(description)

    def parse(self, default_group = None, overriden_file=None):
        super().parse(default_group)
