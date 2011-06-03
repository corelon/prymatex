# encoding: utf-8
'''
This module contains the main window status bar definition and widgets.
Some of the widgets defined here are:
    * The line counter
    * Syntax selector
    * 
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from prymatex.core.base import PMXObject
from prymatex.utils.i18n import ugettext as _

        
class PWMStatusLabel(QLabel):
    '''
    A label which fires a menu when it's clicked. When an action
    is 
    '''
    valueChanged = pyqtSignal(object)
    
    def __init__(self, text, parent, default = 0, *options):
        '''
        
        '''
        QLabel.__init__(self, text, parent)
        self.setToolTip(text)
        self.menu = QMenu(self)
        
        self.menu.triggered[QAction].connect(self.indentModeChangedFromMenu)
        actions = []
        for name, value in options:
            action = self.menu.addAction(name)
            action.value = value
            actions.append(action)
        if actions:
            actions[default].trigger()
        
    def mouseReleaseEvent(self, event):
        if self.menu.actions():
            self.menu.popup( event.globalPos() ) #self.menu.exec_()
    
    def indentModeChangedFromMenu(self, action):
        self.setText(action.text())
        self.valueChanged.emit(action.value)

class PMXCursorPositionLabel(QWidget):
    
    FORMAT = "Line: %5d Col: %5d"
    def __init__(self, parent):
        super(PMXCursorPositionLabel, self).__init__(parent)
        self.__text_format = self.trUtf8(self.FORMAT)
        layout = QHBoxLayout()
        #self.label = QLabel(self.trUtf8('Pos:'))
        #layout.addWidget(self.label)
        self.postionLabel = QLabel(self.text_format % (0, 0))
        fm = self.fontMetrics()
        self.postionLabel.setMinimumWidth(fm.width('0') * len(self.text_format) + 3 )
        layout.addWidget(self.postionLabel)
        self.setLayout(layout)

    @property
    def text_format(self):
        return unicode(self.__text_format)
        
    def update(self, col, line):
        self.postionLabel.setText(self.text_format % (line, col))

class PMXSymbolBox(QComboBox):
    # TODO: Implement SymbolBox
    def __init__(self, parent):
        super(PMXSymbolBox, self).__init__(parent)        
            
class PMXStatusBar(QStatusBar, PMXObject):
    # TODO: Implement indentation checks
    '''
    Main Window status bar, declares some widgets
    '''
    def __init__(self, parent ):
        QStatusBar.__init__(self, parent)
        
        self.lineColLabel = PMXCursorPositionLabel(self)

        self.comboIndentMode = PWMStatusLabel(_("Indent Mode"),
                                                 self, True,
                                                (_('Soft Tabs'), True),
                                                (_('Hard Tabs'), False),
                                                 )
        
        self.comboIndentMode.valueChanged.connect(self.setIndentMode)
        
        self.comboIndentWidth = PWMStatusLabel(_("Intendt width"), self,
                                                  -1,
                                                  ('1', 1),
                                                  ('2', 2),
                                                  ('3', 3),
                                                  ('4', 4),
                                                  ('8', 8),
                                                  )
        
        self.comboIndentWidth.valueChanged.connect(self.setIndentWidth)
        
        
        self.syntaxMenu = QComboBox(self)
        
        #No syntax
        print "Syntax..."
        bundleTableModel = self.pmxApp.supportManager.bundleTableModel
        syntaxModel = bundleTableModel.getProxyFilteringModel(type_ = 'syntax', order_by = 'name')
        self.syntaxMenu.setModelColumn(bundleTableModel._meta.colNumber('name'))
        
        self.syntaxMenu.setModel(syntaxModel)
            
        self.addPermanentWidget(self.syntaxMenu)
        self.addPermanentWidget(self.lineColLabel)
        
        self.addPermanentWidget(self.comboIndentMode)
        
        self.addPermanentWidget(self.comboIndentWidth)
        self.declareEvents()
        self.setSignals()
        
        self.mainWindow.tabWidget.currentEditorChanged.connect(self.syncToEditor)
    
    def mostrar(self, index):
        print self._combo.model()[index, 'item']
        print self._combo.model()[index, 'path']
    
    def setIndentMode(self, value):
        
        self.mainWindow.currentEditorWidget.codeEdit.softTabs = value 
    
    def setIndentWidth(self, value):
        self.warn("Tab Width %d" % value)
        self.mainWindow.currentEditorWidget.codeEdit.tabWidth = value
        
    def setSignals(self):
        #External events
        self.connect(self.mainWindow, SIGNAL('editorCursorPositionChangedEvent'), self.updatePosition )
        self.connect(self.mainWindow, SIGNAL('editorSetSyntaxEvent'), self.updateSyntax )
        self.connect(self.mainWindow, SIGNAL('tabWidgetEditorChangedEvent'), self.updateEditor )
        
        #Internal signals
        # FIXME: Connect syntax
        self.syntaxMenu.currentIndexChanged[int].connect(self.sendStatusBarSyntaxChanged)
        
        # New style
#        self.mainWindow.editorCursorPositionChangedEvent.connect( self.updatePosition )
#        self.mainWindow.editorSetSyntaxEvent.connect( self.updateSyntax )
#        self.mainWindow.tabWidgetEditorChangedEvent.connect( self.updateEditor )
#        
#        #Internal signals
#        self.syntaxMenu.currentIndexChanged[QString].connect( self.sendStatusBarSyntaxChanged )
        
    def declareEvents(self):
        self.declareEvent('statusBarSytnaxChangedEvent()')
    
    def syncToEditor(self, widget):
        editor = widget
        self.debug("Widget changed to %s", editor)
        
        try:
            codeEdit = widget.codeEdit
        except AttributeError:
            self.warn("Tab doen't seem to be a code edit")
            return
        
        # Update labels
        syn = codeEdit.syntax
        if syn:
            self.updateSyntax(None, syn)
        codeEdit.sendCursorPosChange()
        print codeEdit.softTabs
        print codeEdit.tabSize
    
    def sendStatusBarSyntaxChanged(self, index):
        syntax = self.sender().model()[index, 'item']
        #uuid = self.syntaxMenu.itemData(index).toPyObject()
        #syntax = self.pmxApp.bundleManager.getBundleItem(unicode(uuid))
        self.statusBarSytnaxChangedEvent(syntax)
        
    def updatePosition(self, source, line, col):
        self.lineColLabel.update(col, line)
    
    def updateEditor(self, source, editor):
        self.updateSyntax(source, editor.syntax)
    
    def updateSyntax(self, source, syntax):
        print "Statusbar syntax =>", syntax
        if syntax != None:
            #index = self.syntaxMenu.findText(syntax.name, Qt.MatchExactly)
            
            model =  self.syntaxMenu.model() # Proxy
            items = model.findItems(syntax.name, Qt.MatchExactly, 'name')
            print items
            #self.syntaxMenu.setCurrentIndex(index)
            
            
        else:
            self.syntaxMenu.setCurrentIndex(0)


def mostrar(*largs):
    print largs