#!/usr/bin/python
import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsScene, QInputDialog, QGraphicsView
from PyQt5.QtGui import QTransform


class View (QtWidgets.QGraphicsView) :
    def __init__(self,position=(0,0),dimension=(600,400)):
        QtWidgets.QGraphicsView.__init__(self)
        x,y=position
        w,h=dimension
        self.setGeometry(x,y,w,h)

        self.begin,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.offset=QtCore.QPoint(0,0)
        self.pen,self.brush=None,None
        self.tool="rectangle"
        self.item=None
        self.polygon_drawing=[]
        self.polygon_vertices=[]
        self.selected_text_item = None
        
        self.font = QtGui.QFont()

        self.rubber = None
        self.create_style()
        
    def __repr__(self):
        return "<View({},{},{})>".format(self.pen,self.brush,self.tool)
    
    def get_pen(self) :
        return self.pen
    def set_pen(self,pen) :
        self.pen=pen
    def set_pen_color(self,color) :
        print("View.set_pen_color(self,color)",color)
        self.pen.setColor(QtGui.QColor(color))
    def get_brush(self) :
        return self.brush
    def set_brush(self,brush) :
        self.brush=brush
    def set_brush_color(self,color) :
        print("View.set_brush_color(self,color)",color)
        self.brush.setColor(QtGui.QColor(color))

    def get_font(self):
        return self.font

    def set_font(self, font):
        self.font = font

    def get_tool(self) :
        return self.tool
    def set_tool(self,tool) :
        print("View.set_tool(self,tool)",tool)
        self.tool=tool

    def create_style(self) :
        self.create_pen()
        self.create_brush()
        self.create_rubber()
    def create_pen(self) :
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
    def create_brush(self) :
        self.brush=QtGui.QBrush()
        self.brush.setColor(QtCore.Qt.blue)
        self.brush.setStyle(QtCore.Qt.CrossPattern)
    
    def create_rubber(self):
        print(self.scene())  # Debugging: Check if scene is available
        
        # Create a QRectF (rectangle) for the rubber band
        rect = QtCore.QRectF(0, 0, 100, 100)
        
        # Create the QGraphicsRectItem manually
        self.rubber = QtWidgets.QGraphicsRectItem(rect)
        
        # Set the pen style (dash line) for the rubber band
        pen = QtGui.QPen()
        pen.setStyle(QtCore.Qt.DashLine)
        self.rubber.setPen(pen)
        
        # Set initial visibility to False
        self.rubber.setVisible(False)
        
        # Check if the scene exists before trying to add the rubber band to it
        if self.scene():
            self.scene().addItem(self.rubber)
        else:
            print("Warning: Scene not available. Rubber band won't be added to the scene yet.")

    
    def set_pen_color(self,color) :
        print("View.set_pen_color(self,color)",color)
        self.pen.setColor(QtGui.QColor(color))
    def set_brush_color(self,color) :
        print("View.set_brush_color(self,color)",color)
        self.brush.setColor(QtGui.QColor(color))

    # Events
    def mousePressEvent(self, event):
        print("View.mousePressEvent()")
        print("event.pos():", event.pos())
        print("event.screenPos():", event.screenPos())

        self.begin = self.end = event.pos()
        self.scene().addItem(self.rubber)

        if self.scene():
            self.item = self.scene().itemAt(self.begin, QTransform())

            if self.item:
                rect=self.rubber.rect()
                rect.setTopLeft(self.begin) 
                self.rubber.setRect(rect)

                if isinstance(self.item, QGraphicsTextItem):
                    if self.tool == "text":
                        self.selected_text_item = self.item
                        default_text = "Click to edit text"
                        current_text = self.selected_text_item.toPlainText()

                        # Only clear the default text if it's selected and it's not a tool switch
                        if current_text == default_text:
                            self.selected_text_item.setPlainText('')

                        # Enable text editing and set focus to the item
                        self.selected_text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
                        self.selected_text_item.setFocus()
                    else:
                        # If another tool is selected, treat as item manipulation
                        self.selected_text_item = None
                        self.item.setTextInteractionFlags(Qt.NoTextInteraction)

                else:
                    # If a text item was previously selected, disable text interaction
                    if self.selected_text_item:
                        self.selected_text_item.setTextInteractionFlags(Qt.NoTextInteraction)
                        self.selected_text_item = None

                self.offset = self.begin - self.item.pos()
            else:
                # Handle case where no item is clicked
                print("No item under the mouse click!")
                if self.tool == "polygon":
                    self.polygon_drawing.append(self.scene().addRect(self.begin.x(), self.begin.y(), 5, 5))
                    self.polygon_vertices.append(QtCore.QPoint(int(self.begin.x()), int(self.begin.y())))

        else:
            print("View needs a scene to display items!")

    def mouseMoveEvent(self, event):
        self.end=event.pos()
        if self.scene() :
            if self.item :
                self.item.setPos(event.pos() - self.offset)
            else :
                rect = QtCore.QRectF(self.begin, self.end)
                self.rubber.setRect(rect.normalized())  
                self.rubber.setVisible(True)
                print("draw bounding box !")
        else :
            print("View need a scene to display items !!")
            
    def mouseDoubleClickEvent(self, event):
            if self.scene() and self.tool == "polygon":
                for item in self.polygon_drawing:
                    self.scene().removeItem(item)
                qpoly = QtGui.QPolygonF(self.polygon_vertices)
                qgpoly = QtWidgets.QGraphicsPolygonItem(qpoly)
                qgpoly.setPen(self.pen)
                qgpoly.setBrush(self.brush)
                self.scene().addItem(qgpoly)

                self.polygon_drawing.clear()
                self.polygon_vertices.clear()
    
    def mouseReleaseEvent(self, event):
        print("View.mouseReleaseEvent()")
        print("nb items : ", len(self.items()))
        self.end = event.pos()
        self.rubber.setVisible(False)

        # if the scene exists
        if self.scene():
            # if an item is selected, we move it
            self.scene().removeItem(self.rubber)
            if self.item:
                self.item.setPos(event.pos() - self.offset)
                self.item = None
            # if 'line' selected, draw a line
            elif self.tool == "line":
                line = QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(), self.end.x(), self.end.y())
                line.setPen(self.pen)
                self.scene().addItem(line)
            # if 'rectangle' selected, draw a rectangle
            elif self.tool == "rectangle":
                rect = QtWidgets.QGraphicsRectItem(
                    self.begin.x(), self.begin.y(),
                    abs(self.end.x() - self.begin.x()),
                    abs(self.end.y() - self.begin.y())
                )
                rect.setPen(self.pen)
                rect.setBrush(self.brush)
                self.scene().addItem(rect)
                
            # if 'ellipse' selected, draw a ellipse
            elif self.tool == "ellipse":
                ellipse = QtWidgets.QGraphicsEllipseItem(
                    self.begin.x(), self.begin.y(),
                    abs(self.end.x() - self.begin.x()),
                    abs(self.end.y() - self.begin.y())
                )
                ellipse.setPen(self.pen)
                ellipse.setBrush(self.brush)
                self.scene().addItem(ellipse)        
            # if 'text' selected, draw a text
            elif self.tool == "text":
                # Create a new text item when tool is set to "text"
                text_item = QGraphicsTextItem("Click to edit text")
                text_item.setPos(self.begin)
                text_item.setDefaultTextColor(self.pen.color())
                text_item.setFont(self.font)
                text_item.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)  # Make the text editable
                self.scene().addItem(text_item)

                def on_focus_out_event(event):
                    text_item.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)  # Make text non-editable again
                    text_item.setPlainText(text_item.toPlainText())  # Save the text input
                    super(QGraphicsTextItem, text_item).focusOutEvent(event)  # Call the base focusOutEvent

                text_item.focusOutEvent = on_focus_out_event
            else:
                print("No items selected!")
        else:
            print("The view needs a scene to show elements!")


    def focusOutEvent(self, event):
        """ Handle focus out for text items when switching tools. """
        if self.selected_text_item:
            # Only disable text interaction if the focus leaves the text item
            self.selected_text_item.setTextInteractionFlags(Qt.NoTextInteraction)
            self.selected_text_item = None
        super(View, self).focusOutEvent(event)  # Call the base focusOutEvent

    def resizeEvent(self,event):
        print("View.resizeEvent()")
        print("width : {}, height : {}".format(self.size().width(),self.size().height()))
   
if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)

    # View
    x,y=0,0
    w,h=600,400
    view=View(position=(x,y),dimension=(w,h))
    view.setWindowTitle("CAI 2425 A  : View")

    # Scene
    model=QtWidgets.QGraphicsScene()
    model.setSceneRect(x,y,w,h)
    view.setScene(model)

    # Items
    offset=5
    xd,yd=offset,offset
    xf,yf=200+offset,100+offset
    line=QtWidgets.QGraphicsLineItem(xd,yd,xf,yf)
    line.setPen(view.get_pen())
    model.addItem(line)

    view.show()
    sys.exit(app.exec_())

