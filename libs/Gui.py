
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QStyle, QLayout, QSizePolicy, QStackedWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
import libs.Config as Config
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self, tab_name):
        super().__init__()

        self.config = Config.Config()
        self.current_tab_name = self.config.get_default_tab()
        if tab_name:
            self.current_tab_name = tab_name

        # self.tabs = self.config.config['Tabs'][tab_name]
        self.layout = self.config.config['Parameters']['layout']
        self.all_groups = self.config.get_all_groups()
        self.tab_buttons = []
        self.set_main_window()
        self.set_tabs()
        self.change_tab_by_name(self.current_tab_name)


    def set_main_window(self):
        self.setWindowTitle("Keybindings Helper")
        self.setFont(QFont('Lato'))
        self.setStyleSheet("background-color: {}".format(self.layout['background_color']))

        self.setWindowOpacity(self.layout['opacity'])

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.main_widget = QWidget(self)
        self.window_layout = QVBoxLayout()
        self.tabs_layout = QHBoxLayout()
        self.stacked_widget = QStackedWidget()
        for tab in self.all_groups:
            if self.config.config['Tabs'][tab]['visible'] == False:
                if self.current_tab_name != tab:
                    continue
            widget = self.get_tab_shortcuts(tab)
            self.stacked_widget.addWidget(widget)

        self.window_layout.addLayout(self.tabs_layout)
        self.window_layout.addWidget(self.stacked_widget)
        self.main_widget.setLayout(self.window_layout)
        self.setCentralWidget(self.main_widget)

    def set_tabs(self):
        index = 0
        for tab in self.all_groups:
            if self.config.config['Tabs'][tab]['visible'] == False:
                if self.current_tab_name != tab:
                    continue
            self.tab_button = QPushButton(tab)
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
            if index == 0:
                self.tab_buttons[index].setChecked(True)
            self.tabs_layout.addWidget(self.tab_button)
            index += 1

    def change_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.tab_buttons[index].setChecked(True)

    def change_tab_by_name(self, tab_name):
        index = 0
        for tab in self.all_groups:
            if tab == tab_name:
                self.change_tab(index)
                break
            if self.config.config['Tabs'][tab]['visible'] == True:
                index += 1

    def get_tab_shortcuts(self, tab):
        widget = QWidget()
        columns_layout = QHBoxLayout()

        column_layout = QVBoxLayout()
        column_layout.setSpacing(self.layout['spacing'])
        n_lines = 0
        lines = []

        for group_name in self.all_groups[tab].groups:
            if len(self.all_groups[tab].groups[group_name].shortcuts) == 0:
                continue
            if self.all_groups[tab].groups[group_name].enabled == False:
                continue
            lines.append(['layout', self.get_group_label(self.all_groups[tab].groups[group_name])])
            for shortcut in self.all_groups[tab].groups[group_name].shortcuts:
                shortcut_layout = self.get_shortcut_layout(shortcut)
                lines.append(['layout', shortcut_layout])

        size_col = int(len(lines) / int(self.layout['n_columns'])) + (len(lines) % int(self.layout['n_columns']) > 0)

        for l in lines:
            if n_lines > size_col:
                n_lines = 0
                column_layout.addStretch()
                columns_layout.addLayout(column_layout)
                column_layout = QVBoxLayout()
                column_layout.setSpacing(self.layout['spacing'])
            if l[0] == 'widget':
                column_layout.addWidget(l[1])
            else:
                column_layout.addLayout(l[1])
            n_lines += 1
        if n_lines - 1 <= size_col:
            column_layout.addStretch()
            columns_layout.addLayout(column_layout)

        widget.setLayout(columns_layout)
        return widget

    def get_group_label(self, group):
        hbox = QHBoxLayout()
        group_name = group.label
        if '-' in group_name:
            sections = group_name.split('-')
            group_name = sections[1]

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
        label = QLabel(shortcut.label)
        style = "color: {};".format(self.layout['shortcut']['label']['color'])
        label.setStyleSheet(style)
        label.setFont(font_label)

        # Value
        font_value = QFont(self.layout['shortcut']['value']['font'], self.layout['shortcut']['value']['font_size'])
        font_value.setBold(self.layout['shortcut']['value']['bold'])
        value = QLabel(shortcut.value)
        style = "color: {};".format(self.layout['shortcut']['value']['color'])
        value.setStyleSheet(style)
        value.setFont(font_value)

        hbox.addWidget(label)
        hbox.addWidget(value)
        hbox.setSpacing(self.layout['shortcut']['spacing'])
        # hbox.setContentsMargins(0, 0, 0, 0)
        return hbox

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape :
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


