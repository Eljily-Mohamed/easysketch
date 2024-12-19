import sys
from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import QApplication,QWidget,QGraphicsScene,QGraphicsView,QGraphicsItem

# http://www.gchagnon.fr/cours/python/pyqt.html

app=QApplication(sys.argv)
scene=QGraphicsScene()
#------  scene creation -----(-------------------
rect=scene.addRect(QtCore.QRectF(0, 0, 100, 100))
rect.setFlag(QGraphicsItem.ItemIsMovable)
rect.setFlags(QGraphicsItem.ItemIsMovable|QGraphicsItem.ItemIsSelectable )

rect=scene.addRect(QtCore.QRectF(200, 200, 100, 100))
rect.setFlag(QGraphicsItem.ItemIsSelectable)
rect.setFlags(QGraphicsItem.ItemIsMovable|QGraphicsItem.ItemIsSelectable )

#------------------------------------------------
view=QGraphicsView(scene)
# view.resize(500,300)
# view.move(500,500)
view.show()
sys.exit(app.exec_())
