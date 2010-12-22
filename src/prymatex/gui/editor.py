#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from prymatex.lib.i18n import ugettext as _
from prymatex.gui import PMXBaseGUIMixin
import os, codecs
from os.path import basename

from prymatex.gui.syntax import PMXSyntaxProcessor, PMXSyntaxFormatter
from prymatex.lib.textmate.syntax import TM_SYNTAXES, find_syntax_by_first_line


import logging
logger = logging.getLogger(__name__)
   
class PMXCodeEdit(QPlainTextEdit):
    _path = ''
    _tab_length = 4
    _soft_tabs = False
    
    class LineNumberArea(QWidget):
        def __init__(self, editor):
            QWidget.__init__(self, editor)
            self.codeEditor = editor
            
        def sizeHint(self):
            return QSize(self.codeEditor.lineNumberAreaWidth(), 0)
        
        def paintEvent(self, event):
            self.codeEditor.lineNumberAreaPaintEvent(event)
    
    def __init__(self, parent, path = ''):
        QTextEdit.__init__(self, parent)
        
        self.lineNumberArea = PMXCodeEdit.LineNumberArea(self)
        
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()
        self.setTabChangesFocus(False)
        
        self.syntax_processor = PMXSyntaxProcessor(self.document(), formatter = PMXSyntaxFormatter.load_from_textmate_theme('LAZY'))
        # TODO: Ver     
        self.path = path
        
        self.tab_length = 4
        self.soft_tabs = True
        self.actionMenuTab = EditorTabAction(self.title(), self)
        
        self.connect(self, SIGNAL("blockCountChanged(int)"), self.updateLineNumberAreaWidth)
        self.connect(self, SIGNAL("updateRequest(const QRect &, int)"), self.updateLineNumberArea)
        self.connect(self, SIGNAL("cursorPositionChanged()"), self.highlightCurrentLine)
        self.connect(self, SIGNAL("cursorPositionChanged()"), self.notifyCursorChange)
    
    def set_syntax(self, syntax):
        self.syntax_processor.set_syntax(syntax)
        
    # File operations
    def save(self, filename = None, save_as = False):
        '''
        @returns: Filename or None if save operation was somewhat canceled
        
        '''
        if not save_as:
            filename = filename or self.path
            
        if not filename or save_as:
            filename = QFileDialog.getSaveFileName(self, _("Save as"),
                                                    self.path or qApp.instance().startDirectory())
            if not filename:
                return
        
        # TODO: Cargar la codificación por defecto de la config
        s = codecs.open(filename, 'w', 'utf-8')
        s.write(unicode(self.toPlainText()))
        s.close()
        if filename != self.path:
            self.path = filename
            self.updateTab()
            
        self.parent().parent().parent().\
            statusBar().showMessage(_("'%s' saved.", basename(self.path)), 5000)
        self.document().setModified(False)
        
        #get_fspanel()
        return self.path
    
    def get_current_scope(self):
        cursor = self.textCursor()
        user_data = cursor.block().userData()
        return user_data and user_data.get_scope_at(cursor.columnNumber()) or ""
    
    def get_current_folding(self):
        cursor = self.textCursor()
        user_data = cursor.block().userData()
        return user_data.folding
    
    def soft_tabs(): #@NoSelf
        doc = """Soft tabs, insert spaces instead of tab""" #@UnusedVariable
       
        def fget(self):
            return self._soft_tabs
           
        def fset(self, value):
            self._soft_tabs = value
           
        return locals()
       
    soft_tabs = property(**soft_tabs())
    
    def keyPressEvent(self, event):
        key = event.key()
        cursor = self.textCursor()
        
        doc = self.document()
        start_block_pos, end_block_pos = cursor.selectionStart(), cursor.selectionEnd()
        start_block, end_block = map(doc.findBlock, (start_block_pos, end_block_pos)) 
        blocknum_start, blocknum_end = start_block.blockNumber(), end_block.blockNumber()
        
        blocknum_diff = blocknum_end - blocknum_start 
         
      
        # All keys in http://doc.trolltech.com/qtjambi-4.4/html/com/trolltech/qt/core/Qt.Key.html
        if key == Qt.Key_Tab:
            if event.modifiers() & Qt.ShiftModifier:
                print "A"
                return
            elif blocknum_diff:
                print "Moving block"
                cursor.beginEditBlock()
                cursor.movePosition(QTextCursor.StartOfBlock)
                for _i in range(blocknum_diff +1):
                    cursor.insertText(self.indent_text)
                    cursor.movePosition(QTextCursor.NextBlock)
                cursor.endEditBlock()
                return
                
            elif self.soft_tabs:
                self.textCursor().insertText(' '* self.tab_length)
                return
        elif key == 16777220 and doc.blockCount() == 1:
            #Esto es un enter y es el primer blocke que tiene el documento
            text = doc.firstBlock().text()
            syntax = find_syntax_by_first_line(text)
            if syntax != None:
                self.set_syntax(syntax)
                self.parent().currentEditorChange.emit(self)
        QPlainTextEdit.keyPressEvent(self, event)
        
    @property
    def indent_text(self):
        return self.soft_tabs and (self.tab_length * " ") or "\t"
    
    def tab_length(): #@NoSelf
        doc = """Tab length in characters""" #@UnusedVariable
       
        def fget(self):
            return self._tab_length
           
        def fset(self, value):
            if value:
                self._tab_length = value
                self.setTabStopWidth(self.fontMetrics().width('9') * value)
           
        return locals()
       
    tab_length = property(**tab_length())
    
    def contextMenuEvent(self, event):
        '''
        '''
        menu = self.createStandardContextMenu()
        #menu.insertSeparator()
        menu.addAction("Ideas to add here?")
        menu.exec_(event.globalPos())
        
    
    def replaceCursorText(self, function):
        '''
        Used for text alteration such as 
            * title case
            * uppercase
            * lowercase
        '''
        assert callable(function)
        cursor = self.textCursor() 
        selected_text =  cursor.selectedText()
        self.textCursor().beginEditBlock()
        new_text = function(selected_text)
        cursor.removeSelectedText()
        #cursor.clearSelection()
        #cursor.movePosition(QTextCursor.NoMove, QTextCursor.KeepAnchor)
        cursor.insertText(new_text)
        self.textCursor().endEditBlock()    
    
    def path(): #@NoSelf
        def fget(self):
            return self._path
        
        def fset(self, value):
            self._path = unicode(value)
            if os.path.exists(value):
                f = codecs.open(value,'r','utf-8')
                text = f.read()
                f.close()
                self.setPlainText(text)
                
            elif value: # Si no es nulo
                raise IOError("%s does not exist")
            
        doc = u"Path property QString->unicode/str"
        return locals()
    path = property(**path())
    
    def notifyCursorChange(self):
        '''
        Bubbles cursor changes
        '''
        textcursor = self.textCursor()
        col, row = textcursor.columnNumber(), textcursor.blockNumber()
        try:
            self.mainwindow.notifyCursorChange(self, row, col)
        except AttributeError:
            # Cursor changes before widget's been attached to it's panel
            # will produce mainwindow errors
            pass
        
    @property
    def mainwindow(self):
        return self.parent().parent().parent()
    #===========================================================================
    # Show dialogs
    #===========================================================================
    
    def showGoToLineDialog(self):
        doc = self.document()
        cur_pos = self.textCursor().blockNumber() + 1
        num, ok = QInputDialog.getInt(self, _("Go to line"), 
                            _("Please enter the line number:"),
                            cur_pos, 1,
                            doc.blockCount() )
        if ok:
            block = doc.findBlockByLineNumber(num)
            self.setTextCursor(QTextCursor(block))
            
    
    def showGoToSymbol(self):
        pass
    
    
    @property
    def filename(self):
        if self.path:
            return self.path
        return _("This unsaved file")
    
    def getFocus(self):
        self.setFocus(Qt.TabFocusReason)
    
    def setToolTip(self, text):
        tabwidget = self.parent().parent()
        index = tabwidget.indexOf(self)
        tabwidget.setTabToolTip(index, text)
        
    def title(self):
        tabwidget = self.parent()
        #print tabwidget, tabwidget.parent()
        index = tabwidget.indexOf(self)
        return tabwidget.tabText(index)
        
    def setTitle(self, text):
        tabwidget = self.parent().parent()
        #print tabwidget, tabwidget.parent()
        index = tabwidget.indexOf(self)
        tabwidget.setTabText(index, text)
        self.actionMenuTab.setText(text)
    
    def updateTab(self):
        '''
        Updates tab info
        '''
        if self.path:
            name = os.path.basename(self.path)
            self.setTitle(name)
            self.setToolTip(self.path)
            self.actionMenuTab.setText(name)
        else:
            self.setTitle(_("Unsaved File"))
            self.setToolTip(_("Unsaved File"))
            
    def requestClose(self):
        if self.document().isModified():
            while True:
                resp = QMessageBox.question(self, _("File modified"), 
                                            _("%s is modified. Save changes before closing?", self.filename), 
                                            QMessageBox.Yes | QMessageBox.No)
                
                if resp == QMessageBox.Yes:
                    if not self.save():
                        continue
                    
                return resp
        else:
            return True
    
    def afterRemoveEvent(self):
        self.mainwindow.actionGroupTabs.removeAction(self.actionMenuTab)
        
    def afterInsertionEvent(self):
        self.updateTab()
        self.mainwindow.actionGroupTabs.addAction(self.actionMenuTab)
    
    def afterModificationEvent(self):
        pass
        
    def showTab(self, checked):
        if checked:
            tw = self.parent().parent()
            index = tw.indexOf(self)
            if index != tw.currentIndex():
                tw.setCurrentIndex(index)
    
    def lineNumberAreaWidth(self):
        # si tiene folding tengo que sumar mas 10
        return 3 + self.fontMetrics().width('9') * len(str(self.blockCount())) + 10
    
    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
    
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy);
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height());
        if (rect.contains(self.viewport().rect())):
            self.updateLineNumberAreaWidth(0)
 
    def resizeEvent(self, e):
        QPlainTextEdit.resizeEvent(self, e)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 
                                              self.lineNumberAreaWidth(), cr.height()));

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            #e8f2fe
            color = QColor(232, 242, 25)
            lineColor = QColor(color).lighter(180)
            selection.format.setBackground(lineColor);
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
    
    def lineNumberAreaPaintEvent(self, event):
        
        painter = QPainter(self.lineNumberArea)
        
        painter.fillRect(event.rect(), Qt.white)
        block = self.firstVisibleBlock()
        
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top < event.rect().bottom():
            user_data = block.userData()
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.lightGray)
                painter.drawText(-7, top, self.lineNumberArea.width(), self.fontMetrics().height(), Qt.AlignRight, number)
                #Rudimentos de folding
                if user_data and user_data.folding == user_data.FOLDING_START:
                    painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(), Qt.AlignRight, '-')
                    
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    MAX_POINT_SIZE = 24
    MIN_POINT_SIZE = 6
    
    def zoomIn(self):
        font = self.font()
        pt_size = font.pointSize()
        if pt_size < self.MAX_POINT_SIZE:
            pt_size += 1
            font.setPointSize(pt_size)
            print pt_size
        self.setFont(font)
    
    def zoomOut(self):
        font = self.font()
        pt_size = font.pointSize()
        if pt_size > self.MIN_POINT_SIZE:
            pt_size -=  1
            font.setPointSize(pt_size)
            print pt_size
        self.setFont(font)

class EditorTabAction(QAction):
    def __init__(self, title, parent):
        QAction.__init__(self, title, parent)
        self.setCheckable(True)
        self.connect(self, SIGNAL('toggled(bool)'), self.parent().showTab )
    
    def focus(self, checked):
        if checked:
            editor = self.parent()
            tabs = self.parent().parent()
            print editor, tabs
        

