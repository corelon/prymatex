# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configthemes.ui'
#
# Created: Fri Jul  1 21:03:41 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.translation import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FontThemeConfig(object):
    def setupUi(self, FontThemeConfig):
        FontThemeConfig.setObjectName(_fromUtf8("FontThemeConfig"))
        FontThemeConfig.resize(518, 467)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/format-font-size-more.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FontThemeConfig.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(FontThemeConfig)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(FontThemeConfig)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineFont = QtGui.QLineEdit(FontThemeConfig)
        self.lineFont.setReadOnly(True)
        self.lineFont.setObjectName(_fromUtf8("lineFont"))
        self.horizontalLayout.addWidget(self.lineFont)
        self.pushButtonChangeFont = QtGui.QPushButton(FontThemeConfig)
        self.pushButtonChangeFont.setObjectName(_fromUtf8("pushButtonChangeFont"))
        self.horizontalLayout.addWidget(self.pushButtonChangeFont)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(FontThemeConfig)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBoxThemes = QtGui.QComboBox(self.groupBox)
        self.comboBoxThemes.setObjectName(_fromUtf8("comboBoxThemes"))
        self.horizontalLayout_2.addWidget(self.comboBoxThemes)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.pushButtonForeground = QtGui.QPushButton(self.groupBox)
        self.pushButtonForeground.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonForeground.setText(_fromUtf8(""))
        self.pushButtonForeground.setObjectName(_fromUtf8("pushButtonForeground"))
        self.gridLayout.addWidget(self.pushButtonForeground, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.pushButtonInvisibles = QtGui.QPushButton(self.groupBox)
        self.pushButtonInvisibles.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonInvisibles.setText(_fromUtf8(""))
        self.pushButtonInvisibles.setObjectName(_fromUtf8("pushButtonInvisibles"))
        self.gridLayout.addWidget(self.pushButtonInvisibles, 0, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.pushButtonBackground = QtGui.QPushButton(self.groupBox)
        self.pushButtonBackground.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonBackground.setText(_fromUtf8(""))
        self.pushButtonBackground.setObjectName(_fromUtf8("pushButtonBackground"))
        self.gridLayout.addWidget(self.pushButtonBackground, 1, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 1, 2, 1, 1)
        self.pushButtonLineHighlight = QtGui.QPushButton(self.groupBox)
        self.pushButtonLineHighlight.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonLineHighlight.setText(_fromUtf8(""))
        self.pushButtonLineHighlight.setObjectName(_fromUtf8("pushButtonLineHighlight"))
        self.gridLayout.addWidget(self.pushButtonLineHighlight, 1, 3, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.pushButtonSelection = QtGui.QPushButton(self.groupBox)
        self.pushButtonSelection.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonSelection.setText(_fromUtf8(""))
        self.pushButtonSelection.setObjectName(_fromUtf8("pushButtonSelection"))
        self.gridLayout.addWidget(self.pushButtonSelection, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)
        self.pushButtonCaret = QtGui.QPushButton(self.groupBox)
        self.pushButtonCaret.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonCaret.setText(_fromUtf8(""))
        self.pushButtonCaret.setObjectName(_fromUtf8("pushButtonCaret"))
        self.gridLayout.addWidget(self.pushButtonCaret, 2, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tableView = QtGui.QTableView(self.groupBox)
        self.tableView.setShowGrid(False)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButtonAdd = QtGui.QPushButton(self.groupBox)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.horizontalLayout_3.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(self.groupBox)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.horizontalLayout_3.addWidget(self.pushButtonRemove)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_3.addWidget(self.label_9)
        self.comboBoxScope = QtGui.QComboBox(self.groupBox)
        self.comboBoxScope.setEditable(True)
        self.comboBoxScope.setObjectName(_fromUtf8("comboBoxScope"))
        self.horizontalLayout_3.addWidget(self.comboBoxScope)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(FontThemeConfig)
        QtCore.QMetaObject.connectSlotsByName(FontThemeConfig)

    def retranslateUi(self, FontThemeConfig):
        FontThemeConfig.setWindowTitle(_('Font and Theme'))
        self.label.setText(_('Font'))
        self.pushButtonChangeFont.setText(_('&Change Font'))
        self.groupBox.setTitle(_('Themes'))
        self.label_2.setText(_('Current theme'))
        self.label_3.setText(_('Foreground'))
        self.label_6.setText(_('Invisibles'))
        self.label_4.setText(_('Background'))
        self.label_8.setText(_('Line Highlight'))
        self.label_5.setText(_('Selection'))
        self.label_7.setText(_('Caret'))
        self.pushButtonAdd.setText(_('+'))
        self.pushButtonRemove.setText(_('-'))
        self.label_9.setText(_('Scope Selector'))
        self.checkBox.setText(_('Antialias'))

