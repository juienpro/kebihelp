import libs.QuickRefParser as Parser

class Gmail_Default(Parser.Parser):
    def __init__(self):
        description = {
            "name" : "Gmail Default Shortcuts",
            "category": "App",
            "desktop": "All",
            "url": 'https://quickref.me/gmail',
        }
        super(Gmail_Default, self).__init__(description)

    def parse(self, default_group = None, overriden_file=None):
        super().parse(default_group)
