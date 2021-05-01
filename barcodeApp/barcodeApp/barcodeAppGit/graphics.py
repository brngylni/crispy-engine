from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget


class Ui_Form(QWidget):
    
    def __init__(self):
        super(Ui_Form, self).__init__()
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1650, 800)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(0, 50, 1650, 650))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.btnClearScene = QtWidgets.QPushButton(Form)
        self.btnClearScene.setText("Clear")
        self.btnClearScene.setEnabled(True)
        self.btnClearScene.setGeometry(QtCore.QRect(650, 660, 121, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnClearScene.setFont(font)
        self.btnClearScene.setObjectName("btnClearScene")
        self.btnPrint = QtWidgets.QPushButton(Form)
        self.btnPrint.setText("Print")
        self.btnPrint.setEnabled(True)
        self.btnPrint.setGeometry(QtCore.QRect(850, 660, 121, 30))
        self.btnPrint.setFont(font)
        self.btnPrint.setObjectName("btnPrint")
        self.btnClearScene.clicked.connect(lambda: self.graphicsView.scene().clear())
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

