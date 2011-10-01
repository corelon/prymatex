# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/editorstatus.ui'
#
# Created: Sat Oct  1 12:07:57 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CodeEditorStatus(object):
    def setupUi(self, CodeEditorStatus):
        CodeEditorStatus.setObjectName(_fromUtf8("CodeEditorStatus"))
        CodeEditorStatus.resize(721, 254)
        self.verticalLayout = QtGui.QVBoxLayout(CodeEditorStatus)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widgetStatus = QtGui.QWidget(CodeEditorStatus)
        self.widgetStatus.setObjectName(_fromUtf8("widgetStatus"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widgetStatus)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelLineColumn = QtGui.QLabel(self.widgetStatus)
        self.labelLineColumn.setObjectName(_fromUtf8("labelLineColumn"))
        self.horizontalLayout_2.addWidget(self.labelLineColumn)
        self.comboBoxSyntaxes = QtGui.QComboBox(self.widgetStatus)
        self.comboBoxSyntaxes.setObjectName(_fromUtf8("comboBoxSyntaxes"))
        self.horizontalLayout_2.addWidget(self.comboBoxSyntaxes)
        self.comboBoxTabSize = QtGui.QComboBox(self.widgetStatus)
        self.comboBoxTabSize.setObjectName(_fromUtf8("comboBoxTabSize"))
        self.horizontalLayout_2.addWidget(self.comboBoxTabSize)
        self.comboBoxSymbols = QtGui.QComboBox(self.widgetStatus)
        self.comboBoxSymbols.setObjectName(_fromUtf8("comboBoxSymbols"))
        self.horizontalLayout_2.addWidget(self.comboBoxSymbols)
        self.verticalLayout.addWidget(self.widgetStatus)
        self.widgetCommand = QtGui.QWidget(CodeEditorStatus)
        self.widgetCommand.setObjectName(_fromUtf8("widgetCommand"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widgetCommand)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonCommandClose = QtGui.QPushButton(self.widgetCommand)
        self.pushButtonCommandClose.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/dialog-close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCommandClose.setIcon(icon)
        self.pushButtonCommandClose.setFlat(True)
        self.pushButtonCommandClose.setObjectName(_fromUtf8("pushButtonCommandClose"))
        self.horizontalLayout.addWidget(self.pushButtonCommandClose)
        self.label = QtGui.QLabel(self.widgetCommand)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEditCommand = QtGui.QLineEdit(self.widgetCommand)
        self.lineEditCommand.setObjectName(_fromUtf8("lineEditCommand"))
        self.horizontalLayout.addWidget(self.lineEditCommand)
        self.label_2 = QtGui.QLabel(self.widgetCommand)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBoxInput = QtGui.QComboBox(self.widgetCommand)
        self.comboBoxInput.setObjectName(_fromUtf8("comboBoxInput"))
        self.horizontalLayout.addWidget(self.comboBoxInput)
        self.label_3 = QtGui.QLabel(self.widgetCommand)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.comboBoxOutput = QtGui.QComboBox(self.widgetCommand)
        self.comboBoxOutput.setObjectName(_fromUtf8("comboBoxOutput"))
        self.horizontalLayout.addWidget(self.comboBoxOutput)
        self.verticalLayout.addWidget(self.widgetCommand)
        self.widgetGoToLine = QtGui.QWidget(CodeEditorStatus)
        self.widgetGoToLine.setObjectName(_fromUtf8("widgetGoToLine"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widgetGoToLine)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButtonGoToLineClose = QtGui.QPushButton(self.widgetGoToLine)
        self.pushButtonGoToLineClose.setText(_fromUtf8(""))
        self.pushButtonGoToLineClose.setIcon(icon)
        self.pushButtonGoToLineClose.setFlat(True)
        self.pushButtonGoToLineClose.setObjectName(_fromUtf8("pushButtonGoToLineClose"))
        self.horizontalLayout_3.addWidget(self.pushButtonGoToLineClose)
        self.labelGoToLine = QtGui.QLabel(self.widgetGoToLine)
        self.labelGoToLine.setObjectName(_fromUtf8("labelGoToLine"))
        self.horizontalLayout_3.addWidget(self.labelGoToLine)
        self.spinBoxGoToLine = QtGui.QSpinBox(self.widgetGoToLine)
        self.spinBoxGoToLine.setMinimum(1)
        self.spinBoxGoToLine.setMaximum(1000)
        self.spinBoxGoToLine.setObjectName(_fromUtf8("spinBoxGoToLine"))
        self.horizontalLayout_3.addWidget(self.spinBoxGoToLine)
        spacerItem = QtGui.QSpacerItem(154, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widgetGoToLine)
        self.widgetFindReplace = QtGui.QWidget(CodeEditorStatus)
        self.widgetFindReplace.setObjectName(_fromUtf8("widgetFindReplace"))
        self.gridLayout = QtGui.QGridLayout(self.widgetFindReplace)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonFindReplaceClose = QtGui.QPushButton(self.widgetFindReplace)
        self.pushButtonFindReplaceClose.setText(_fromUtf8(""))
        self.pushButtonFindReplaceClose.setIcon(icon)
        self.pushButtonFindReplaceClose.setFlat(True)
        self.pushButtonFindReplaceClose.setObjectName(_fromUtf8("pushButtonFindReplaceClose"))
        self.gridLayout.addWidget(self.pushButtonFindReplaceClose, 0, 0, 1, 1)
        self.labelFind = QtGui.QLabel(self.widgetFindReplace)
        self.labelFind.setObjectName(_fromUtf8("labelFind"))
        self.gridLayout.addWidget(self.labelFind, 0, 1, 1, 1)
        self.labelReplace = QtGui.QLabel(self.widgetFindReplace)
        self.labelReplace.setObjectName(_fromUtf8("labelReplace"))
        self.gridLayout.addWidget(self.labelReplace, 1, 1, 1, 1)
        self.lineFind = QtGui.QLineEdit(self.widgetFindReplace)
        self.lineFind.setObjectName(_fromUtf8("lineFind"))
        self.gridLayout.addWidget(self.lineFind, 0, 2, 1, 1)
        self.lineReplace = QtGui.QLineEdit(self.widgetFindReplace)
        self.lineReplace.setObjectName(_fromUtf8("lineReplace"))
        self.gridLayout.addWidget(self.lineReplace, 1, 2, 1, 1)
        self.pushButtonFindPrevious = QtGui.QPushButton(self.widgetFindReplace)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-previous-view.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonFindPrevious.setIcon(icon1)
        self.pushButtonFindPrevious.setObjectName(_fromUtf8("pushButtonFindPrevious"))
        self.gridLayout.addWidget(self.pushButtonFindPrevious, 0, 3, 1, 1)
        self.pushButtonFindNext = QtGui.QPushButton(self.widgetFindReplace)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-next-view.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonFindNext.setIcon(icon2)
        self.pushButtonFindNext.setObjectName(_fromUtf8("pushButtonFindNext"))
        self.gridLayout.addWidget(self.pushButtonFindNext, 0, 4, 1, 1)
        self.pushButtonReplacePrevious = QtGui.QPushButton(self.widgetFindReplace)
        self.pushButtonReplacePrevious.setObjectName(_fromUtf8("pushButtonReplacePrevious"))
        self.gridLayout.addWidget(self.pushButtonReplacePrevious, 1, 3, 1, 1)
        self.pushButtonReplaceNext = QtGui.QPushButton(self.widgetFindReplace)
        self.pushButtonReplaceNext.setObjectName(_fromUtf8("pushButtonReplaceNext"))
        self.gridLayout.addWidget(self.pushButtonReplaceNext, 1, 4, 1, 1)
        self.verticalLayout.addWidget(self.widgetFindReplace)

        self.retranslateUi(CodeEditorStatus)
        QtCore.QMetaObject.connectSlotsByName(CodeEditorStatus)

    def retranslateUi(self, CodeEditorStatus):
        CodeEditorStatus.setWindowTitle(_('Form'))
        self.labelLineColumn.setText(_('Line: 0 Column: 0'))
        self.label.setText(_('Command:'))
        self.label_2.setText(_('Input:'))
        self.label_3.setText(_('Output:'))
        self.labelGoToLine.setText(_('Go to line:'))
        self.labelFind.setText(_('Find:'))
        self.labelReplace.setText(_('Replace:'))
        self.pushButtonFindPrevious.setText(_('Previous'))
        self.pushButtonFindNext.setToolTip(_('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;">\n<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Find Previous</p></body></html>'))
        self.pushButtonFindNext.setText(_('Next'))
        self.pushButtonReplacePrevious.setToolTip(_('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:\'Nimbus Mono L\'; font-size:8pt; font-weight:600; font-style:normal;">\n<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Replace &amp; Find Previous</p></body></html>'))
        self.pushButtonReplacePrevious.setText(_('Replace'))
        self.pushButtonReplaceNext.setText(_('Replace &All'))

from prymatex import resources_rc
