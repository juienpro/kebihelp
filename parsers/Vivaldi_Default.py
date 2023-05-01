import os
import configparser
import re
import libs.Groups as Groups
import libs.QuickRefParser as Parser

class Vivaldi_Default(Parser.Parser):
    def __init__(self):
        description = {
            "name" : "Vivaldi Browser Default Shortcuts",
            "category": "Browser",
            "desktop": "All",
            "url": 'https://quickref.me/vivaldi',
        }
        super(Vivaldi_Default, self).__init__(description)

    def parse(self, default_group = None, overriden_file=None):
        super().parse(default_group)
