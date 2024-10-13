from PyQt5.QtCore import Qt, QRectF
from PyQt5 import QtSvg
from PyQt5.QtWidgets import (
    QApplication,
    QTextEdit,
    QMainWindow,
)

import sys

SVG_PATH = './donuts-cake-svgrepo-com.svg'

# Article to fix pyqt error I was seeing:
# https://stackoverflow.com/questions/59809703/could-not-load-the-qt-platform-plugin-xcb-in-even-though-it-was-found

# QSvgWidget
#https://doc.qt.io/qtforpython-5/PySide2/QtSvg/QSvgWidget.html#more

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        
#        self.config_editor = QTextEdit()
        self.svg_preview = QtSvg.QSvgWidget()
        self.svg_preview.load(SVG_PATH)
        self.sv_renderer = self.svg_preview.renderer()

        print(self.svg_preview.renderer().viewBox())
        self.sv_renderer.setViewBox(QRectF(0,0,16,16))
#        
        self.setCentralWidget(self.svg_preview)



app = QApplication([])
window = MyMainWindow()
window.show()  
app.exec()
