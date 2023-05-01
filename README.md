# UKBHelp - The Universal Key Bindings Helper

UKBHelp is an universal key-bindings helper for Linux, written in Python and heavily inspired by AwesomeWM and its "Mod4+s" feature.

The features are as follows:

- Configuration with JSON
- Facilities to import shortcuts from existing files
- Configure the helper with Templates and Groups
- Customizable design (colors, opacity, fonts, etc.)
- Window Rules supported, to show the shortcuts relevant to the current app
- CLI tool to list and do some actions with your shortcuts


## Usage

The code is a Python 3 script. You just need to clone this repository and run `pip3 install -r requirements.txt`.

Then you have to launch `ukbhelp.py` with the relevant options. The tool has 5 main commands:

- `parsers` to show the available shortcut parsers in the console
- `templates` to show the available templates
- `import` to import a file containing shortcuts
- `keys` to show the keybindings configured
- `show` to show the helper in itself

For each command, you can type `ukbhelp.py <command> -h` to get help.

To achieve the configuration:
```
./kbhelp.py import -i 1 -p KDE
./kbhelp.py import -i 2 -p Vivaldi
./kbhelp.py import -i 4 -p Dolphin -g Dolphin -f ~/dolphin.shortcuts
```



```
./kbhelp.py manage -a associate -g Dolphin -t Dolphin
./kbhelp.py manage -a dissociate -g Dolphin -t Default
./kbhelp.py manage -a associate -g Vivaldi -t Vivaldi
./kbhelp.py manage -a dissociate -g Vivaldi -t Default
```

## Feedbacks

This tool is not perfect, but it may be useful to build your own "keybinding helper" if your Desktop Environment does not support this feature.
Your contributions are welcomed!

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/juienpro)
