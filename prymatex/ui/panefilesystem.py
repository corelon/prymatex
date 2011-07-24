# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/panefilesystem.ui'
#
# Created: Sat Jul 23 13:30:00 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FSPane(object):
    def setupUi(self, FSPane):
        FSPane.setObjectName(_fromUtf8("FSPane"))
        FSPane.resize(282, 457)
        FSPane.setStyleSheet(_fromUtf8("QPushButton {\n"
"    padding: 5px;\n"
"\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(FSPane)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.setSpacing(-1)
        self.buttonsLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.buttonsLayout.setObjectName(_fromUtf8("buttonsLayout"))
        self.buttonUp = QtGui.QPushButton(FSPane)
        self.buttonUp.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonUp.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonUp.setIcon(icon)
        self.buttonUp.setIconSize(QtCore.QSize(16, 16))
        self.buttonUp.setFlat(True)
        self.buttonUp.setObjectName(_fromUtf8("buttonUp"))
        self.buttonsLayout.addWidget(self.buttonUp)
        self.buttonBackRoot = QtGui.QPushButton(FSPane)
        self.buttonBackRoot.setMaximumSize(QtCore.QSize(24, 24))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-previous.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonBackRoot.setIcon(icon1)
        self.buttonBackRoot.setIconSize(QtCore.QSize(16, 16))
        self.buttonBackRoot.setFlat(True)
        self.buttonBackRoot.setObjectName(_fromUtf8("buttonBackRoot"))
        self.buttonsLayout.addWidget(self.buttonBackRoot)
        self.pushFowardRoot = QtGui.QPushButton(FSPane)
        self.pushFowardRoot.setMaximumSize(QtCore.QSize(24, 24))
        self.pushFowardRoot.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-next.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushFowardRoot.setIcon(icon2)
        self.pushFowardRoot.setFlat(True)
        self.pushFowardRoot.setObjectName(_fromUtf8("pushFowardRoot"))
        self.buttonsLayout.addWidget(self.pushFowardRoot)
        self.buttonFilter = QtGui.QPushButton(FSPane)
        self.buttonFilter.setMaximumSize(QtCore.QSize(24, 24))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/view-filter.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonFilter.setIcon(icon3)
        self.buttonFilter.setIconSize(QtCore.QSize(16, 16))
        self.buttonFilter.setFlat(True)
        self.buttonFilter.setObjectName(_fromUtf8("buttonFilter"))
        self.buttonsLayout.addWidget(self.buttonFilter)
        self.buttonSyncTabFile = QtGui.QPushButton(FSPane)
        self.buttonSyncTabFile.setMaximumSize(QtCore.QSize(24, 24))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/system-switch-user.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonSyncTabFile.setIcon(icon4)
        self.buttonSyncTabFile.setIconSize(QtCore.QSize(16, 16))
        self.buttonSyncTabFile.setCheckable(True)
        self.buttonSyncTabFile.setFlat(True)
        self.buttonSyncTabFile.setObjectName(_fromUtf8("buttonSyncTabFile"))
        self.buttonsLayout.addWidget(self.buttonSyncTabFile)
        self.buttonCollapseAll = QtGui.QPushButton(FSPane)
        self.buttonCollapseAll.setMaximumSize(QtCore.QSize(24, 24))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/debug-step-into.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCollapseAll.setIcon(icon5)
        self.buttonCollapseAll.setIconSize(QtCore.QSize(16, 16))
        self.buttonCollapseAll.setFlat(True)
        self.buttonCollapseAll.setObjectName(_fromUtf8("buttonCollapseAll"))
        self.buttonsLayout.addWidget(self.buttonCollapseAll)
        self.pushShowHidden = QtGui.QPushButton(FSPane)
        self.pushShowHidden.setMaximumSize(QtCore.QSize(24, 24))
        self.pushShowHidden.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/help-hint.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushShowHidden.setIcon(icon6)
        self.pushShowHidden.setCheckable(True)
        self.pushShowHidden.setFlat(True)
        self.pushShowHidden.setObjectName(_fromUtf8("pushShowHidden"))
        self.buttonsLayout.addWidget(self.pushShowHidden)
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.buttonsLayout)
        self.bookmarksLayout = QtGui.QHBoxLayout()
        self.bookmarksLayout.setObjectName(_fromUtf8("bookmarksLayout"))
        self.comboBookmarks = QtGui.QComboBox(FSPane)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBookmarks.sizePolicy().hasHeightForWidth())
        self.comboBookmarks.setSizePolicy(sizePolicy)
        self.comboBookmarks.setObjectName(_fromUtf8("comboBookmarks"))
        self.bookmarksLayout.addWidget(self.comboBookmarks)
        self.verticalLayout.addLayout(self.bookmarksLayout)
        self.tree = FSTree(FSPane)
        self.tree.setObjectName(_fromUtf8("tree"))
        self.verticalLayout.addWidget(self.tree)

        self.retranslateUi(FSPane)
        QtCore.QMetaObject.connectSlotsByName(FSPane)

    def retranslateUi(self, FSPane):
        FSPane.setWindowTitle(_('Form'))
        self.buttonUp.setToolTip(_('Go up one level'))
        self.buttonBackRoot.setToolTip(_('Go previous place'))
        self.pushFowardRoot.setToolTip(_('Go next place'))
        self.buttonFilter.setToolTip(_('Filter settings'))
        self.buttonSyncTabFile.setToolTip(_('Sync folder with current editor file path'))
        self.buttonCollapseAll.setToolTip(_('Collapse Folder'))
        self.pushShowHidden.setToolTip(_('Show Hidden Files'))
        self.comboBookmarks.setToolTip(_('Folders'))

from prymatex.gui.panes.fstree import FSTree
from prymatex import resources_rc
