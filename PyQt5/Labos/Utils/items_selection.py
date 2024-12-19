import sys
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem

app=QApplication(sys.argv)
view=QGraphicsView()
scene=QGraphicsScene()
view.setScene(scene)
#------------- scene creation --------------------
pix=scene.addPixmap(QPixmap('monkey_on_16x16.png'))
pix.setFlags(QGraphicsItem.ItemIsSelectable| QGraphicsItem.ItemIsMovable)
pix.setSelected(True)

pix=scene.addPixmap(QPixmap('monkey_on_16x16.png'))
pix.setFlags(QGraphicsItem.ItemIsSelectable| QGraphicsItem.ItemIsMovable)
pix.setPos(100,50)   
#-------------------------------------------------
view.show()
sys.exit(app.exec_())
