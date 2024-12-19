#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import json
import pickle

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QT_VERSION_STR

def data_to_items(scene,data):
    scene.clear()
    print("data",data)
    for d_item in data :
        print("d_item",d_item)
        t = d_item["type"]
        if t == "line":
            x1, y1, x2, y2 = d_item["x1"], d_item["y1"], d_item["x2"], d_item["y2"]
            scene.addLine(x1, y1, x2, y2)

def load_scene(scene,name) :
    data = json.load(open(name,"r"))
    print("data",data)
    return data
        
if __name__ == "__main__":
    print(QT_VERSION_STR)
    app   = QtWidgets.QApplication(sys.argv)
    scene=QtWidgets.QGraphicsScene()
    filename="scene.json"
    #------------- scene creation --------------------
    data=load_scene(scene,filename) 
    data_to_items(scene,data)
    #-------------------------------------------------
    view=QtWidgets.QGraphicsView(scene)
    view.show()
    sys.exit(app.exec_())
