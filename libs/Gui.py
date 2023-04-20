
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QStyle, QLayout, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
import libs.Config as Config

class MainWindow(QMainWindow):
    def __init__(self, template_name):
        super().__init__()
        if not template_name:
            template_name = "default"

        config = Config.Config()
        self.template = config.config['Templates'][template_name]
        self.groups = config.get_groups(template_name)
        self.set_main_window()
        self.set_groups()
        #self.adjustSize()
        height = self.wid.minimumSizeHint().height()
        width = self.wid.minimumSizeHint().width()
        self.resize(width+20, height+20)


    def set_main_window(self):
        self.setWindowTitle("Keybindings Helper")
        self.setFont(QFont('Lato'))
        self.setStyleSheet("background-color: {}".format(self.template['background_color']))
        self.setWindowOpacity(0.9)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setFixedSize(QSize(self.template['width'], self.template['height']))
        self.window_grid = QHBoxLayout()
        wid = QWidget(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(wid)
        self.setCentralWidget(scroll)
        wid.setLayout(self.window_grid)
        self.wid = wid

    def set_groups(self):
        n_lines = 0
        column_layout = QVBoxLayout()
        column_layout.setSpacing(self.template['spacing'])
        lines = []
        for group_name in self.groups.groups:
            if len(self.groups.groups[group_name].shortcuts) == 0:
                continue
            lines.append(['layout', self.get_group_label(self.groups.groups[group_name])])
            for shortcut in self.groups.groups[group_name].shortcuts:
                shortcut_layout = self.get_shortcut_layout(shortcut)
                lines.append(['layout', shortcut_layout])

        size_col = int(len(lines) / int(self.template['n_columns'])) + (len(lines) % int(self.template['n_columns']) > 0)

        for l in lines:
            if n_lines > size_col:
                n_lines = 0
                column_layout.addStretch()
                self.window_grid.addLayout(column_layout)
                column_layout = QVBoxLayout()
                column_layout.setSpacing(self.template['spacing'])
            if l[0] == 'widget':
                column_layout.addWidget(l[1])
            else:
                column_layout.addLayout(l[1])
            n_lines += 1
        if n_lines <= size_col:
            column_layout.addStretch()
            self.window_grid.addLayout(column_layout)

    def get_group_label(self, group):
        hbox = QHBoxLayout()
        label = QLabel(group.label)
        font = QFont(self.template['group_name']['font'], self.template['group_name']['font_size'])
        if self.template['group_name']['bold']:
            font.setBold(True)

        label.setFont(font)
        style = "background-color: {}; color: {}; padding: {}".format(self.template['group_name']['background_color'], self.template['group_name']['color'], self.template['group_name']['padding'])
        label.setStyleSheet(style)
        hbox.addWidget(label)
        if not self.template['group_name']['stretched']:
            hbox.addStretch()
        return hbox

    def get_shortcut_layout(self, shortcut):
        hbox = QHBoxLayout()
        # Label
        font_label = QFont(self.template['shortcut']['label']['font'], self.template['shortcut']['label']['font_size'])
        font_label.setBold(self.template['shortcut']['label']['bold'])
        label = QLabel(shortcut.label)
        style = "color: {};".format(self.template['shortcut']['label']['color'])
        label.setStyleSheet(style)
        label.setFont(font_label)

        # Value
        font_value = QFont(self.template['shortcut']['value']['font'], self.template['shortcut']['value']['font_size'])
        font_value.setBold(self.template['shortcut']['value']['bold'])
        value = QLabel(shortcut.value)
        style = "color: {};".format(self.template['shortcut']['value']['color'])
        value.setStyleSheet(style)
        value.setFont(font_value)

        hbox.addWidget(label)
        hbox.addWidget(value)
        hbox.setSpacing(self.template['shortcut']['spacing'])
        # hbox.setContentsMargins(0, 0, 0, 0)
        return hbox

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape :
            self.close()

