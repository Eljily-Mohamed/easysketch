# -*- coding: utf-8 -*-
import os,sys
from PyQt5 import QtCore,QtGui,QtWidgets

from view import View
import json

class Window(QtWidgets.QMainWindow):
    def __init__(self,position=(0,0),dimension=(500,300)):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("CAI  2425A : MainWindow (View) ")
        x,y=position
        w,h=dimension
        self.filename = None

        self.items_deletes = []  # Stack for Undo
        self.items_redo = []     # Stack for Redo

        self.view=View()       
        self.scene=QtWidgets.QGraphicsScene()   # model 
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        self.view.setGeometry(x,y,w,h)
        self.scene.setSceneRect(x,y,w,h) 

        self.create_actions()
        self.connect_actions()
        self.create_menus()
 
    def get_view(self) :
        return self.view
    def set_view(self,view) :
        self.view=view

    def get_scene(self) :
        return self.scene
    def set_scene(self,scene) :
        self.scene=scene


    def create_actions(self):
        # File actions
        self.action_file_open = QtWidgets.QAction(QtGui.QIcon('Icons/open.png'), "Open", self)
        self.action_file_open.setShortcut("Ctrl+O")
        self.action_file_open.setStatusTip("Open file")
        self.action_file_new = QtWidgets.QAction(QtGui.QIcon('Icons/new.png'),"New", self)
        self.action_file_new.setStatusTip("New file")
        self.action_file_save = QtWidgets.QAction(QtGui.QIcon('Icons/save.png'),"Save", self)
        self.action_file_save.setShortcut("Ctrl+S")
        self.action_file_save.setStatusTip("Save file")
        self.action_file_save_as = QtWidgets.QAction(QtGui.QIcon('Icons/save_as.png'),"Save As", self)
        self.action_file_save_as.setShortcut("Ctrl+Shift+S")
        self.action_file_save_as.setStatusTip("Save file As")
        self.action_file_exit = QtWidgets.QAction(QtGui.QIcon('Icons/exit.png'),"Exit", self)
        self.action_file_exit.setShortcut("Ctrl+Q")
        self.action_file_exit.setStatusTip("Exit file")

        # Undo action
        self.action_undo = QtWidgets.QAction(self)
        self.action_undo.setShortcut("Ctrl+Z")
        self.action_undo.setStatusTip("Undo last action")

        # Redo action
        self.action_redo = QtWidgets.QAction(self)
        self.action_redo.setShortcut("Ctrl+Y")  
        self.action_redo.setStatusTip("Redo last undone action")
        
        # Tools actions
        self.action_tools = QtWidgets.QActionGroup(self)

        # Line tool
        self.action_tools_line = QtWidgets.QAction(QtGui.QIcon('Icons/tool_line.png'),self.tr("&Line"), self)
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setChecked(True)
        self.action_tools.addAction(self.action_tools_line)

        # Rectangle tool
        self.action_tools_rectangle = QtWidgets.QAction(QtGui.QIcon('Icons/tool_rectangle.png'),self.tr("&Rectangle"), self)
        self.action_tools_rectangle.setCheckable(True)
        self.action_tools.addAction(self.action_tools_rectangle)

        # Ellipse tool
        self.action_tools_ellipse = QtWidgets.QAction(QtGui.QIcon('Icons/tool_ellipse.png'),self.tr("&Ellipse"), self)
        self.action_tools_ellipse.setCheckable(True)
        self.action_tools.addAction(self.action_tools_ellipse)

        # Polygon tool
        self.action_tools_polygon = QtWidgets.QAction(QtGui.QIcon('Icons/tool_polygon.png'),self.tr("&Polygon"), self)
        self.action_tools_polygon.setCheckable(True)
        self.action_tools.addAction(self.action_tools_polygon)

        # Text tool
        self.action_tools_text = QtWidgets.QAction(QtGui.QIcon('Icons/tool_text.png'),self.tr("&Text"), self)
        self.action_tools_text.setCheckable(True)
        self.action_tools.addAction(self.action_tools_text)
        
        # Style actions    
        self.action_style_pen_color=QtWidgets.QAction(QtGui.QIcon('Icons/colorize.png'),self.tr("&Color"),self)
        self.action_style_pen_line_style = QtWidgets.QAction(QtGui.QIcon('Icons/line_style.png'),self.tr("&Line Style"), self)
        self.action_style_pen_width = QtWidgets.QAction(QtGui.QIcon('Icons/line_width.png'),self.tr("&Line Width"), self)

        self.action_style_brush_color = QtWidgets.QAction(QtGui.QIcon('Icons/colorize.png'),self.tr("&Brush Color"), self)
        self.action_style_brush_fill = QtWidgets.QAction(QtGui.QIcon('Icons/brush_fill.png'),self.tr("&Brush Fill"), self)
        self.action_style_font = QtWidgets.QAction(QtGui.QIcon('Icons/tool_font.png'),self.tr("&Font"), self)

    def connect_actions(self):
        # File actions
        self.action_file_open.triggered.connect(self.file_open)
        self.action_file_new.triggered.connect(self.file_new)
        self.action_file_save.triggered.connect(self.file_save)
        self.action_file_save_as.triggered.connect(self.file_save_as)
        self.action_file_exit.triggered.connect(self.close)

        self.action_undo.triggered.connect(self.undo_function)  
        self.action_redo.triggered.connect(self.redo_function)

        #Style actions
        self.action_style_pen_color.triggered.connect(self.style_pen_color_selection)
        self.action_style_pen_line_style.triggered.connect(self.style_pen_line_style_selection)
        self.action_style_pen_width.triggered.connect(self.style_pen_width_selection)

        self.action_style_brush_color.triggered.connect(self.style_brush_color_selection)
        self.action_style_brush_fill.triggered.connect(self.style_brush_fill_selection)
        self.action_style_font.triggered.connect(self.style_font_selection)

        # Tools actions
        self.action_tools_line.triggered.connect(
            lambda checked, tool="line": self.tools_selection(checked, tool)
        )
        self.action_tools_rectangle.triggered.connect(
            lambda checked, tool="rectangle": self.tools_selection(checked, tool)
        )
        self.action_tools_ellipse.triggered.connect(
            lambda checked, tool="ellipse": self.tools_selection(checked, tool)
        )
        self.action_tools_polygon.triggered.connect(
            lambda checked, tool="polygon": self.tools_selection(checked, tool)
        )
        self.action_tools_text.triggered.connect(
            lambda checked, tool="text": self.tools_selection(checked, tool)
        )

    # File actions implementation
    def file_open(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd())
        if filename:
            print(f"Opening file: {filename}")

            file = QtCore.QFile(filename)
            if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                print(f"Failed to open file: {filename}")
                return

            text_stream = QtCore.QTextStream(file)
            file_content = text_stream.readAll()

            data = json.loads(file_content)
            self.scene.clear()

            for item_data in data:
                if item_data["type"] == "line":
                    x1, y1, x2, y2 = item_data["x1"], item_data["y1"], item_data["x2"], item_data["y2"]
                    pen = QtGui.QPen(QtGui.QColor(item_data["pen_color"]))
                    pen.setWidth(item_data["pen_width"])
                    line_item = QtWidgets.QGraphicsLineItem(x1, y1, x2, y2)
                    line_item.setPen(pen)
                    self.scene.addItem(line_item)
                elif item_data["type"] == "ellipse":
                    x,y,width,height=item_data["x"], item_data["y"], item_data["width"], item_data["height"]
                    pen = QtGui.QPen(QtGui.QColor(item_data["pen_color"]))
                    pen.setWidth(item_data["pen_width"])
                    brush = QtGui.QBrush(QtGui.QColor(item_data["brush_color"]))
                    brush.setStyle(item_data["brush_fill"])
                    ellipse_item = QtWidgets.QGraphicsEllipseItem(x,y,width,height)
                    ellipse_item.setPen(pen)
                    ellipse_item.setBrush(brush)
                    self.scene.addItem(ellipse_item)
                elif item_data["type"] == "rectangle":
                    x,y,width,height=item_data["x"], item_data["y"], abs(item_data["width"]), abs(item_data["height"])
                    pen = QtGui.QPen(QtGui.QColor(item_data["pen_color"]))
                    pen.setWidth(item_data["pen_width"])
                    brush = QtGui.QBrush(QtGui.QColor(item_data["brush_color"]))
                    brush.setStyle(item_data["brush_fill"])
                    rect = QtWidgets.QGraphicsRectItem(x,y,width,height)
                    rect.setPen(pen)
                    rect.setBrush(brush)
                    self.scene.addItem(rect)
                elif item_data["type"] == "polygon":
                    polygon = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF([QtCore.QPointF(p[0], p[1]) for p in item_data["points"]]))
                    pen = QtGui.QPen(QtGui.QColor(item_data["pen_color"]))
                    pen.setWidth(item_data["pen_width"])
                    brush = QtGui.QBrush(QtGui.QColor(item_data["brush_color"]))
                    brush.setStyle(item_data["brush_fill"])
                    polygon.setPen(pen)
                    polygon.setBrush(brush)
                    self.scene.addItem(polygon)
                elif item_data["type"] == "text":
                    text = QtWidgets.QGraphicsTextItem(item_data["text"])
                    font = QtGui.QFont(item_data["font_family"], item_data["font_size"])
                    text.setFont(font)
                    text.setPos(item_data["x"], item_data["y"])
                    text.setDefaultTextColor(QtGui.QColor(item_data["pen_color"]))
                    self.scene.addItem(text)

    def file_new(self):
        reply = QtWidgets.QMessageBox.warning(
            self, "New File", "Are you sure you want to create a new file? (All your work will be gone if you've not saved it yet)",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.scene.clear()
            #print("New file created!")
        else :
            print("Operation canceled")

    def info_file(self):
        items = []
        
        for item in self.scene.items():
            item_data = {}
            if isinstance(item, QtWidgets.QGraphicsLineItem):
                line = item.line()
                position = item.pos()

                x1 = line.x1() + position.x()
                y1 = line.y1() + position.y()
                x2 = line.x2() + position.x()
                y2 = line.y2() + position.y()

                item_data = {
                    "type": "line",
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "pen_color": item.pen().color().name(),
                    "pen_width": item.pen().width(),
                }
            elif isinstance(item, QtWidgets.QGraphicsEllipseItem):
                rect = item.rect()
                position = item.pos()
                x = rect.x() + position.x()
                y = rect.y() + position.y()
                item_data = {
                    "type": "ellipse",
                    "x": x,
                    "y": y,
                    "width": rect.width(),
                    "height": rect.height(),
                    "pen_color": item.pen().color().name(),
                    "pen_width": item.pen().width(),
                    "brush_color": item.brush().color().name(),
                    "brush_fill": item.brush().style()
                }
            elif isinstance(item, QtWidgets.QGraphicsRectItem):
                rect = item.rect()
                position = item.pos()
                x = rect.x() + position.x()
                y = rect.y() + position.y()
                item_data = {
                    "type": "rectangle",
                    "x": x,
                    "y": y,
                    "width": rect.width(),
                    "height": rect.height(),
                    "pen_color": item.pen().color().name(),
                    "pen_width": item.pen().width(),
                    "brush_color": item.brush().color().name(),
                    "brush_fill": item.brush().style()

                }
                print(item_data)
            elif isinstance(item, QtWidgets.QGraphicsPolygonItem):
                position = item.pos()
                points = [(point.x()+position.x(), point.y()+position.y()) for point in item.polygon()]
                item_data = {
                    "type": "polygon",
                    "points": points,
                    "pen_color": item.pen().color().name(),
                    "pen_width": item.pen().width(),
                    "brush_color": item.brush().color().name(),
                    "brush_fill": item.brush().style()
                }
            elif isinstance(item, QtWidgets.QGraphicsTextItem):
                item_data = {
                    "type": "text",
                    "text": item.toPlainText(),
                    "x": item.x(),
                    "y": item.y(),
                    "font_family": item.font().family(),
                    "font_size": item.font().pointSize(),
                    "pen_color": item.defaultTextColor().name()
            }
            items.append(item_data)
        return items

    def file_save(self):
        if self.filename is None:  # If no file has been specified
            options = QtWidgets.QFileDialog.Options()
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save File", "", "JSON Files (*.json)", options=options
            )
            if file_name:  # The user gives a file name
                self.filename = file_name
                self._save_to_file(file_name)
        else:  # Use the existing file
            self._save_to_file(self.filename)

    def _save_to_file(self, file_name):
        items = self.info_file()
        with open(file_name, 'w') as file:
            json.dump(items, file, indent=4)
        print(f"File saved: {file_name}")

    def file_save_as(self):
        # Choose to save file as JSON, PNG, JPG
        filename, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save File As",
            os.getcwd(),
            "JSON Files (*.json);;PNG Files (*.png);;JPG Files (*.jpg *.jpeg);;All Files (*)"
        )

        if filename:
            if '.' not in filename:
                if 'JSON' in selected_filter:
                    filename += '.json'
                elif 'PNG' in selected_filter:
                    filename += '.png'
                elif 'JPG' in selected_filter or 'JPEG' in selected_filter:
                    filename += '.jpg'

            file_extension = filename.split('.')[-1].lower()

            if file_extension not in ['json', 'png', 'jpg']:
                print(f"Unsupported file type: {file_extension}")
                return

            if file_extension == 'json':
                self.save_json(filename)
            elif file_extension == 'png':
                self.save_png(filename)
            elif file_extension == 'jpg':
                self.save_jpg(filename)
            print(f"File saved as: {filename}")

    def save_json(self, file_path):
        items = self.info_file()
        with open(file_path, "w") as file:
            import json
            json.dump(items, file, indent=4)

    def save_png(self, file_path):
        image = self.view.grab()
        image.save(file_path, "PNG")
        print(f"PNG file saved as: {file_path}")

    def save_jpg(self, file_path):
        image = self.view.grab()
        image.save(file_path, "JPG")
        print(f"JPG file saved as: {file_path}")

    def file_exit(self):
        reply = QtWidgets.QMessageBox.question(
            self, "Exit", "Are you sure you want to exit? (Don't forget to save your work)",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.close()

    # Tools actions implementation
    def tools_selection(self, checked, tool):
        print(f"Window.tools_selection() - Tool: {tool}, Checked: {checked}")
        if checked:
            self.view.set_tool(tool)


    #PEN
    def style_pen_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow,self)
        if color.isValid() :
            self.view.set_pen_color(color.name())

    def style_pen_line_style_selection(self):
        line_style, ok = QtWidgets.QInputDialog.getItem(
            self, "Select Line Style", "Line style:", 
            ["SolidLine", "DashLine", "DotLine", "DashDotLine"], 0, False
        )
        if ok:
            pen = self.view.get_pen()
            if line_style == "SolidLine":
                pen.setStyle(QtCore.Qt.SolidLine)
            elif line_style == "DashLine":
                pen.setStyle(QtCore.Qt.DashLine)
            elif line_style == "DotLine":
                pen.setStyle(QtCore.Qt.DotLine)
            elif line_style == "DashDotLine":
                pen.setStyle(QtCore.Qt.DashDotLine)
            self.view.set_pen(pen)

    def style_pen_width_selection(self):
        width, ok = QtWidgets.QInputDialog.getInt(self, "Line Width", "Select width:", 1, 1, 10, 1)
        if ok:
            pen = self.view.get_pen()
            pen.setWidth(width)
            self.view.set_pen(pen)

    #BRUSH
    def style_brush_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.green, self)
        if color.isValid():
            self.view.set_brush_color(color.name())

    def style_brush_fill_selection(self):
        style, ok = QtWidgets.QInputDialog.getItem(
            self, "Select Fill Pattern", "Fill pattern:", 
            ["SolidPattern", "VerticalPattern", "CrossPattern", "HorPattern", "NoPattern"]
        )
        if ok:
            brush = self.view.get_brush()
            if style == "SolidPattern":
                brush.setStyle(QtCore.Qt.SolidPattern)
            elif style == "VerticalPattern":
                brush.setStyle(QtCore.Qt.VerPattern)
            elif style == "CrossPattern":
                brush.setStyle(QtCore.Qt.CrossPattern)
            elif style == "HorPattern":
                brush.setStyle(QtCore.Qt.HorPattern)
            elif style == "NoPattern":
                brush.setStyle(0) 
            self.view.set_brush(brush)

    #FONT
    def style_font_selection(self):
        font, ok = QtWidgets.QFontDialog.getFont(self.view.get_font(), self)
        if ok:
            self.view.set_font(font)
 
    # Help actions implementation
    def help_about_us(self) :
        about_dialog = QtWidgets.QDialog(self)
        about_dialog.setWindowTitle("About Us")
        about_dialog.setFixedSize(400, 200)

        text_browser = QtWidgets.QTextBrowser(about_dialog)
        text_browser.setGeometry(10, 10, 380, 180)
        text_browser.setHtml(
            """
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    text-align: center;
                    color: #2C3E50;
                }
                p {
                    margin: 5px 0;
                }
                table {
                    width: 100%;
                    margin-top: 10px;
                    border-collapse: collapse;
                }
                td {
                    padding: 5px;
                    text-align: left;
                }
                .email {
                    color: #2980B9;
                    font-weight: bold;
                }
            </style>
            <body>
                <h1>About Us</h1>
                <table>
                    <tr>
                        <td><b>CHOUBRI Douae</b></td>
                        <td class="email">d3choubr@enib.fr</td>
                    </tr>
                    <tr>
                        <td><b>EL JILY Mohamed</b></td>
                        <td class="email">m3eljily@enib.fr</td>
                    </tr>
                </table>
            </body>
            """
        )
        about_dialog.exec_()

    def help_about_qt(self) :
        about_qt = QtWidgets.QMessageBox.aboutQt(self)

    def help_about_application(self):
        about_dialog = QtWidgets.QDialog(self)
        about_dialog.setWindowTitle("About The Application")

        about_dialog.setFixedSize(600, 400)

        # Center the window on the screen
        screen_geometry = QtWidgets.QDesktopWidget().availableGeometry()
        x = (screen_geometry.width() - about_dialog.width()) // 2
        y = (screen_geometry.height() - about_dialog.height()) // 2
        about_dialog.move(x, y)

        # Create a QTextBrowser to display Markdown
        text_browser = QtWidgets.QTextBrowser(about_dialog)
        text_browser.setGeometry(10, 10, 580, 380)

        # Load and set Markdown content
        try:
            with open("README.md", "r", encoding="utf-8") as file:
                readme_content = file.read()
                # setMarkdown method to render Markdown
                text_browser.setMarkdown(readme_content)
                text_browser.setStyleSheet("""
                    QTextBrowser {
                        background-color: #f9f9f9; 
                        color: #333; 
                        font-family: Arial, sans-serif; 
                        font-size: 14px; 
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    }
                    code { 
                        background-color: #f0f0f0; 
                        color: #e74c3c; 
                        padding: 2px 4px; 
                        border-radius: 4px; 
                        font-family: Consolas, monospace;
                    }
                """)
        except FileNotFoundError:
            text_browser.setPlainText("README.md file not found.")
        about_dialog.exec_()

    def erase_warning(self):
        all_items = self.scene.items()
        if not all_items:
            QtWidgets.QMessageBox.information(self, "Erase", "No item selected to erase.")
            return
        reply = QtWidgets.QMessageBox.warning(
            self,
            "Erase",
            "Are you sure you want to erase everything?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            for item in all_items:
                self.scene.removeItem(item)
            print("Selected item(s) erased.")

    def undo_function(self):
        """Undo the last action."""
        all_items = self.scene.items()
        
        if all_items:
            item = all_items.pop(0)
            self.scene.removeItem(item)
            self.items_deletes.append(item)

    def redo_function(self):
        """Redo the last undone action."""
        if self.items_deletes:
            item = self.items_deletes.pop()
            self.scene.addItem(item)
            self.items_redo.append(item)

    def create_menus(self):
        # Menubar actions
        menubar = self.menuBar()

        # File menu
        menu_file = menubar.addMenu('F&ile')
        menu_file.addAction(self.action_file_new)
        menu_file.addSeparator()
        menu_file.addAction(self.action_file_open)
        menu_file.addAction(self.action_file_save)
        menu_file.addAction(self.action_file_save_as)
        menu_file.addSeparator()
        menu_file.addAction(self.action_file_exit)

        self.addAction(self.action_undo)  # This action will not show in the menu
        self.addAction(self.action_redo)  # This action will not show in the menu
        
        # Tools menu
        menu_tool = menubar.addMenu('&Tools')
        menu_tool.addAction(self.action_tools_line)
        menu_tool.addAction(self.action_tools_rectangle)
        menu_tool.addAction(self.action_tools_ellipse)
        menu_tool.addAction(self.action_tools_polygon)
        menu_tool.addAction(self.action_tools_text)

        # Style menu
        menu_style = menubar.addMenu('&Style')
        menu_style_pen = menu_style.addMenu(QtGui.QIcon('Icons/tool_pen.png'),'&Pen')
        menu_style_pen.addAction(self.action_style_pen_color)
        menu_style_pen.addAction(self.action_style_pen_line_style)
        menu_style_pen.addAction(self.action_style_pen_width)
        menu_style_brush = menu_style.addMenu(QtGui.QIcon('Icons/brush.png'),'&Brush')
        menu_style_brush.addAction(self.action_style_brush_color)
        menu_style_brush.addAction(self.action_style_brush_fill)
        menu_style.addSeparator()
        menu_style.addAction(self.action_style_font)

        # Help menu
        menu_help = menubar.addMenu('&Help')
        menu_help.addAction(QtGui.QIcon('Icons/about_us.png'),'About Us', self.help_about_us)
        menu_help.addAction(QtGui.QIcon('Icons/about_qt.png'),'About Qt', self.help_about_qt)
        menu_help.addAction(QtGui.QIcon('Icons/about_app.png'),'About the Application', self.help_about_application)
        statusbar=self.statusBar()

    def resizeEvent(self, event):
        print("MainWindow.resizeEvent() : View")
        if self.view :
            print("dx : ",self.size().width()-self.view.size().width())
            print("dy : ",self.size().height()-self.view.size().height())
        else :
            print("MainWindow need  a view !!!!! ")
        print("menubar size : ", self.menuBar().size())

    #Popup Menu
    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)

        # Tools menu
        action_tools = menu.addMenu(QtGui.QIcon('Icons/tools.png'),"Tools")
        action_line = action_tools.addAction(QtGui.QIcon('Icons/tool_line.png'),"Line")
        action_rectangle = action_tools.addAction(QtGui.QIcon('Icons/tool_rectangle.png'),"Rectangle")
        action_ellipse = action_tools.addAction(QtGui.QIcon('Icons/tool_ellipse.png'),"Ellipse")
        action_polygon = action_tools.addAction(QtGui.QIcon('Icons/tool_polygon.png'),"Polygon")
        action_text = action_tools.addAction(QtGui.QIcon('Icons/tool_text.png'),"Text")

        # Style menu
        action_style = menu.addMenu(QtGui.QIcon('Icons/style.png'),"Style")
        menu_style_pen = action_style.addMenu(QtGui.QIcon('Icons/tool_pen.png'),'&Pen')
        action_pen_color = menu_style_pen.addAction(QtGui.QIcon('Icons/colorize.png'),"Color")
        action_line_style = menu_style_pen.addAction(QtGui.QIcon('Icons/line_style.png'),"Line Style")
        action_line_width = menu_style_pen.addAction(QtGui.QIcon('Icons/line_width.png'),"Line Width")
        menu_style_brush = action_style.addMenu(QtGui.QIcon('Icons/brush.png'),'&Brush')
        action_brush_color = menu_style_brush.addAction(QtGui.QIcon('Icons/colorize.png'),"Brush Color")
        action_brush_fill = menu_style_brush.addAction(QtGui.QIcon('Icons/brush_fill.png'),"Brush Fill")
        action_style.addSeparator()
        action_font = action_style.addAction(QtGui.QIcon('Icons/tool_font.png'),"Font")
        # Erase action
        menu.addSeparator()
        action_erase = menu.addAction(QtGui.QIcon('Icons/clear.png'),"Erase")

        # Connect actions to their methods
        action_line.triggered.connect(lambda: self.tools_selection(True, "line"))
        action_rectangle.triggered.connect(lambda: self.tools_selection(True, "rectangle"))
        action_ellipse.triggered.connect(lambda: self.tools_selection(True, "ellipse"))
        action_polygon.triggered.connect(lambda: self.tools_selection(True, "polygon"))
        action_text.triggered.connect(lambda: self.tools_selection(True, "text"))

        action_pen_color.triggered.connect(self.style_pen_color_selection)
        action_line_style.triggered.connect(self.style_pen_line_style_selection)
        action_line_width.triggered.connect(self.style_pen_width_selection)
        action_brush_color.triggered.connect(self.style_brush_color_selection)
        action_brush_fill.triggered.connect(self.style_brush_fill_selection)
        action_font.triggered.connect(self.style_font_selection)

        action_erase.triggered.connect(self.erase_warning)

        # Execute the context menu
        menu.exec_(event.globalPos())
            
if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)

    position=0,0
    dimension=600,400

    mw=Window(position,dimension)

    offset=5
    xd,yd=offset,offset
    xf,yf=200+offset,100+offset
    line=QtWidgets.QGraphicsLineItem(xd,yd,xf,yf)
    line.setPen(mw.get_view().get_pen())
    # mw.get_scene().addItem(line)

    mw.show()

    sys.exit(app.exec_())