#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import json
import pickle

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QT_VERSION_STR

def items_to_data(scene):
    # liste de dictionnaires d'items à sauvegarder
    to_save=[] 
    for item in scene.items():
        if isinstance(item, QtWidgets.QGraphicsLineItem):
            # création d'un dictionnaire pour chaque item
            data = {} 
            data["type"] = "line"
            data["x1"] = item.line().x1()
            data["y1"] = item.line().y1()
            data["x2"] = item.line().x2()
            data["y2"] = item.line().y2()
            # ajout du dictionnaire dans la liste des dictionnaires d'items
            to_save.append(data) 
        # a completer pour chaque item
        elif  isinstance(item, QtWidgets.QGraphicsRectItem): 
            pass
        else :
            pass
    return to_save

def save(scene,filename) :
    data=items_to_data(scene)
    print(data)
    # file_to_save = open(filename,"wb")
    # pickle.dump(data,file_to_save)
    # file_to_save.close()
    file_to_save = QtCore.QFile(filename)
    if file_to_save.open(QtCore.QIODevice.WriteOnly):
        file_to_save.write(json.dumps(data).encode("utf-8"))
        file_to_save.close()
        
if __name__ == "__main__":
    print(QT_VERSION_STR)
    app   = QtWidgets.QApplication(sys.argv)
    scene=QtWidgets.QGraphicsScene()
    #------------- scene creation --------------------
    pen=QtGui.QPen(QtCore.Qt.blue,3)
    brush=QtGui.QBrush(QtCore.Qt.red)
    line=scene.addLine(0,0,200,200,pen)
    rect=scene.addRect(QtCore.QRectF(0,0,100,100),pen,brush)
    #-------------------------------------------------
    view=QtWidgets.QGraphicsView(scene)
    filename="scene.json"
    save(scene,filename)
    view.show()
    sys.exit(app.exec_())
