import libs.Config as Config
import libs.Groups as Groups
import libs.Group as Group
import libs.Shortcut as Shortcut
import os
import urllib.request
import re

class Parser():
    def __init__(self, description):
        self.name = description['name']
        self.category = description['category']
        self.desktop = description['desktop']
        self.file = description['url']
        self.groups_supported = True
        self.error = False
        self.error_reason = ""
        self.groups = Groups.Groups()

    def parse(self, default_group = None):
        req = urllib.request.Request(self.file, data=None, headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        f = urllib.request.urlopen(req)
        html = f.read().decode('utf-8')
        sections = html.split('<div class="h3-wrap">')
        sections.pop(0)

        if default_group:
           group = Group.Group(default_group)

        for section in sections:
            z = re.match(".*<h3.*</a>(.+?)</h3>", section, re.MULTILINE + re.DOTALL)
            title = z.group(1)
            if not default_group:
                group = Group.Group(title)

            trs = re.findall(r"<tr>(.+?)</tr>", section, re.MULTILINE + re.DOTALL)
            for tr in trs:
                tds = re.findall(r"<td>(.+?)</td>", tr ,re.MULTILINE + re.DOTALL)
                if (len(tds) > 1):
                    label = tds[1]
                    value = tds[0].replace("</code> <code>", "+").replace("</code>", "").replace('<code>', "")
                    shortcut = Shortcut.Shortcut()
                    shortcut.set_label(label)
                    shortcut.set_shortcut(value)
                    shortcut.set_source(self.name)
                    group.add_shortcut(shortcut)

            if not default_group:
                self.groups.add_group(group)

        if default_group:
            self.groups.add_group(group)

    def set_prefix(self, prefix):
        self.groups.set_prefix(prefix)

    def filter(self, filter_group, filter_name, filter_value):
        self.groups.filter(filter_group, filter_name, filter_value)

    def save(self):
        config = Config.Config()
        config.save_groups(self.groups)

    def associate_to_tab(self, tab):
        if tab:
            config = Config.Config()
            config.associate_groups_to_tab(tab, self.groups)
