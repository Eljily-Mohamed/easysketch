import sys
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5 import QtCore,QtGui,QtWidgets

class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)

    def keyPressEvent(self,event):
        if event.key()==(QtCore.Qt.Key_Control and QtCore.Qt.Key_Z):
            self.undo()
        #To get the remaining functionality back (e.g. without this, typing would not work):
        QtWidgets.QWidget.keyPressEvent(self,event)

    def undo(self):
        print("Ctrl-Z : undo")

if __name__ == "__main__" :  
    print(QT_VERSION_STR)
    app = QtWidgets.QApplication(sys.argv)
    main = MyWidget()
    main.show()
    sys.exit(app.exec_())
