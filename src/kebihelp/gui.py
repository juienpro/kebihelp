
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QStyle, QLayout, QSizePolicy, QStackedWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from kebihelp.config import Config
import subprocess
from functools import partial
import sys

class MainWindow(QMainWindow):
    def __init__(self, selected_tab, autodetect):
        super().__init__()
        self.selected_tab = selected_tab
        self.autodetect = autodetect
        self.current_tab_name = None
        self.config = Config()

        self.keybindings = self.config.config['Keybindings']
        self.set_current_tab()

        self.layout = self.config.config['Parameters']['layout']
        # self.all_groups = self.config.get_all_groups()
        self.tab_buttons = []
        self.set_main_window()
        self.set_tabs()
        self.change_tab_by_name(self.current_tab_name)
    
    def set_current_tab(self):
        if self.selected_tab != None:
            if self.selected_tab not in self.keybindings:
                print("The tab {} does not exist".format(self.selected_tab))
                sys.exit(1)
            self.current_tab_name = self.selected_tab

        elif self.autodetect:
            result = subprocess.run(self.config.config['Parameters']['cmd_focused_window'], shell=True, stdout=subprocess.PIPE) 
            result = result.stdout.decode('utf-8').strip()
            for window_name, tab_name in self.config.config['Rules'].items():
                if window_name in result:
                    self.current_tab_name = tab_name
                    break
        if self.current_tab_name == None:
            tabs = self.keybindings.keys()
            if len(tabs) == 0:
                print("No tabs found")
                sys.exit(1)
            if '_default' in self.config.config['Rules'].keys() and self.config.config['Rules']['_default'] in tabs:
                self.current_tab_name = self.config.config['Rules']['_default']
            else:
                self.current_tab_name = list(tabs)[0]

        if '_hidden' in self.keybindings[self.current_tab_name] and self.keybindings[self.current_tab_name]['_hidden'] == True:
            print("The tab {} is hidden".format(self.current_tab_name))
            sys.exit(1)

    def set_main_window(self):
        self.setWindowTitle("Kebihelp")
        self.setFont(QFont('Lato'))
        self.setStyleSheet("background-color: {}".format(self.layout['background_color']))

        self.setWindowOpacity(self.layout['opacity'])

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.main_widget = QWidget(self)
        self.window_layout = QVBoxLayout()
        self.tabs_layout = QHBoxLayout()
        self.stacked_widget = QStackedWidget()

        for tab_name, tab_config in self.keybindings.items():
            if '_hidden' in tab_config and tab_config['_hidden'] == True:
                continue
            # if self.current_tab_name != tab_name:
            #     continue
            widget = self.get_tab_shortcuts(tab_name)
            self.stacked_widget.addWidget(widget)

        # for tab in self.all_groups:
        #     if self.config.config['Tabs'][tab]['visible'] == False:
        #         if self.current_tab_name != tab:
        #             continue
        #     widget = self.get_tab_shortcuts(tab)
        #     self.stacked_widget.addWidget(widget)

        self.window_layout.addLayout(self.tabs_layout)
        self.window_layout.addWidget(self.stacked_widget)
        self.window_layout.addStretch()
        self.main_widget.setLayout(self.window_layout)
        self.setCentralWidget(self.main_widget)

    def set_tabs(self):
        index = 0
        for tab_name, tab_config in self.keybindings.items():
            if '_hidden' in tab_config and tab_config['_hidden'] == True:
                continue
            # if self.current_tab_name != tab_name:
            #     continue
            self.tab_button = QPushButton(tab_name)
            conf = self.layout['tabs']
            styles = {'normal': [], 'pressed':[]}
            styles['normal'].append("background-color: {}".format(conf['background_color']))
            styles['normal'].append("padding-top: {}".format(conf['padding']))
            styles['normal'].append("padding-bottom: {}".format(conf['padding']))
            styles['normal'].append("color: {}".format(conf['color']))
            styles['pressed'].append("background-color: {}".format(conf['background_color_current']))

            style = "QPushButton {" + '; '.join(styles['normal'])+ "} "
            style += "QPushButton:checked {" + '; '.join(styles['pressed'])+ "} "
            style += "QPushButton:hover { border: none}"
            style += "QPushButton:enabled { border: none}"

            self.tab_button.setFont(QFont(conf['font'], conf['font_size']))
            self.tab_button.setStyleSheet(style)
            self.tab_button.setCheckable(True)

            self.tab_button.clicked.connect(partial(lambda index: self.change_tab(index), index=index))
            self.tab_button.page = index
            self.tab_button.setAutoExclusive(True)
            self.tab_buttons.append(self.tab_button)
            # if index == 0:
            #     self.tab_buttons[index].setChecked(True)
            self.tabs_layout.addWidget(self.tab_button)
            index += 1

    def change_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.tab_buttons[index].setChecked(True)

    def change_tab_by_name(self, tab_name):
        index = 0
        for tab in self.keybindings.keys():
            if tab == tab_name:
                self.change_tab(index)
                break
            if self.keybindings[tab]['_hidden'] == False:
                index += 1
            # if self.config.config['Tabs'][tab]['visible'] == True:
            #     index += 1
    

    def get_groups(self, tab):
        groups = {}
        for group_name, group_config in self.keybindings[tab].items():
            if group_name == '_hidden':
                continue
            if '_hidden' in group_config and group_config['_hidden'] == True:
                continue
            if len(group_config['keybindings']) == 0:
                continue
            groups[group_name] = { "lines": [], "n_lines": 0 } 
            
            for keybinding in group_config['keybindings']:
                if '_hidden' in keybinding and keybinding['_hidden'] == True:
                    continue
                shortcut_layout = self.get_shortcut_layout(keybinding)
                groups[group_name]['lines'].append(shortcut_layout)
                groups[group_name]['n_lines'] += 1

        groups_sorted = dict(sorted(groups.items(), key=lambda item: item[1]['n_lines']))
        return groups_sorted

    def get_tab_shortcuts(self, tab):
        
        groups = self.get_groups(tab)
        n_groups = len(groups.keys())

        widget = QWidget()

        # vertical_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        
        current_row = 0
        current_column = 0
        for group_name, group in groups.items():
            block_layout = QVBoxLayout()
            block_layout.setSpacing(4)
            group_label = self.get_group_label(group_name)
            block_layout.addLayout(group_label)
            for line in group['lines']:
                block_layout.addLayout(line)
            block_layout.addStretch()
            grid_layout.addLayout(block_layout, current_row, current_column)
            current_column += 1
            
            if current_column >= 2:
                current_column = 0
                current_row += 1
        # columns_layout = QHBoxLayout()
        grid_layout.setVerticalSpacing(10) 
        grid_layout.setHorizontalSpacing(30) 
        grid_layout.setRowStretch(grid_layout.rowCount(), 1)
        widget.setLayout(grid_layout)
        return widget

    def get_group_label(self, group_name):
        hbox = QHBoxLayout()

        label = QLabel(group_name)
        font = QFont(self.layout['group_name']['font'], self.layout['group_name']['font_size'])
        if self.layout['group_name']['bold']:
            font.setBold(True)

        label.setFont(font)
        style = "background-color: {}; color: {}; padding: {}".format(self.layout['group_name']['background_color'], self.layout['group_name']['color'], self.layout['group_name']['padding'])
        label.setStyleSheet(style)
        hbox.addWidget(label)
        if not self.layout['group_name']['stretched']:
            hbox.addStretch()
        
        return hbox

    def get_shortcut_layout(self, shortcut):
        hbox = QHBoxLayout()
        # Label
        font_label = QFont(self.layout['shortcut']['label']['font'], self.layout['shortcut']['label']['font_size'])
        font_label.setBold(self.layout['shortcut']['label']['bold'])
        label = QLabel(shortcut['label'])
        style = "color: {};".format(self.layout['shortcut']['label']['color'])
        label.setStyleSheet(style)
        label.setFont(font_label)

        # Value
        font_value = QFont(self.layout['shortcut']['value']['font'], self.layout['shortcut']['value']['font_size'])
        font_value.setBold(self.layout['shortcut']['value']['bold'])
        value = QLabel(shortcut['value'])
        style = "color: {};".format(self.layout['shortcut']['value']['color'])
        value.setStyleSheet(style)
        value.setFont(font_value)

        hbox.addWidget(label)
        hbox.addStretch()
        hbox.addWidget(value)
        # hbox.setSpacing(self.layout['shortcut']['spacing'])
        # hbox.setContentsMargins(0, 0, 0, 0)
        return hbox

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Q:
            self.close()
        if event.key() == Qt.Key_Tab:
            current_index = self.stacked_widget.currentIndex()
            n_widgets = self.stacked_widget.count()
            if (current_index == n_widgets - 1):
                new_index = 0
            else:
                new_index = current_index + 1
            self.tab_buttons[new_index].setChecked(True)
            self.change_tab(new_index)


