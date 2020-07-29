#!/usr/bin/env python3

# Filename: noting.py

"""Noting is a simple note taking app built using Python and PyQt5."""

import sys
from os import path, mkdir
from PyQt5 import QtCore, QtGui, QtWidgets

from notingUI import NotingUi
from notingCtrl import NotingCtrl
from notingModel import NotingModel

__version__ = '0.1'
__author__ = 'David Morilla Cabello'

def main():
    """Main function."""

    DEFAULT_PATH = path.join(QtCore.QDir.currentPath(), 'sessions')
    
    if not path.isdir(DEFAULT_PATH):
        mkdir(DEFAULT_PATH)

    app = QtWidgets.QApplication(sys.argv)

    view = NotingUi()
    model = NotingModel()

    control = NotingCtrl(model=model, view=view, path=DEFAULT_PATH)

    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":

    main()
