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
)
from PyQt5.QtGui import QPalette, QColor 

import sys
# Article to fix pyqt error I was seeing:
# https://stackoverflow.com/questions/59809703/could-not-load-the-qt-platform-plugin-xcb-in-even-though-it-was-found

# QSvgWidget
#https://doc.qt.io/qtforpython-5/PySide2/QtSvg/QSvgWidget.html#more

SVG_PATH = './donuts-cake-svgrepo-com.svg'
class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.setWindowTitle("My App")

        config_editor_widget = ConfigEditor()
        svg_viewwe_widget = SvgViewer()
        btn_menue_widget = ButtonMenu()

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

class ConfigEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

class ButtonMenu(QWidget):
    def __init__(self):
        super().__init__()

        btn_menue_layout = QHBoxLayout()

        btn0 = QPushButton('btn0')
        btn0.setCheckable(True)
        btn0.clicked.connect(self.btn0_clicked)

        btn1 = QPushButton('btn1')
        btn1.setCheckable(True)
        btn1.clicked.connect(self.btn1_clicked)

        btn_h_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        btn_menue_layout.addWidget(btn0)
        btn_menue_layout.addWidget(btn1)
#        btn_menue_layout.addWidget(btn_h_spacer)
        

        self.setLayout(btn_menue_layout)

    def btn0_clicked(self):
        print('btn0_clicked!')
    def btn1_clicked(self):
        print('btn1_clicked!')

        
if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow()
    window.show()  
    app.exec()
