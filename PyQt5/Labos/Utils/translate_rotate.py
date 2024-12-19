#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore,QtGui,QtWidgets 
app=QtWidgets.QApplication(sys.argv)
scene=QtWidgets.QGraphicsScene()
view=QtWidgets.QGraphicsView(scene)
w,h=600,400
view.setGeometry(QtCore.QRect(0,0,w,h))
scene.setSceneRect(0,0,w/2.0,h/2.0)
#------------- scene creation --------------------
topLeft=scene.sceneRect().topLeft()
topRight=scene.sceneRect().topRight()
topLine=QtCore.QLineF(topLeft,topRight)

bottomLeft=scene.sceneRect().bottomLeft()
bottomRight=scene.sceneRect().bottomRight()
bottomLine=QtCore.QLineF(bottomLeft,bottomRight)

leftLine=QtCore.QLineF(topLeft,bottomLeft)
rightLine=QtCore.QLineF(topRight,bottomRight)

pen = QtGui.QPen(QtCore.Qt.red)

scene.addLine(topLine,pen)
scene.addLine(bottomLine,pen)
scene.addLine(leftLine,pen)
scene.addLine(rightLine,pen)

text=QtWidgets.QGraphicsTextItem("Translate/Rotate")
transform=QtGui.QTransform()
toTranslate=bottomRight.y()/2.0
transform.translate(0,toTranslate)
transform.rotate(45)
text.setTransform(transform)
scene.addItem(text)

text=QtWidgets.QGraphicsTextItem("Rotate/Translate")
transform=QtGui.QTransform()
transform.rotate(-45)
transform.translate(0,toTranslate)
text.setTransform(transform)
scene.addItem(text)
#-------------------------------------------------

view.show()
sys.exit(app.exec_())
