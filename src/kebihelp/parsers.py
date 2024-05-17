
import os
import re
import sys
import urllib.request
import glob
from kebihelp.config import Config
from prettytable import PrettyTable
import importlib

class Parsers():
    def __init__(self, destination_tab, source):
        self.destination_tab = destination_tab
        self.source = source
        self.config = Config()

    def import_from_quickref(self):
        req = urllib.request.Request(self.source, data=None, headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        f = urllib.request.urlopen(req)
        html = f.read().decode('utf-8')
        sections = html.split('<div class="h3-wrap">')
        sections.pop(0)

        for section in sections:
            z = re.match(".*<h3.*</a>(.+?)</h3>", section, re.MULTILINE + re.DOTALL)
            title = z.group(1)
            trs = re.findall(r"<tr>(.+?)</tr>", section, re.MULTILINE + re.DOTALL)
            for tr in trs:
                tds = re.findall(r"<td>(.+?)</td>", tr ,re.MULTILINE + re.DOTALL)
                if (len(tds) > 1):
                    label = tds[1]
                    value = tds[0].replace("</code> <code>", "+").replace("</code>", "").replace('<code>', "")
                    self.config.add_keybinding(self.destination_tab, section, value, label)

    def import_from_directory(self):
        # Format: KBH=tab,value,description
        files = glob.glob(self.source+"/**/*", recursive=True)
        if not files:
            print("No files found")
            sys.exit(1)
        regexp = self.config.config['Parameters']['importer']['match_line']
        for file in files:
            # print("Importing from file "+file)
            if os.path.isfile(file):
                with open(file, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        line = line.strip()
                        res = re.match(regexp, line, re.IGNORECASE)
                        if res:
                            group = res.group(self.config.config['Parameters']['importer']['position_group'])
                            keybind = res.group(self.config.config['Parameters']['importer']['position_keybinding'])
                            label = res.group(self.config.config['Parameters']['importer']['position_label'])
                            self.config.add_keybinding(self.destination_tab, group, keybind, label)


    def import_bindings(self):
        if 'quickref.me' in self.source:
            self.import_from_quickref()
        else:
            self.import_from_directory()
        self.config.save()


