# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dialogs/selector.ui'
#
# Created: Fri Nov  9 18:10:44 2012
#      by: PyQt4 UI code generator snapshot-4.9.6-95094339d25b
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SelectorDialog(object):
    def setupUi(self, SelectorDialog):
        SelectorDialog.setObjectName(_fromUtf8("SelectorDialog"))
        SelectorDialog.resize(600, 371)
        SelectorDialog.setMinimumSize(QtCore.QSize(600, 371))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/prymatex/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SelectorDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(SelectorDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineFilter = QtGui.QLineEdit(SelectorDialog)
        self.lineFilter.setObjectName(_fromUtf8("lineFilter"))
        self.verticalLayout.addWidget(self.lineFilter)
        self.tableItems = QtGui.QTableView(SelectorDialog)
        self.tableItems.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableItems.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableItems.setShowGrid(False)
        self.tableItems.setObjectName(_fromUtf8("tableItems"))
        self.tableItems.horizontalHeader().setVisible(False)
        self.tableItems.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableItems)

        self.retranslateUi(SelectorDialog)
        QtCore.QMetaObject.connectSlotsByName(SelectorDialog)

    def retranslateUi(self, SelectorDialog):
        pass

