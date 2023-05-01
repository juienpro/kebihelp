import libs.QuickRefParser as Parser

class Chrome_Default(Parser.Parser):
    def __init__(self):
        description = {
            "name" : "Chrome Browser Default Shortcuts",
            "category": "Browser",
            "desktop": "All",
            "url": 'https://quickref.me/google-chrome',
        }
        super(Chrome_Default, self).__init__(description)

    def parse(self, default_group = None, overriden_file=None):
        super().parse(default_group)
