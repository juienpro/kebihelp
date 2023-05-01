from prettytable import PrettyTable
import libs.Config as Config

class Tabs():
    def __init__(self):
        self.config = Config.Config()
        self.tabs = self.config.get_tabs()

    def output_table(self):
        table = PrettyTable(["\033[33mID\033[0m", "\033[33mTab\033[0m", "\033[33mInclude\033[0m", "\033[33m# Groups\033[0m", "\033[33m# Shortcuts\033[0m"])
        index = 1
        for tab_name in self.tabs:
            include = ', '.join(self.tabs[tab_name]['include'])

            groups = self.config.get_groups(tab_name)
            n_shortcuts = 0
            for group in groups.groups:
               n_shortcuts += len(groups.groups[group].shortcuts)
            table.add_row([
                index,
                tab_name,
                include,
                len(groups.groups),
                n_shortcuts
            ])
            index += 1
        print(table)
