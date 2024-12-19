# coding: utf-8
# https://ensip.gitlab.io/pages-info/ressources/transverse/tuto_pyqt.html#qgraphicsview-et-qgraphicsscene

import sys
from PyQt5 import QtCore,QtGui,QtWidgets

class Scene(QtWidgets.QGraphicsScene):
    def __init__(self,x=0,y=0,width=400,height=300):
        QtWidgets.QGraphicsScene.__init__(self) 
        self.setSceneRect(x,y,width,height)
        self.start,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0)

        self.polygon_drawing=[]
        self.polygon_vertices=[]

        self.item=None
        self.tools="polygon"
        self.create()
        self.dimension()

    def create(self) :
        rect=QtWidgets.QGraphicsRectItem(100.0,0.0,100.0,200)
        rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,True)
        self.addItem(rect)

    def dimension(self) :
        top= QtCore.QLineF(self.sceneRect().topLeft(),self.sceneRect().topRight())
        left= QtCore.QLineF(self.sceneRect().topLeft(),self.sceneRect().bottomLeft())
        right=QtCore.QLineF(self.sceneRect().topRight(), self.sceneRect().bottomRight())
        bottom=QtCore.QLineF(self.sceneRect().bottomLeft(), self.sceneRect().bottomRight())

        pen = QtGui.QPen(QtCore.Qt.red)
        
        self.addLine(top, pen)
        self.addLine(left, pen)
        self.addLine(right, pen)
        self.addLine(bottom, pen)

    def mousePressEvent(self, event):
        print("mousePressEvent()")
        # print("event.scenePos()",event.scenePos())
        # print("event.screenPos()",event.screenPos())
        # print("event.lastScenePos()",event.lastScenePos())
        # print("event.lastScreenPos()",event.lastScreenPos())
        # print("event.pos()",event.pos())
        # print("event.lastPos()",event.lastPos())
        self.start=event.scenePos()
        self.item=self.itemAt(self.start,QtGui.QTransform())
        if self.item :
            self.offset =self.start-self.item.pos()
        else :
            self.end=event.scenePos()
            if self.tools=='polygon' :
                # self.polygon_drawing.append(self.addLine(self.start.x(),self.start.y(),
                #                                             self.end.x(),self.end.y()))
                self.polygon_drawing.append(self.addRect(self.start.x(),self.start.y(),5,5))
                self.polygon_vertices.append(QtCore.QPoint(int(event.scenePos().x()),int(event.scenePos().y())))

    def mouseMoveEvent(self, event):
        # print("mouseMoveEvent()")
        print("event.scenePos().x()- event.lastScenePos().x()",event.scenePos().x()- event.lastScenePos().x())
        print("event.scenePos().y()- event.lastScenePos().y()",event.scenePos().y()- event.lastScenePos().y())
        self.end=event.scenePos()
        if self.item :
            self.item.setPos(event.scenePos() - self.offset)
        else :
            if self.tools=='line' :
                pass
            else :
                pass

    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent()")
        self.end=event.scenePos()
        if self.item :
            self.item.setPos(event.scenePos() - self.offset)
            self.item=None
        else :
            if self.tools=='line' :
                pass
            else :
                pass

    def mouseDoubleClickEvent(self, event):
        print("mouseDoubleClickEvent()")
        if self.tools=="polygon":
            for i in self.polygon_drawing :
                self.removeItem(i)
            qpoly=QtGui.QPolygonF(self.polygon_vertices)
            qgpoly=QtWidgets.QGraphicsPolygonItem(qpoly)
            self.addItem(qgpoly)
            del self.polygon_drawing[:]
            del self.polygon_vertices[:]

# class View(QtWidgets.QGraphicsView):
#     def __init__(self,x=0,y=0,width=600,height=800):
#         QtWidgets.QGraphicsView.__init__(self) 
#         self.setGeometry(x,y,width,height)
#         self.create()
#     def create(self) :
#         pass    
 
  
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)   
    scene=Scene()
    view=QtWidgets.QGraphicsView()
    x,y=0,0
    width,height=600,800
    view.setGeometry(x,y,width,height)
    scene=Scene(x,y,width,height)
    # scene.setSceneRect(x,y,width,height)
    view.setScene(scene)
    view.show()

    sys.exit(app.exec_())
