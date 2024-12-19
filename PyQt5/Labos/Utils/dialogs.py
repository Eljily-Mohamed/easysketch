import sys
from PyQt5 import QtCore,QtWidgets

def message_box(
        title="CAI ",
        text="QMessageBox.Warning",
        informative="Fermer l'application ?",
        details="Attention : en validant OK vous allez tout perdre",
        icon=QtWidgets.QMessageBox.Warning) :
    msg = QtWidgets.QMessageBox()
    msg.setIcon(icon)
    msg.setText(text)
    msg.setInformativeText(informative)
    msg.setWindowTitle(title)
    msg.setDetailedText(details)
    return msg

if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)
    answer=message_box().exec()
    if answer== QtWidgets.QMessageBox.Ok:
        exit()
    sys.exit(app.exec_())
