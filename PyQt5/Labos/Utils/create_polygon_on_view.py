# coding: utf-8
# https://ensip.gitlab.io/pages-info/ressources/transverse/tuto_pyqt.html#qgraphicsview-et-qgraphicsscene

import sys
from PyQt5 import QtCore,QtGui,QtWidgets

class View(QtWidgets.QGraphicsView):
    def __init__(self,x=0,y=0,width=400,height=300,scene=None):
        QtWidgets.QGraphicsScene.__init__(self) 
        self.setGeometry(x,y,width,height)
        self.setScene(scene)
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
        self.scene().addItem(rect)

    def dimension(self) :
        scene_rect=self.scene().sceneRect()
        top= QtCore.QLineF(scene_rect.topLeft(),scene_rect.topRight())
        left= QtCore.QLineF(scene_rect.topLeft(),scene_rect.bottomLeft())
        right=QtCore.QLineF(scene_rect.topRight(),scene_rect.bottomRight())
        bottom=QtCore.QLineF(scene_rect.bottomLeft(),scene_rect.bottomRight())

        pen = QtGui.QPen(QtCore.Qt.red)
        
        scene.addLine(top, pen)
        scene.addLine(left, pen)
        scene.addLine(right, pen)
        scene.addLine(bottom, pen)

    def mousePressEvent(self, event):
        print("mousePressEvent()")
        scene=self.scene()
        # print("event.scenePos()",event.scenePos())
        # print("event.screenPos()",event.screenPos())
        # print("event.lastScenePos()",event.lastScenePos())
        # print("event.lastScreenPos()",event.lastScreenPos())
        # print("event.pos()",event.pos())
        # print("event.lastPos()",event.lastPos())
        scene=self.scene()
        # self.start=event.screenPos()
        self.start=event.pos()
        self.item=scene.itemAt(self.start,QtGui.QTransform())
        if self.item :
            self.offset =self.start-self.item.pos()
        else :
            # self.end=event.screenPos()
            self.start=event.pos()
            if self.tools=='polygon' :
                # self.polygon_drawing.append(self.addLine(self.start.x(),self.start.y(),
                #                                             self.end.x(),self.end.y()))
                self.polygon_drawing.append(scene.addRect(self.start.x(),self.start.y(),5,5))
                self.polygon_vertices.append(
                    # QtCore.QPoint(int(event.screenPos().x()),int(event.screenPos().y())))
                    QtCore.QPoint(int(event.pos().x()),int(event.pos().y())))


    def mouseMoveEvent(self, event):
        print("mouseMoveEvent()")
        # self.end=event.screenPos()
        self.end=event.pos()
        if self.item :
            # self.item.setPos(event.screenPos() - self.offset)
            # self.item.setPos(event.screenPos() - self.offset)
            self.item.setPos(event.pos() - self.offset)
            self.item.setPos(event.pos() - self.offset)
        else :
            if self.tools=='line' :
                pass
            else :
                pass

    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent()")
        # self.end=event.screenPos()
        self.end=event.pos()
        if self.item :
            # self.item.setPos(event.screenPos() - self.offset)
            self.item.setPos(event.pos() - self.offset)
            self.item=None
        else :
            if self.tools=='line' :
                pass
            else :
                pass

    def mouseDoubleClickEvent(self, event):
        print("mouseDoubleClickEvent()")
        scene=self.scene()
        if self.tools=="polygon":
            for i in self.polygon_drawing :
                scene.removeItem(i)
            qpoly=QtGui.QPolygonF(self.polygon_vertices)
            qgpoly=QtWidgets.QGraphicsPolygonItem(qpoly)
            scene.addItem(qgpoly)
            del self.polygon_drawing[:]
            del self.polygon_vertices[:]

# class Scene(QtWidgets.QGraphicsScene):
#     def __init__(self,x=0,y=0,width=600,height=800):
#         QtWidgets.QGraphicsView.__init__(self) 
#         self.setSceneRect(x,y,width,height)
#         self.create()
#     def create(self) :
#         pass    
 
  
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)   
    scene=QtWidgets.QGraphicsScene()
    x,y=0,0
    width,height=600,800
    scene.setSceneRect(x,y,width,height)
    view=View(x,y,width,height,scene)
    view.show()

    sys.exit(app.exec_())
