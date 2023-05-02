#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication
import sys
import argparse
import libs.Parsers as Parsers
import libs.Config as Config
import libs.Tabs as Tabs
import libs.Manage as Manage
import libs.Gui as Gui

VERSION="1.0.0"

parsers = Parsers.Parsers()

parser = argparse.ArgumentParser(description="Kebihelp - The universal keybinder helper")

parser.add_argument("-v", "--version", dest="version", action="store_true", help="Show the current version")
subparsers = parser.add_subparsers(dest="command", help="Main action to perform")


parser_import = subparsers.add_parser('import', help='Import new keybindings')
parser_import.add_argument('-l', action="store_true", dest="show_parsers", help="Show the available parsers")
parser_import.add_argument('-i', dest="index_parser", help="The ID of the supported parser")
parser_import.add_argument('-p', dest="import_prefix", help="The prefix for the groups that will be created")
parser_import.add_argument("-g", dest="import_group", help="Associate the imported keybindings to a particular group")
parser_import.add_argument("-f", dest="import_file", help="Override the filename to import")
parser_import.add_argument("-t", dest="import_to_tab", help="Associated the imported shortcuts to a particular tab")
parser_import.add_argument("-fg", "--group", dest="import_filter_group", help="Select a particular group")
parser_import.add_argument("-fn", "--name", dest="import_filter_name", help="A part of the particular keybinding name to match")
parser_import.add_argument("-fk", "--keybinding", dest="import_filter_key", help="A part of the particular keybinding value to match")

parser_keys= subparsers.add_parser('keys', help='List the existing keybindings')
parser_keys.add_argument("-fg", "--group", dest="keys_group", help="Select a particular group")
parser_keys.add_argument("-fs", "--source", dest="keys_source", help="Select a particular source")
parser_keys.add_argument("-fn", "--name", dest="keys_name", help="A part of the particular keybinding name to match")
parser_keys.add_argument("-fk", "--keybinding", dest="keys_key", help="A part of the particular keybinding value to match")
parser_keys.add_argument("-a", "--all", dest="keys_all", help="Show also disabled keybindings")
parser_keys.add_argument("-t", "--tab", dest="keys_tab", help="Select the tab")


parser_tabs = subparsers.add_parser('tabs', help='List the tabs')

parser_manage = subparsers.add_parser('manage', help='Manage keybindings')
parser_manage.add_argument('-a', required=True, choices=['associate', 'dissociate', 'hidetab', 'unhidetab', 'disablegroup', 'enablegroup'], dest="manage_action", help="Action to perform")
parser_manage.add_argument('-g', dest="manage_groups", help="Input groups")
parser_manage.add_argument('-t', dest="manage_tab", help="Target tab")


parser_show = subparsers.add_parser('show', help='Show the keybindings')
parser_show.add_argument("-t", "--tab", dest="show_tab", help="Show the keybindings only associated to this tab")

args = parser.parse_args()

if args.version:
    print("kebihelp.py - v"+VERSION)
    exit(0)

if not args.command:
    parser.print_usage()
    exit(0)

if args.command == "tabs":
    tabs = Tabs.Tabs()
    tabs.output_table()
    exit(0)

if args.command == 'import':
    if args.show_parsers:
        parsers.output_table()
        exit(0)
    if not args.index_parser:
        parser_import.print_usage()
    else:
        parsers.import_shortcuts(args.index_parser, args.import_group, args.import_file, args.import_to_tab, args.import_prefix, args.import_filter_group, args.import_filter_name, args.import_filter_key)

if args.command == 'keys':
    config = Config.Config()
    groups = config.get_groups(args.keys_tab)
    groups.output_table(args.keys_group, args.keys_source, args.keys_name, args.keys_key, args.keys_all, args.keys_tab)

if args.command == 'manage':
    manage = Manage.Manage()
    if args.manage_action == 'associate':
        manage.associate_to_tab(args.manage_tab, args.manage_groups)
    if args.manage_action == 'dissociate':
        manage.dissociate_from_tab(args.manage_tab, args.manage_groups)
    if args.manage_action == 'hidetab':
        manage.hide_tab(args.manage_tab)
    if args.manage_action == 'unhidetab':
        manage.unhide_tab(args.manage_tab)
    if args.manage_action == 'disablegroup':
        manage.disable_group(args.manage_groups)
    if args.manage_action == 'enablegroup':
        manage.enable_group(args.manage_groups)

if args.command == 'show':
    app = QApplication(sys.argv)
    window = Gui.MainWindow(args.show_tab)
    window.show()
    app.exec()
