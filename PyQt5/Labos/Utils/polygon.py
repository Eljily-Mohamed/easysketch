import os,sys
from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtCore import QT_VERSION_STR

if __name__ == "__main__" :
    print(QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)
    view=QtWidgets.QGraphicsView()
    scene=QtWidgets.QGraphicsScene()
#   view.setGeometry(500,200,1000,600)
    w=view.width() 
    h=view.height()
    points=[(-100,-100),(-100,100),(100,100),(100,-100)]
    vertices = [QtCore.QPointF(x, y) for (x, y) in points]
    polygon = QtGui.QPolygonF(vertices)
    qpoly=QtWidgets.QGraphicsPolygonItem()
    qpoly.setPolygon(polygon)      
    scene.addItem(qpoly)
    for item in scene.items() :
        print("type",item.type())
        if item.type() == 5 :
            print("polygon")
            for point in item.polygon() :
                print("point", point.x(),point.y())
    view.setScene(scene)
    view.show()
    sys.exit(app.exec_())
