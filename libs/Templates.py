from prettytable import PrettyTable
import libs.Config as Config

class Templates():
    def __init__(self):
        config = Config.Config()
        self.templates = config.get_templates()

    def output_table(self):
        table = PrettyTable(["\033[33mID\033[0m", "\033[33mTemplate\033[0m", "\033[33mWindow N_cols\033[0m", "\033[33mWindow direction\033[0m", "\033[33mGroups N_Cols\033[0m", "\033[33mGroups direction\033[0m"])
        index = 1
        for template_name in self.templates:
            table.add_row([
                index,
                template_name,
                self.templates[template_name]['window_layout']['n_columns'],
                self.templates[template_name]['window_layout']['fill_direction'],
                self.templates[template_name]['groups_layout']['n_columns'],
                self.templates[template_name]['groups_layout']['fill_direection'],
            ])
            index += 1
        print(table)
