import sys
from PyQt5 import QtCore,QtGui,QtWidgets,QtSvg
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView,QGraphicsItem

class Scene(QGraphicsScene) :
    def __init__(self):
        super().__init__()
        # scene.setSceneRect(-150, -150, 300, 300)
        self.setSceneRect(0,0,1000,800)
        self.begin=QtCore.QPointF(0.0,0.0)
        self.end=QtCore.QPointF(0.0,0.0)
        rect=QtCore.QRectF(0,0,100,100)
        self.rubber=self.addRect(rect)
        pen=QtGui.QPen()
        pen.setStyle(QtCore.Qt.DashLine)
        self.rubber.setPen(pen)
        self.rubber.setVisible(False)

    def mousePressEvent(self,event) :
        if (event.buttons() & QtCore.Qt.LeftButton) :
            self.begin=event.scenePos()
            self.end=event.scenePos()
            rect=self.rubber.rect()
            rect.setTopLeft(self.begin) 
            self.rubber.setRect(rect)

    def mouseMoveEvent(self,event) :
        if (event.buttons() & QtCore.Qt.LeftButton) :
            self.end=event.scenePos()
            self.rubber.setVisible(True)
            rect=self.rubber.rect()
            rect.setBottomRight(self.end) 
            self.rubber.setRect(rect)    

    def mouseReleaseEvent(self,event) :
        self.rubber.setVisible(False)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    view = QtWidgets.QGraphicsView()
    view.setGeometry(QtCore.QRect(0, 0, 600, 500))
    view.setWindowTitle("Rubberband")
    scene=Scene()
    view.setScene(scene)
    view.show()
    sys.exit(app.exec_())