# coding: utf-8
# https://ensip.gitlab.io/pages-info/ressources/transverse/tuto_pyqt.html#qgraphicsview-et-qgraphicsscene

import sys
from PyQt5 import QtCore,QtGui,QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self, titre,x=0,y=0,width=600,height=800):
        QtWidgets.QWidget.__init__(self) 
        self.setWindowTitle(titre)
        self.width,self.height=width,height
        self.setGeometry(x,y,width,height)
        self.create_scene()
        self.view.installEventFilter(self)

        self.polygon=[]
    def create_scene(self) :
            self.scene=QtWidgets.QGraphicsScene()
            self.view =QtWidgets.QGraphicsView(self.scene,self)
            # self.view.setSceneRect(QtCore.QRectF(0,0,self.width,self.height))
            self.view.setSceneRect(QtCore.QRectF(0,0,self.width-100,self.height-200))

            rect=QtWidgets.QGraphicsRectItem(100.0,0.0,100.0,200)
            rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,True)
            self.scene.addItem(rect)
            rect=QtWidgets.QGraphicsRectItem(-5.0,-5.0,10,10)
            self.scene.addItem(rect)
        
    def eventFilter(self, obj, event):
        if obj == self.view:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.button_press_event(event)
                return True
        return False
 
    def button_press_event(self, event):
        print("coordonnees fenetre : ",event.pos())
        c=self.view.mapToScene(event.pos())
        print("coordonnees scene : ",c)
        transform=QtGui.QTransform()
        self.item=self.scene.itemAt(c,transform)
        if self.item :
            print("itemAt()")
            
    def mousePressEvent(self, event):
        print("mousePressEvent() : ",event.pos())

    def mouseMoveEvent(self, event):
        print("mouseMoveEvent()",event.pos())
    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent()",event.pos())
        self.item=None
      
    def display(self) :
        self.view.show()
        self.show()

  
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)   
##    mw=QtWidgets.QWidget()
##    create_scene(mw)
##    mw.show()
    mw=MainWindow("Fenêtre principale")
    mw.display()

    sys.exit(app.exec_())
