#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fnmatch
from bisect import bisect

import uuid as uuidmodule
from PyQt4 import QtCore, QtGui

from prymatex.core.settings import pmxConfigPorperty
from prymatex.utils.decorators.memoize import dynamic_memoized
from prymatex.models.process import ExternalProcessTableModel
from prymatex.models.support import (BundleItemTreeModel, BundleItemTreeNode,
                                    ThemeListModel, ThemeStylesTableModel, 
                                    ThemeStyleTableRow)
from prymatex.models.support import (BundleItemProxyTreeModel, BundleItemTypeProxyModel, 
                                    ThemeStyleProxyTableModel, BundleListModel, 
                                    SyntaxListModel, TemplateListModel, ProjectListModel)
from prymatex.support.manager import PMXSupportBaseManager

class BundleItemMenuGroup(QtCore.QObject):
    def __init__(self, manager):
        QtCore.QObject.__init__(self, manager)
        self.manager = manager
        #The bundle menues
        self.menus = {}
        #The qt menus where a bundle menu is added
        self.containers = []
        self.manager.bundlePopulated.connect(self.on_manager_bundlePopulated)
        self.manager.bundleAdded.connect(self.on_manager_bundleAdded)
        self.manager.bundleItemChanged.connect(self.on_manager_bundleItemChanged)
        self.manager.bundleChanged.connect(self.on_manager_bundleChanged)
        self.manager.bundleRemoved.connect(self.on_manager_bundleRemoved)
        
    def appendMenu(self, menu, offset = None):
        if menu not in map(lambda (menu, offset): menu, self.containers):
            self.containers.append((menu, offset is not None and offset or len(menu.actions())))
        #Append all bundle menus in order
        for bundle, bundleMenu in iter(sorted(self.menus.iteritems(), key=lambda (bundle, bundleMenu): bundleMenu.title().replace("&","").lower())):
            menu.addMenu(bundleMenu)
        
    def buildMenu(self, items, menu, submenus, parent = None):
        for uuid in items:
            if uuid.startswith('-'):
                menu.addSeparator()
                continue
            item = self.manager.getBundleItem(uuid)
            if item != None:
                action = item.triggerItemAction(parent)
                menu.addAction(action)
            elif uuid in submenus:
                submenu = QtGui.QMenu(submenus[uuid]['name'], parent)
                
                #Conectamos el about to show para filtar un poco los items cuando se muestra el menu
                submenu.aboutToShow.connect(self.on_bundleMenu_aboutToShow)
                
                menu.addMenu(submenu)
                self.buildMenu(submenus[uuid]['items'], submenu, submenus, parent)

    def buildBundleMenu(self, bundle):
        menu = QtGui.QMenu(bundle.buildBundleAccelerator())
        menu.ID = id(bundle.mainMenu)
        
        #Conectamos el about to show para filtar un poco los items cuando se muestra el menu
        menu.aboutToShow.connect(self.on_bundleMenu_aboutToShow)
        return menu

    def addBundle(self, bundle):
        """
            Add bundle to menu collection, all bundle has one QMenu in the collection
        """
        menu = self.buildBundleMenu(bundle)
        menu.menuAction().setVisible(bundle.enabled and bundle.mainMenu is not None)
        # Primero agregarlo a los containers porque estos usan self.menus para ordenar
        self.addToContainers(menu)
        self.menus[bundle] = menu

    def menuForBundle(self, bundle):
        return self.menus.get(bundle)

    def addToContainers(self, menu):
        currentTitles = sorted(map(lambda menu: menu.title().replace("&","").lower(), self.menus.values()))
        index = bisect(currentTitles, menu.title().replace("&","").lower())
        for container, offset in self.containers:
            currentActions = container.actions()
            if index < len(currentActions) - offset:
                container.insertMenu(currentActions[offset + index], menu)
            else:
                container.addMenu(menu)

    def removeFromContainers(self, menu):
        for container, offset in self.containers:
            container.removeAction(menu.menuAction())

    def on_bundleMenu_aboutToShow(self):
        menu = self.sender()
        for action in menu.actions():
            if hasattr(action, "bundleTreeNode"):
                action.setDisabled(action.bundleTreeNode.isEditorNeeded() and not self.manager.editorAvailable)
            
    def on_manager_bundleItemChanged(self, item):
        action = item.triggerItemAction()
        if action is not None:
            text = item.buildMenuTextEntry()
            if text != action.text():
                action.setText(text)
                
    def on_manager_bundleChanged(self, bundle):
        menu = self.menus[bundle]
        title = bundle.buildBundleAccelerator()
        if title != menu.title():
            self.removeFromContainers(menu)
            menu.setTitle(title)
            self.addToContainers(menu)
        if bundle.enabled != menu.menuAction().isVisible():
            menu.menuAction().setVisible(bundle.enabled and bundle.mainMenu is not None)
        if id(bundle.mainMenu) != menu.ID:
            # TODO Ver si no tengo que desconectar las señales de los submenues
            menu.clear()
            submenus = bundle.mainMenu['submenus'] if bundle.mainMenu is not None and 'submenus' in bundle.mainMenu else {}
            items = bundle.mainMenu['items'] if 'items' in bundle.mainMenu else []
            self.buildMenu(items, menu, submenus, menu)
            menu.ID = id(bundle.mainMenu)

    def on_manager_bundleAdded(self, bundle):
        assert bundle not in self.menus, "The bundle is in menus"
        self.addBundle(bundle)

    def on_manager_bundlePopulated(self, bundle):
        menu = self.menus[bundle]
        menu.clear()
        if bundle.mainMenu is not None:
            submenus = bundle.mainMenu['submenus'] if 'submenus' in bundle.mainMenu else {}
            items = bundle.mainMenu['items'] if 'items' in bundle.mainMenu else []
            self.buildMenu(items, menu, submenus, menu)

    def on_manager_bundleRemoved(self, bundle):
        self.removeFromContainers(self.menus[bundle])

class SupportManager(QtCore.QObject, PMXSupportBaseManager):
    #Signals for bundle
    bundleAdded = QtCore.pyqtSignal(object)
    bundleRemoved = QtCore.pyqtSignal(object)
    bundleChanged = QtCore.pyqtSignal(object)
    bundlePopulated = QtCore.pyqtSignal(object)

    #Signals for bundle items
    bundleItemAdded = QtCore.pyqtSignal(object)
    bundleItemRemoved = QtCore.pyqtSignal(object)
    bundleItemChanged = QtCore.pyqtSignal(object)
    bundleItemTriggered = QtCore.pyqtSignal(object)
    
    #Signals for themes
    themeAdded = QtCore.pyqtSignal(object)
    themeRemoved = QtCore.pyqtSignal(object)
    themeChanged = QtCore.pyqtSignal(object)
    
    #Settings
    shellVariables = pmxConfigPorperty(default = [], tm_name = u'OakShelVariables')
    
    @pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDeletedBundles')
    def deleted(self, deleted):
        self.deletedObjects = map(lambda uuid: uuidmodule.UUID(uuid), deleted)
        
    @pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDeletedBundles')
    def disabled(self, disabled):
        self.disabledObjects = map(lambda uuid: uuidmodule.UUID(uuid), disabled)
    
    #http://manual.macromates.com/en/expert_preferences.html
    #When you create a new item in the bundle editor without having selected a bundle first, then the bundle with the UUID held by this defaults key is used as the target
    defaultBundleForNewBundleItems = pmxConfigPorperty(default = u'B7BC3FFD-6E4B-11D9-91AF-000D93589AF6', tm_name = u'OakDefaultBundleForNewBundleItems')
        
    SETTINGS_GROUP = 'SupportManager'
    
    def __init__(self, application):
        QtCore.QObject.__init__(self)
        PMXSupportBaseManager.__init__(self)
        self.application = application
        self.bundleTreeModel = BundleItemTreeModel(self)
        self.themeListModel = ThemeListModel(self)
        self.themeStylesTableModel = ThemeStylesTableModel(self)
        self.processTableModel = ExternalProcessTableModel(self)
        
        #STYLE PROXY
        self.themeStyleProxyModel = ThemeStyleProxyTableModel(self)
        self.themeStyleProxyModel.setSourceModel(self.themeStylesTableModel)

        #TREE PROXY
        self.bundleProxyTreeModel = BundleItemProxyTreeModel(self)
        self.bundleProxyTreeModel.setSourceModel(self.bundleTreeModel)

        #BUNDLES
        self.bundleProxyModel = BundleListModel(self)
        self.bundleProxyModel.setSourceModel(self.bundleTreeModel)
        
        #TEMPLATES
        self.templateProxyModel = TemplateListModel(self)
        self.templateProxyModel.setSourceModel(self.bundleTreeModel)
        
        #PROJECTS
        self.projectProxyModel = ProjectListModel(self)
        self.projectProxyModel.setSourceModel(self.bundleTreeModel)

        #SYNTAX
        self.syntaxProxyModel = SyntaxListModel(self)
        self.syntaxProxyModel.setSourceModel(self.bundleTreeModel)
        
        #INTERACTIVEITEMS
        self.actionItemsProxyModel = BundleItemTypeProxyModel(["command", "snippet", "macro"], self)
        self.actionItemsProxyModel.setSourceModel(self.bundleTreeModel)
        
        #PREFERENCES
        self.preferenceProxyModel = BundleItemTypeProxyModel("preference", self)
        self.preferenceProxyModel.setSourceModel(self.bundleTreeModel)
        
        #DRAGCOMMANDS
        self.dragcommandProxyModel = BundleItemTypeProxyModel("dragcommand", self)
        self.dragcommandProxyModel.setSourceModel(self.bundleTreeModel)
        
        #BUNDLEMENUGROUP
        self.bundleMenuGroup = BundleItemMenuGroup(self)

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.environment import PMXEnvVariablesWidget
        return [ PMXEnvVariablesWidget ]

    def setEditorAvailable(self, available):
        self.editorAvailable = available

    def appendMenuToBundleMenuGroup(self, menu, offset = None):
        self.bundleMenuGroup.appendMenu(menu, offset)

    def menuForBundle(self, bundle):
        return self.bundleMenuGroup.menuForBundle(bundle)
        
    #---------------------------------------------------
    # Environment
    #---------------------------------------------------
    def environmentVariables(self):
        environment = PMXSupportBaseManager.buildEnvironment(self)
        #Extend wiht the user shell variables
        for var in self.shellVariables:
            if var['enabled']:
                environment[var['variable']] = var['value']
        return environment
    
    def buildEnvironment(self, systemEnvironment = True):
        env = PMXSupportBaseManager.buildEnvironment(self, systemEnvironment)
        for var in self.shellVariables:
            if var['enabled']:
                env[var['variable']] = var['value']
        return env
    
    # Override loadSupport for emit signals
    def loadSupport(self, *largs, **kwargs):
        PMXSupportBaseManager.loadSupport(self, *largs, **kwargs)
        self.bundleProxyTreeModel.sort(0, QtCore.Qt.AscendingOrder)
        self.bundleProxyTreeModel.setDynamicSortFilter(True)

    def runProcess(self, context, callback):
        if context.asynchronous:
            return self.runQProcess(context, callback)
        else:
            return PMXSupportBaseManager.runProcess(self, context, callback)
            
    #Interface
    def runQProcess(self, context, callback):
        process = QtCore.QProcess(self)
        if context.workingDirectory is not None:
            process.setWorkingDirectory(context.workingDirectory)
            
        self.processTableModel.appendProcess(process, description = context.description())

        environment = QtCore.QProcessEnvironment()
        for key, value in context.environment.iteritems():
            environment.insert(key, value)
                    
        process.setProcessEnvironment(environment)

        def onQProcessFinished(process, context, callback):
            def runCallback(exitCode):
                self.processTableModel.removeProcess(process)
                context.errorValue = str(process.readAllStandardError()).decode("utf-8")
                context.outputValue = str(process.readAllStandardOutput()).decode("utf-8")
                context.outputType = exitCode
                callback(context)
            return runCallback

        process.finished[int].connect(onQProcessFinished(process, context, callback))

        if context.inputType is not None:
            process.start(context.shellCommand, QtCore.QIODevice.ReadWrite)
            if not process.waitForStarted():
                raise Exception("No puedo correr")
            process.write(unicode(context.inputValue).encode("utf-8"))
            process.closeWriteChannel()
        else:
            process.start(context.shellCommand, QtCore.QIODevice.ReadOnly)

    def buildAdHocCommand(self, *largs, **kwargs):
        return BundleItemTreeNode(PMXSupportBaseManager.buildAdHocCommand(self, *largs, **kwargs))

    def buildAdHocSnippet(self, *largs, **kwargs):
        return BundleItemTreeNode(PMXSupportBaseManager.buildAdHocSnippet(self, *largs, **kwargs))

    #---------------------------------------------------
    # MANAGED OBJECTS OVERRIDE INTERFACE
    #---------------------------------------------------
    def setDeleted(self, uuid):
        """
        Marcar un managed object como eliminado
        """
        self.deletedObjects.append(uuid)
        deleted = map(lambda uuid: unicode(uuid).upper(), self.deletedObjects)
        self.settings.setValue('deleted', deleted)

    def isDeleted(self, uuid):
        return uuid in self.deletedObjects

    def isEnabled(self, uuid):
        return uuid not in self.disabledObjects
    
    def setDisabled(self, uuid):
        self.disabledObjects.append(uuid)
        disabled = map(lambda uuid: unicode(uuid).upper(), self.disabledObjects)
        self.settings.setValue('disabled', disabled)
        
    def setEnabled(self, uuid):
        self.disabledObjects.remove(uuid)
        disabled = map(lambda uuid: unicode(uuid).upper(), self.disabledObjects)
        self.settings.setValue('disabled', disabled)
    
    #---------------------------------------------------
    # BUNDLE OVERRIDE INTERFACE 
    #---------------------------------------------------
    def addBundle(self, bundle):
        bundleNode = BundleItemTreeNode(bundle)
        self.bundleTreeModel.appendBundle(bundleNode)
        self.bundleAdded.emit(bundleNode)
        return bundleNode
    
    def modifyBundle(self, bundle):
        self.bundleChanged.emit(bundle)
    
    def removeBundle(self, bundle):
        self.bundleTreeModel.removeBundle(bundle)
        self.bundleRemoved.emit(bundle)
    
    def getAllBundles(self):
        return self.bundleProxyModel.getAllItems()
    
    def getDefaultBundle(self):
        return self.getBundle(self.defaultBundleForNewBundleItems)
    
    def populatedBundle(self, bundle):
        self.bundlePopulated.emit(bundle)
        
    #---------------------------------------------------
    # BUNDLEITEM OVERRIDE INTERFACE 
    #---------------------------------------------------
    def addBundleItem(self, bundleItem):
        bundleItemNode = BundleItemTreeNode(bundleItem)
        self.bundleTreeModel.appendBundleItem(bundleItemNode)
        self.bundleItemAdded.emit(bundleItemNode)
        return bundleItemNode

    def modifyBundleItem(self, bundleItem):
        self.bundleItemChanged.emit(bundleItem)
        
    def removeBundleItem(self, bundleItem):
        self.bundleTreeModel.removeBundleItem(bundleItem)
        self.bundleItemRemoved.emit(bundleItem)
        
    def getAllBundleItems(self):
        nodes = []
        for bundle in self.getAllBundles():
            for node in bundle.childNodes():
                nodes.append(node)
        return nodes
        
    #---------------------------------------------------
    # TEMPLATEFILE OVERRIDE INTERFACE
    #---------------------------------------------------
    def addTemplateFile(self, file):
        bundleTemplateFileNode = BundleItemTreeNode(file)
        self.bundleTreeModel.appendTemplateFile(bundleTemplateFileNode)
        return bundleTemplateFileNode
    
    #---------------------------------------------------
    # THEME OVERRIDE INTERFACE
    #---------------------------------------------------
    def addTheme(self, theme):
        themeRow = ThemeStyleTableRow(theme, self.scores)
        self.themeListModel.appendTheme(themeRow)
        self.themeAdded.emit(themeRow)
        return themeRow
    
    def modifyTheme(self, theme):
        self.themeChanged.emit(theme)
        
    def removeTheme(self, theme):
        self.themeListModel.removeTheme(theme)
        self.themeRemoved.emit(theme)
            
    def getAllThemes(self):
        return self.themeListModel.getAllItems()
    
    #---------------------------------------------------
    # THEME STYLE OVERRIDE INTERFACE
    #---------------------------------------------------
    def addThemeStyle(self, style):
        themeStyle = ThemeStyleTableRow(style)
        self.themeStylesTableModel.appendStyle(themeStyle)
        return themeStyle
    
    def removeThemeStyle(self, style):
        self.themeStylesTableModel.removeStyle(style)

    #---------------------------------------------------
    # PREFERENCES OVERRIDE INTERFACE
    #---------------------------------------------------
    @dynamic_memoized
    def getAllPreferences(self):
        return self.preferenceProxyModel.getAllItems()
    
    #---------------------------------------------------
    # TABTRIGGERS OVERRIDE INTERFACE
    #---------------------------------------------------
    @dynamic_memoized
    def getAllTabTriggerItems(self):
        tabTriggers = []
        for item in self.actionItemsProxyModel.getAllItems():
            if item.tabTrigger != None:
                tabTriggers.append(item)
        return tabTriggers
        
    @dynamic_memoized
    def getAllBundleItemsByTabTrigger(self, tabTrigger):
        items = []
        for item in self.actionItemsProxyModel.getAllItems():
            if item.tabTrigger == tabTrigger:
                items.append(item)
        return items

    #---------------------------------------------------
    # KEYEQUIVALENT OVERRIDE INTERFACE
    #---------------------------------------------------
    @dynamic_memoized
    def getAllKeyEquivalentItems(self):
        keyEquivalent = []
        for item in self.actionItemsProxyModel.getAllItems() + self.syntaxProxyModel.getAllItems():
            if item.keyEquivalent != None:
                keyEquivalent.append(item)
        return keyEquivalent
        
    @dynamic_memoized
    def getAllBundleItemsByKeyEquivalent(self, keyEquivalent):
        items = []
        for item in self.actionItemsProxyModel.getAllItems():
            if item.keyEquivalent == keyEquivalent:
                items.append(item)
        for syntax in self.syntaxProxyModel.getAllItems():
            if syntax.keyEquivalent == keyEquivalent:
                items.append(syntax)
        return items
    
    #---------------------------------------------------
    # FILE EXTENSION OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllBundleItemsByFileExtension(self, path):
        items = []
        for item in self.dragcommandProxyModel.getAllItems():
            if any(map(lambda extension: fnmatch.fnmatch(path, "*.%s" % extension), item.draggedFileExtensions)):
                items.append(item)
        return items
    
    #---------------------------------------------------
    # ACTION ITEMS OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllActionItems(self):
        return self.actionItemsProxyModel.getAllItems()
    
    #---------------------------------------------------
    # SYNTAXES OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllSyntaxes(self):
        return self.syntaxProxyModel.getAllItems()