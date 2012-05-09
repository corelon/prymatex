# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\ui\dockers\filesystem.ui'
#
# Created: Wed May 09 07:32:31 2012
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FileSystemDock(object):
    def setupUi(self, FileSystemDock):
        FileSystemDock.setObjectName(_fromUtf8("FileSystemDock"))
        FileSystemDock.resize(330, 484)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.setSpacing(2)
        self.buttonsLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.buttonsLayout.setObjectName(_fromUtf8("buttonsLayout"))
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.pushButtonBack = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonBack.setMaximumSize(QtCore.QSize(24, 24))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-previous.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonBack.setIcon(icon)
        self.pushButtonBack.setFlat(True)
        self.pushButtonBack.setObjectName(_fromUtf8("pushButtonBack"))
        self.buttonsLayout.addWidget(self.pushButtonBack)
        self.pushButtonFoward = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonFoward.setMaximumSize(QtCore.QSize(24, 24))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-next.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonFoward.setIcon(icon1)
        self.pushButtonFoward.setFlat(True)
        self.pushButtonFoward.setObjectName(_fromUtf8("pushButtonFoward"))
        self.buttonsLayout.addWidget(self.pushButtonFoward)
        self.pushButtonUp = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonUp.setMaximumSize(QtCore.QSize(24, 24))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonUp.setIcon(icon2)
        self.pushButtonUp.setFlat(True)
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.buttonsLayout.addWidget(self.pushButtonUp)
        self.line = QtGui.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.buttonsLayout.addWidget(self.line)
        self.pushButtonSync = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonSync.setMaximumSize(QtCore.QSize(24, 24))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/system-switch-user.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSync.setIcon(icon3)
        self.pushButtonSync.setCheckable(True)
        self.pushButtonSync.setFlat(True)
        self.pushButtonSync.setObjectName(_fromUtf8("pushButtonSync"))
        self.buttonsLayout.addWidget(self.pushButtonSync)
        self.pushButtonCollapseAll = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonCollapseAll.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonCollapseAll.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/view-list-tree.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCollapseAll.setIcon(icon4)
        self.pushButtonCollapseAll.setFlat(True)
        self.pushButtonCollapseAll.setObjectName(_fromUtf8("pushButtonCollapseAll"))
        self.buttonsLayout.addWidget(self.pushButtonCollapseAll)
        self.pushButtonCustomFilters = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonCustomFilters.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonCustomFilters.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/view-filter.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCustomFilters.setIcon(icon5)
        self.pushButtonCustomFilters.setFlat(True)
        self.pushButtonCustomFilters.setObjectName(_fromUtf8("pushButtonCustomFilters"))
        self.buttonsLayout.addWidget(self.pushButtonCustomFilters)
        self.pushButtonOptions = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonOptions.setMaximumSize(QtCore.QSize(45, 24))
        self.pushButtonOptions.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/configure.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonOptions.setIcon(icon6)
        self.pushButtonOptions.setFlat(True)
        self.pushButtonOptions.setObjectName(_fromUtf8("pushButtonOptions"))
        self.buttonsLayout.addWidget(self.pushButtonOptions)
        self.verticalLayout.addLayout(self.buttonsLayout)
        self.comboBoxLocation = QtGui.QComboBox(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxLocation.sizePolicy().hasHeightForWidth())
        self.comboBoxLocation.setSizePolicy(sizePolicy)
        self.comboBoxLocation.setEditable(True)
        self.comboBoxLocation.setObjectName(_fromUtf8("comboBoxLocation"))
        self.verticalLayout.addWidget(self.comboBoxLocation)
        self.treeViewFileSystem = QtGui.QTreeView(self.dockWidgetContents)
        self.treeViewFileSystem.setObjectName(_fromUtf8("treeViewFileSystem"))
        self.verticalLayout.addWidget(self.treeViewFileSystem)
        FileSystemDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtGui.QAction(FileSystemDock)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFile.setIcon(icon7)
        self.actionNewFile.setObjectName(_fromUtf8("actionNewFile"))
        self.actionNewFolder = QtGui.QAction(FileSystemDock)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/folder-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFolder.setIcon(icon8)
        self.actionNewFolder.setObjectName(_fromUtf8("actionNewFolder"))
        self.actionNewFromTemplate = QtGui.QAction(FileSystemDock)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/run-build-file.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFromTemplate.setIcon(icon9)
        self.actionNewFromTemplate.setObjectName(_fromUtf8("actionNewFromTemplate"))
        self.actionDelete = QtGui.QAction(FileSystemDock)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/edit-delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon10)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionOrderByName = QtGui.QAction(FileSystemDock)
        self.actionOrderByName.setCheckable(True)
        self.actionOrderByName.setObjectName(_fromUtf8("actionOrderByName"))
        self.actionOrderBySize = QtGui.QAction(FileSystemDock)
        self.actionOrderBySize.setCheckable(True)
        self.actionOrderBySize.setObjectName(_fromUtf8("actionOrderBySize"))
        self.actionOrderByDate = QtGui.QAction(FileSystemDock)
        self.actionOrderByDate.setCheckable(True)
        self.actionOrderByDate.setObjectName(_fromUtf8("actionOrderByDate"))
        self.actionOrderByType = QtGui.QAction(FileSystemDock)
        self.actionOrderByType.setCheckable(True)
        self.actionOrderByType.setObjectName(_fromUtf8("actionOrderByType"))
        self.actionOrderDescending = QtGui.QAction(FileSystemDock)
        self.actionOrderDescending.setCheckable(True)
        self.actionOrderDescending.setObjectName(_fromUtf8("actionOrderDescending"))
        self.actionOrderFoldersFirst = QtGui.QAction(FileSystemDock)
        self.actionOrderFoldersFirst.setCheckable(True)
        self.actionOrderFoldersFirst.setObjectName(_fromUtf8("actionOrderFoldersFirst"))
        self.actionOpen = QtGui.QAction(FileSystemDock)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon11)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionOpenSystemEditor = QtGui.QAction(FileSystemDock)
        self.actionOpenSystemEditor.setObjectName(_fromUtf8("actionOpenSystemEditor"))
        self.actionOpenDefaultEditor = QtGui.QAction(FileSystemDock)
        self.actionOpenDefaultEditor.setObjectName(_fromUtf8("actionOpenDefaultEditor"))
        self.actionRename = QtGui.QAction(FileSystemDock)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/edit-rename.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRename.setIcon(icon12)
        self.actionRename.setObjectName(_fromUtf8("actionRename"))
        self.actionConvertIntoProject = QtGui.QAction(FileSystemDock)
        self.actionConvertIntoProject.setIcon(icon7)
        self.actionConvertIntoProject.setObjectName(_fromUtf8("actionConvertIntoProject"))
        self.actionSetInTerminal = QtGui.QAction(FileSystemDock)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/apps/utilities-terminal.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSetInTerminal.setIcon(icon13)
        self.actionSetInTerminal.setObjectName(_fromUtf8("actionSetInTerminal"))
        self.actionCut = QtGui.QAction(FileSystemDock)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/edit-cut.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon14)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionCopy = QtGui.QAction(FileSystemDock)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/edit-copy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon15)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(FileSystemDock)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/edit-paste.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon16)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))

        self.retranslateUi(FileSystemDock)
        QtCore.QMetaObject.connectSlotsByName(FileSystemDock)

    def retranslateUi(self, FileSystemDock):
        FileSystemDock.setWindowTitle(_('File System'))
        self.pushButtonBack.setToolTip(_('Go previous place'))
        self.pushButtonFoward.setToolTip(_('Go next place'))
        self.pushButtonUp.setToolTip(_('Go up one level'))
        self.pushButtonSync.setToolTip(_('Sync folder with current editor file path'))
        self.comboBoxLocation.setToolTip(_('Folders'))
        self.actionNewFile.setText(_('File'))
        self.actionNewFolder.setText(_('Folder'))
        self.actionNewFromTemplate.setText(_('File From Template'))
        self.actionNewFromTemplate.setToolTip(_('File From Template'))
        self.actionDelete.setText(_('Delete'))
        self.actionOrderByName.setText(_('By Name'))
        self.actionOrderBySize.setText(_('By Size'))
        self.actionOrderByDate.setText(_('By Date'))
        self.actionOrderByType.setText(_('By Type'))
        self.actionOrderDescending.setText(_('Descending'))
        self.actionOrderFoldersFirst.setText(_('Folders First'))
        self.actionOpen.setText(_('Open'))
        self.actionOpenSystemEditor.setText(_('System Editor'))
        self.actionOpenDefaultEditor.setText(_('Default Editor'))
        self.actionRename.setText(_('Rename'))
        self.actionRename.setToolTip(_('Rename'))
        self.actionRename.setShortcut(_('F2'))
        self.actionConvertIntoProject.setText(_('Convert Into Project'))
        self.actionConvertIntoProject.setToolTip(_('Convert current directory into project'))
        self.actionSetInTerminal.setText(_('Set In Terminal'))
        self.actionCut.setText(_('Cu&t'))
        self.actionCut.setShortcut(_('Ctrl+X'))
        self.actionCopy.setText(_('&Copy'))
        self.actionCopy.setShortcut(_('Ctrl+C'))
        self.actionPaste.setText(_('&Paste'))
        self.actionPaste.setShortcut(_('Ctrl+V'))

from prymatex import resources_rc
