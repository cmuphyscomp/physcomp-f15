# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ArduinoConsoleWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ArduinoConsoleWindow(object):
    def setupUi(self, ArduinoConsoleWindow):
        ArduinoConsoleWindow.setObjectName(_fromUtf8("ArduinoConsoleWindow"))
        ArduinoConsoleWindow.resize(812, 631)
        self.centralwidget = QtGui.QWidget(ArduinoConsoleWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.consoleOutput = QtGui.QPlainTextEdit(self.centralwidget)
        self.consoleOutput.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.consoleOutput.setObjectName(_fromUtf8("consoleOutput"))
        self.verticalLayout.addWidget(self.consoleOutput)
        self.buttonLayout = QtGui.QHBoxLayout()
        self.buttonLayout.setObjectName(_fromUtf8("buttonLayout"))
        self.verticalLayout.addLayout(self.buttonLayout)
        self.sliderLayout = QtGui.QVBoxLayout()
        self.sliderLayout.setObjectName(_fromUtf8("sliderLayout"))
        self.verticalLayout.addLayout(self.sliderLayout)
        self.ArduinoControlsLayout = QtGui.QHBoxLayout()
        self.ArduinoControlsLayout.setObjectName(_fromUtf8("ArduinoControlsLayout"))
        self.ArduinoPortLabel = QtGui.QLabel(self.centralwidget)
        self.ArduinoPortLabel.setObjectName(_fromUtf8("ArduinoPortLabel"))
        self.ArduinoControlsLayout.addWidget(self.ArduinoPortLabel)
        self.ArduinoPortName = QtGui.QLineEdit(self.centralwidget)
        self.ArduinoPortName.setObjectName(_fromUtf8("ArduinoPortName"))
        self.ArduinoControlsLayout.addWidget(self.ArduinoPortName)
        self.resetPlotButton = QtGui.QPushButton(self.centralwidget)
        self.resetPlotButton.setObjectName(_fromUtf8("resetPlotButton"))
        self.ArduinoControlsLayout.addWidget(self.resetPlotButton)
        self.ArduinoRawSwitch = QtGui.QCheckBox(self.centralwidget)
        self.ArduinoRawSwitch.setObjectName(_fromUtf8("ArduinoRawSwitch"))
        self.ArduinoControlsLayout.addWidget(self.ArduinoRawSwitch)
        self.ArduinoConnectSwitch = QtGui.QCheckBox(self.centralwidget)
        self.ArduinoConnectSwitch.setObjectName(_fromUtf8("ArduinoConnectSwitch"))
        self.ArduinoControlsLayout.addWidget(self.ArduinoConnectSwitch)
        self.verticalLayout.addLayout(self.ArduinoControlsLayout)
        self.commandLineLayout = QtGui.QHBoxLayout()
        self.commandLineLayout.setObjectName(_fromUtf8("commandLineLayout"))
        self.commandLineLabel = QtGui.QLabel(self.centralwidget)
        self.commandLineLabel.setObjectName(_fromUtf8("commandLineLabel"))
        self.commandLineLayout.addWidget(self.commandLineLabel)
        self.commandLine = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandLine.sizePolicy().hasHeightForWidth())
        self.commandLine.setSizePolicy(sizePolicy)
        self.commandLine.setObjectName(_fromUtf8("commandLine"))
        self.commandLineLayout.addWidget(self.commandLine)
        self.verticalLayout.addLayout(self.commandLineLayout)
        ArduinoConsoleWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ArduinoConsoleWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuTitle = QtGui.QMenu(self.menubar)
        self.menuTitle.setObjectName(_fromUtf8("menuTitle"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        ArduinoConsoleWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ArduinoConsoleWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ArduinoConsoleWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuTitle.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(ArduinoConsoleWindow)
        QtCore.QObject.connect(self.ArduinoConnectSwitch, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), ArduinoConsoleWindow.ArduinoConnectToggled)
        QtCore.QObject.connect(self.ArduinoPortName, QtCore.SIGNAL(_fromUtf8("returnPressed()")), ArduinoConsoleWindow.ArduinoPortEntered)
        QtCore.QObject.connect(self.commandLine, QtCore.SIGNAL(_fromUtf8("returnPressed()")), ArduinoConsoleWindow.commandEntered)
        QtCore.QObject.connect(self.resetPlotButton, QtCore.SIGNAL(_fromUtf8("clicked()")), ArduinoConsoleWindow.resetPlotPressed)
        QtCore.QMetaObject.connectSlotsByName(ArduinoConsoleWindow)

    def retranslateUi(self, ArduinoConsoleWindow):
        ArduinoConsoleWindow.setWindowTitle(_translate("ArduinoConsoleWindow", "Arduino Console", None))
        self.consoleOutput.setToolTip(_translate("ArduinoConsoleWindow", "Console area for showing text received from Arduino.", None))
        self.ArduinoPortLabel.setText(_translate("ArduinoConsoleWindow", "Arduino Port:", None))
        self.resetPlotButton.setText(_translate("ArduinoConsoleWindow", "Reset Plot", None))
        self.ArduinoRawSwitch.setText(_translate("ArduinoConsoleWindow", "Show Raw Data", None))
        self.ArduinoConnectSwitch.setText(_translate("ArduinoConsoleWindow", "Connected", None))
        self.commandLineLabel.setText(_translate("ArduinoConsoleWindow", "Command Input:", None))
        self.commandLine.setToolTip(_translate("ArduinoConsoleWindow", "Command line for entering text to send to Arduino.", None))
        self.menuTitle.setTitle(_translate("ArduinoConsoleWindow", "File", None))
        self.menuSettings.setTitle(_translate("ArduinoConsoleWindow", "Settings", None))

