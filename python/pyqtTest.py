from PyQt5.QtCore import Qt, QRectF
from PyQt5 import QtSvg
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton, 
    QTextEdit,
    QPlainTextEdit,
    QVBoxLayout, 
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFileDialog, 
)
from PyQt5.QtGui import (
        QPalette, 
        QColor, 
)

import sys, os
# Article to fix pyqt error I was seeing:
# https://stackoverflow.com/questions/59809703/could-not-load-the-qt-platform-plugin-xcb-in-even-though-it-was-found

# QSvgWidget
#https://doc.qt.io/qtforpython-5/PySide2/QtSvg/QSvgWidget.html#more

SVG_PATH = './donuts-cake-svgrepo-com.svg'
#TODO: Keyboard shortcuts
class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.setWindowTitle("My App")

        config_editor_widget = ConfigEditor()
        svg_viewwe_widget = SvgViewer()
        btn_menue_widget = ButtonMenu(config_editor_widget)

        top_v_layout = QHBoxLayout()
        top_v_layout.addWidget(config_editor_widget)
        top_v_layout.addWidget(svg_viewwe_widget)
        top_widget = QWidget()
        top_widget.setLayout(top_v_layout)

        main_h_layout = QVBoxLayout() 
        main_h_layout.addWidget(top_widget)
        main_h_layout.addWidget(btn_menue_widget)
        main_widget = QWidget()
        main_widget.setLayout(main_h_layout)

        self.setCentralWidget(main_widget)
        self.showMaximized()
    

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

#TODO: implement zoom in with mouse wheel, or let click
#TODO: impolemnt zoom out with mouse wheel, or right click
#TODO: implement pan with middle mouse click + drag
class SvgViewer(QtSvg.QSvgWidget):
    def __init__(self):
        super().__init__()
        self.image_path:str = SVG_PATH
        self.zoom:int = 100 #100%
        self.load(self.image_path)

    def update_image(self, path:str):
        #TODO: assert here to make sure path is a valid path
        self.image_path = path
        self.load(path)

    def reset_zoom(self):
        self.renderer().viewBox().setSize(self.renderer().viewBox().defaultSize())

    def zoom_in(self, scale:float=2):
        bbox = self.renderer().viewBox()
        sz = bbox.size()
        print(f'bbox was: {bbox}\nsize was: {sz}')
        bbox.setSize(sz/scale)
        self.renderer().setViewBox(bbox)

    def zoom_out(self, amount:int=25):
        pass
    
    def pan(sefl, direction:str, speed:float):
        pass

#TODO: figure out how to load a text file into the widget on startup
class ConfigEditor(QTextEdit):
    def __init__(self):
        super().__init__()

#TODO: Open a text file with the file manager popup
#TODO: Save a text file with the file manager popup
class ButtonMenu(QWidget):
    def __init__(self, config_editor):
        super().__init__()

        btn_menue_layout = QHBoxLayout()

        load_btn = QPushButton('load_btn')
        load_btn.setCheckable(True)
        load_btn.clicked.connect(self.load_btn_clicked)

        save_btn = QPushButton('save_btn')
        save_btn.setCheckable(True)
        save_btn.clicked.connect(self.save_btn_clicked)

        btn_h_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        btn_menue_layout.addWidget(load_btn)
        btn_menue_layout.addWidget(save_btn)

        self.config_editor = config_editor
        self.config_editor.setText('Hello World!')
#        btn_menue_layout.addWidget(btn_h_spacer)
        self.setLayout(btn_menue_layout)

    def _is_valid_txt_or_json_file(self, path:str)->bool:
        file_name, file_extionsion = os.path.splitext(path)
        if not(file_extionsion == '.txt' or file_extionsion == '.json'):
            return False
        return True

    def load_btn_clicked(self):
        file_path, msg = QFileDialog.getOpenFileName(self, 'Open File')
        if not(os.path.exists(file_path)):
            return 
        if not(self._is_valid_txt_or_json_file(file_path)):
            return 
        with open(file_path, 'r') as file:
            file_text_str = file.read()
        self.config_editor.setText(file_text_str)

    def save_btn_clicked(self):
        print('save_btn_clicked!')
        print(self.config_editor.toPlainText())
        file_path, msg = QFileDialog.getSaveFileName(self, 'Save File')
        if not(self._is_valid_txt_or_json_file(file_path)):
            return 
        content = self.config_editor.toPlainText()
        with open(file_path, 'w', encoding='utf-8', errors='xmlcharrefreplace') as output_file:
            output_file.write(content)

        
if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow()
    window.show()  
    app.exec()
