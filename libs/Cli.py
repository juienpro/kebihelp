
from prettytable import PrettyTable

def print_shortcuts(shortcuts):
    table = PrettyTable(["\033[33mSection\033[0m", "\033[33mAction\033[0m", "\033[33mKeybinding\033[0m", "\033[33mDefault\033[0m", "\033[33mHidden\033[0m"])
    R = "\033[0;31;40m" #RED
    G = "\033[0;32;40m" # GREEN
    Y = "\033[0;33;40m" # Yellow
    B = "\033[0;34;40m" # Blue
    N = "\033[0m" # Reset
    table.align = "l"
    for sect in shortcuts:
        hidden = shortcuts[sect]['hidden']
        for shortcut in shortcuts[sect]['shortcuts']:
            is_hidden = hidden or shortcut['hidden']
            table.add_row([sect, shortcut['label'], shortcut['key'], shortcut['default'], is_hidden])
    print(table)

