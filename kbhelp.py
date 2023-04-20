#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication
import sys
import argparse
import libs.Parsers as Parsers
import libs.Config as Config
import libs.Templates as Templates
import libs.Gui as Gui

VERSION="1.0"

parsers = Parsers.Parsers()
# config = Config.Config()
# all_parsers = parser.parsers

# parsers.output_table()
# print(all_parsers)


parser = argparse.ArgumentParser(description="KB Help")

parser.add_argument("-v", "--version", dest="version", action="store_true", help="Show the current version")
# parser.add_argument("-p", "--parsers", dest="parsers", action="store_true", help="Display the list of available parsers")
subparsers = parser.add_subparsers(dest="command", help="Main action to perform")

parser_parsers = subparsers.add_parser('parsers', help="Show the available parsers")

parser_import = subparsers.add_parser('import', help='Import new keybindings')
parser_import.add_argument('-i', dest="index_parser", help="The ID of the supported parser")
parser_import.add_argument("-g", dest="import_group", help="Associate the imported keybindings to a particular group")
parser_import.add_argument("-f", dest="import_file", help="Override the filename to import")
parser_import.add_argument("-fg", "--group", dest="import_filter_group", help="Select a particular group")
parser_import.add_argument("-fn", "--name", dest="import_filter_name", help="A part of the particular keybinding name to match")
parser_import.add_argument("-fk", "--keybinding", dest="import_filter_key", help="A part of the particular keybinding value to match")

parser_keys= subparsers.add_parser('keys', help='Manage the existing keybindings')
parser_keys.add_argument("-l", "--list", dest="list_keys", action="store_true", help="List keybindings")
parser_keys.add_argument("-r", "--remove", dest="remove", action="store_true", help="Remove existing keybindings")
parser_keys.add_argument("-d", "--disable", dest="disable", action="store_true", help="Disable existing keybindings")

parser_keys.add_argument("-fg", "--group", dest="keys_group", help="Select a particular group")
parser_keys.add_argument("-fs", "--source", dest="keys_source", help="Select a particular source")
parser_keys.add_argument("-fn", "--name", dest="keys_name", help="A part of the particular keybinding name to match")
parser_keys.add_argument("-fk", "--keybinding", dest="keys_key", help="A part of the particular keybinding value to match")
parser_keys.add_argument("-a", "--all", dest="keys_all", help="Show also disabled keybindings")
parser_keys.add_argument("-t", "--template", dest="keys_template", help="Select the template")


parser_templates = subparsers.add_parser('templates', help='Manage the templates')
parser_templates.add_argument("-l", "--list", dest="list_templates", action="store_true", help="List the templates")

parser_show = subparsers.add_parser('show', help='Show the keybindings')
parser_show.add_argument("-t", "--template", dest="show_template", help="Select the template to use")

args = parser.parse_args()
print(args)

if args.version:
    print("KbHelp.py - v"+VERSION)
    exit(0)

if not args.command:
    parser.print_usage()
    exit(0)

if args.command == "parsers":
    parsers.output_table()
    exit(0)

if args.command == "templates":
    if args.list_templates:
        templates = Templates.Templates()
        templates.output_table()
    exit(0)

if args.command == 'import':
    if not args.index_parser:
        parser_import.print_usage()
    else:
        parsers.import_shortcuts(args.index_parser, args.import_group, args.import_file, args.import_filter_group, args.import_filter_name, args.import_filter_key)

if args.command == 'keys':
    if args.list_keys:
        config = Config.Config()
        groups = config.get_groups()
        groups.output_table(args.keys_group, args.keys_source, args.keys_name, args.keys_key, args.keys_all, args.keys_template)

if args.command == 'show':
    app = QApplication(sys.argv)
    window = Gui.MainWindow(args.show_template)
    window.show()
    app.exec()
        #parsers.import_shortcuts(args.import_shortcuts, args.group)
    # if args.import_shortcuts:
    #     parsers.import_shortcuts(args.import_shortcuts, args.group)
# if not args.pretty_table:
#     app = QApplication(sys.argv)
#     window = Gui.MainWindow(shortcuts, config)
#     window.show()
#     app.exec()
# else:
#     Cli.print_shortcuts(shortcuts).k
