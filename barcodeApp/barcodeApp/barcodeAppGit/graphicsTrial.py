from PyQt5.QtCore import Qt, QPointF

from graphics import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsView, \
    QGraphicsScene,QGraphicsPixmapItem, QGraphicsSceneMouseEvent, \
    QGraphicsSceneHoverEvent


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()




    def addBarcode(self, barcode):
        self.ui.graphicsView.scene().addItem(Image(-150, 50, f"barcodes/{barcode}.png"))

class GraphicsTrial(QGraphicsView):
    def __init__(self, parent):
        super(GraphicsTrial, self).__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0,0,1200,1000)

class Image(QGraphicsPixmapItem):
    def __init__(self,x,y, pixmap):
        super(Image, self).__init__()
        self.setPixmap(QPixmap(pixmap))
        self.setPos(x,y)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        app.instance().restoreOverrideCursor()

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        pass
    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()
        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()

        self.setPos(QPointF(updated_cursor_x,updated_cursor_y))

    def mouseReleaseEvent(self, event) :
        pass

