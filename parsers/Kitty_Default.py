import urllib.request
import re
import libs.Config as Config
import libs.Groups as Groups
import libs.Group as Group
import libs.Shortcut as Shortcut

class Kitty_Default():

    def __init__(self):
        self.name = "Kitty Default Shortcuts"
        self.category = "Terminal"
        self.desktop = "All"
        self.groups_supported = True
        self.file = 'https://sw.kovidgoyal.net/kitty/overview/'
        self.groups = Groups.Groups()


    def parse(self, default_group = None, overriden_file=None):
        req = urllib.request.Request(self.file, data=None, headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        f = urllib.request.urlopen(req)
        html = f.read().decode('utf-8')
        sections = html.split('<section id')

        if default_group:
           group = Group.Group(default_group)

        for section in sections:
            z = re.match(".*<h\d>(.+?)<a (.+?)</h\d>", section, re.MULTILINE + re.DOTALL)
            if not z:
                continue
            title = z.group(1)
            if not default_group:
                group = Group.Group(title)
             
            trs = re.findall(r"<tr(.+?)>(.+?)</tr>", section, re.MULTILINE + re.DOTALL)
            if len(trs) == 0:
                continue

            for tr in trs:
                tds = re.findall(r"<td>(.+?)</td>", tr[1] ,re.MULTILINE + re.DOTALL)
                if len(tds) > 1:
                    label = self.clean_html(tds[0])
                    value = self.clean_html(tds[1])
                    value = value.replace('&gt;', '>')
                    value = re.sub("\(.+?\)", "", value)
                    value = value.replace("\n", "")

                    shortcut = Shortcut.Shortcut()
                    shortcut.set_label(label)
                    shortcut.set_shortcut(value)
                    shortcut.set_source(self.name)
                    group.add_shortcut(shortcut)

            if not default_group:
                self.groups.add_group(group)

        if default_group:
            self.groups.add_group(group)

    def clean_html(self, html):
        clean_r = re.compile('<.*?>')
        cleantext = re.sub(clean_r, '', html)
        return cleantext

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
