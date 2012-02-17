#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.ui.dialogs.treewidget import Ui_TreeWidgetDialog
from prymatex.gui.settings.models import PMXNamespacedModel, PMXPropertiesProxyModel, PMXProxyNamespacedTreeNode

class PMXProxyPropertyTreeNode(QtGui.QWidget, PMXProxyNamespacedTreeNode):
    def __init__(self, name, parent):
        QtGui.QWidget.__init__(self)
        PMXProxyNamespacedTreeNode.__init__(self, name, parent)

    def acceptFileSystemItem(self, fileSystemItem):
        return True
        
    def edit(self, fileSystemItem):
        pass

class PMXPropertiesDialog(QtGui.QDialog, Ui_TreeWidgetDialog):
    """Properties dialog, it's hold by the project docker
    """
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.baseWindowTitle = self.windowTitle()
        
        self.model = PMXNamespacedModel(self)
        self.model.proxyNodeFactory = self.proxyNodeFactory
        
        self.proxyModelProperties = PMXPropertiesProxyModel(self)
        self.proxyModelProperties.setSourceModel(self.model)
        
        self.treeView.setModel(self.proxyModelProperties)
        
        self.stackedWidget = QtGui.QStackedWidget(self.splitter)
        self.widgetsLayout.addWidget(self.stackedWidget)
    
    def proxyNodeFactory(self, name, parent):
        proxyWidget = PMXProxyPropertyTreeNode(name, parent)
        self.stackedWidget.addWidget(proxyWidget)
        return proxyWidget
        
    def on_lineEditFilter_textChanged(self, text):
        self.proxyModelProperties.setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive))
    
    def on_treeView_pressed(self, index):
        treeNode = self.proxyModelProperties.node(index)
        self.setCurrentPropertyWidget(treeNode)
        
    def on_treeView_activated(self, index):
        treeNode = self.proxyModelProperties.node(index)
        self.setCurrentPropertyWidget(treeNode)
    
    def setCurrentPropertyWidget(self, widget):
        widget.edit(self.proxyModelProperties.fileSystemItem)
        self.stackedWidget.setCurrentWidget(widget)
        self.textLabelTitle.setText(widget.title)
        self.setWindowTitle("%s - %s" % (self.baseWindowTitle, widget.title))
    
    def register(self, widget):
        index = self.stackedWidget.addWidget(widget)
        self.model.addSetting(widget)
    
    def exec_(self, fileSystemItem):
        self.proxyModelProperties.setFilterFileSystem(fileSystemItem)
        return QtGui.QDialog.exec_(self)
        