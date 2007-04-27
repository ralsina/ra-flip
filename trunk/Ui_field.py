# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/ra-flip/field.ui'
#
# Created: Fri Apr 27 10:37:28 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,611,549).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.zoomIn = QtGui.QToolButton(self.layoutWidget)
        self.zoomIn.setIcon(QtGui.QIcon("../../../../../../../opt/kde/share/icons/crystalsvg/32x32/actions/viewmag+.png"))
        self.zoomIn.setAutoRepeat(True)
        self.zoomIn.setObjectName("zoomIn")
        self.vboxlayout1.addWidget(self.zoomIn)

        self.zoomOut = QtGui.QToolButton(self.layoutWidget)
        self.zoomOut.setIcon(QtGui.QIcon("../../../../../../../opt/kde/share/icons/crystalsvg/32x32/actions/viewmag-.png"))
        self.zoomOut.setAutoRepeat(True)
        self.zoomOut.setObjectName("zoomOut")
        self.vboxlayout1.addWidget(self.zoomOut)

        self.play = QtGui.QToolButton(self.layoutWidget)
        self.play.setIcon(QtGui.QIcon("../../../../../../../opt/kde/share/icons/crystalsvg/32x32/actions/player_play.png"))
        self.play.setAutoRepeat(True)
        self.play.setObjectName("play")
        self.vboxlayout1.addWidget(self.play)

        self.stop = QtGui.QToolButton(self.layoutWidget)
        self.stop.setIcon(QtGui.QIcon("../../../../../../../opt/kde/share/icons/crystalsvg/32x32/actions/player_stop.png"))
        self.stop.setAutoRepeat(True)
        self.stop.setObjectName("stop")
        self.vboxlayout1.addWidget(self.stop)

        self.pause = QtGui.QToolButton(self.layoutWidget)
        self.pause.setIcon(QtGui.QIcon("../../../../../../../opt/kde/share/icons/crystalsvg/32x32/actions/player_pause.png"))
        self.pause.setAutoRepeat(True)
        self.pause.setObjectName("pause")
        self.vboxlayout1.addWidget(self.pause)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)
        self.hboxlayout.addLayout(self.vboxlayout1)

        self.field = QtGui.QGraphicsView(self.layoutWidget)
        self.field.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.field.setObjectName("field")
        self.hboxlayout.addWidget(self.field)

        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.vboxlayout2.addWidget(self.label)

        self.input = QtGui.QTextEdit(self.layoutWidget1)
        self.input.setObjectName("input")
        self.vboxlayout2.addWidget(self.input)
        self.hboxlayout1.addLayout(self.vboxlayout2)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setMargin(0)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.vboxlayout3.addWidget(self.label_2)

        self.output = QtGui.QTextBrowser(self.layoutWidget1)
        self.output.setObjectName("output")
        self.vboxlayout3.addWidget(self.output)
        self.hboxlayout1.addLayout(self.vboxlayout3)
        self.vboxlayout.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.zoomIn.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.zoomOut.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.play.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.stop.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pause.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Output", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
