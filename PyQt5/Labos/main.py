#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore,QtGui,QtWidgets

from window import Window

print(QtCore.QT_VERSION_STR)

app=QtWidgets.QApplication(sys.argv)

position=0,0
dimension=600,400
mw=Window(position,dimension)

offset=5
xd,yd=offset,offset
xf,yf=200+offset,100+offset
line=QtWidgets.QGraphicsLineItem(xd,yd,xf,yf)

pen=QtGui.QPen()
pen.setColor(QtCore.Qt.red)
line.setPen(pen)
#mw.get_scene().addItem(line)

mw.show()

sys.exit(app.exec_())
