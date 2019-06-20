# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 15:37:36 2018

@author: Prashant
"""
import sys
import time
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap

import editor

class SplaceScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super(SplaceScreen, self).__init__()
        uic.loadUi('ui/splace.ui', self)
        self.move(500, 200)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SplaceScreen()
    for i in range(1, 101):
        window.progressBar.setValue(i)
        time.sleep(0.01)
    window.close()
    edit_app = editor.MainApp()
    sys.exit(app.exec_())