
import os
import re
import libs.Config as Config
from prettytable import PrettyTable
import importlib

class Parsers():
    def __init__(self):
        self.parsers = []
        parser_files = self.get_parser_files()
        for parser_file in parser_files:
            module = importlib.import_module('parsers.'+parser_file)
            class_name = getattr(module, parser_file)
            instance = class_name()
            self.parsers.append(instance)

    def get_parser_files(self):
        path = os.path.dirname(__file__)+'/../parsers/'
        files = []
        for p in os.listdir(path):
            if os.path.isfile(os.path.join(path, p)):
                if p != '__init__.py':
                    module = p.replace('.py', '')
                    files.append(module)

        return files

    def output_table(self):
        table = PrettyTable(["\033[33mID\033[0m", "\033[33mParser\033[0m", "\033[33mCategory\033[0m", "\033[33mDesktop\033[0m", "\033[33mFile\033[0m", "\033[33mGroup support\033[0m"])

        table.align = "l"
        for idx, parser in enumerate(self.parsers):
            table.add_row([idx+1, parser.name, parser.category, parser.desktop, parser.file, parser.groups_supported])
        print(table)

    def import_shortcuts(self, parser_index, to_group, overriden_file, to_tab, prefix, filter_group, filter_name, filter_value):
        found = False
        parser = self.parsers[int(parser_index)-1]
    
        if not parser:
            print('This parser with index {} does not exist'.format(parser_index))
            return

        if to_tab:
            config = Config.Config()
            if not config.is_tab_exists(to_tab):
                print('The tab {} does not exist').format(to_tab)
                return

        if not to_group and not prefix:
            print('You need to specify a prefix with the -p option to avoid a group to be overwritten if it has the same name as an existing one')
            return

        ret = parser.parse(to_group, overriden_file)
        if ret == False:
            print(parser.error_reason)
            return

        parser.filter(filter_group, filter_name, filter_value)

        if not to_group:
            parser.set_prefix(prefix)

        parser.save()

        if to_tab:
            parser.associate_to_tab(to_tab)
        else:
            parser.associate_to_tab('Default')

        return True
        # for parser in self.parsers:
        #     if parser.name == parser_name:
        #         found = True
        #         ret = parser.parse(to_group)
        #         if ret == False:
        #             print(parser.error_reason)
        # if not found:
        #     print("The parser '{}' does not exist".format(parser_name))


