# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/support/preference.ui'
#
# Created: Mon Nov  7 18:31:02 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Preference(object):
    def setupUi(self, Preference):
        Preference.setObjectName(_fromUtf8("Preference"))
        Preference.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Preference)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.settings = QtGui.QPlainTextEdit(Preference)
        self.settings.setObjectName(_fromUtf8("settings"))
        self.verticalLayout.addWidget(self.settings)

        self.retranslateUi(Preference)
        QtCore.QMetaObject.connectSlotsByName(Preference)

    def retranslateUi(self, Preference):
        Preference.setWindowTitle(_('Form'))
