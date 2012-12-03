#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseEditorKeyHelper

class CodeEditorKeyHelper(PMXBaseEditorKeyHelper):
    def accept(self, event, cursor, scope):
        return PMXBaseEditorKeyHelper.accept(self, event)
    
    def execute(self, event, cursor, scope):
        PMXBaseEditorKeyHelper.accept(self, event)

class KeyEquivalentHelper(CodeEditorKeyHelper):
    def accept(self, event, cursor = None, scope = None):
        keyseq = int(event.modifiers()) + event.key()
        if keyseq not in self.application.supportManager.getAllKeyEquivalentCodes():
            return False
        self.items = self.application.supportManager.getKeyEquivalentItem(keyseq, scope)
        return bool(self.items)

    def execute(self, event, cursor = None, scope = None):
        if len(self.items) == 1:
            self.editor.insertBundleItem(self.items[0])
        else:
            self.editor.selectBundleItem(self.items)

class TabTriggerHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Tab
    def accept(self, event, cursor = None, scope = None):
        if cursor.hasSelection(): return False

        trigger = self.application.supportManager.getTabTriggerSymbol(cursor.block().text(), cursor.columnNumber())
        self.items = self.application.supportManager.getTabTriggerItem(trigger, scope) if trigger is not None else []
        return bool(self.items)

    def execute(self, event, cursor = None, scope = None):
        #Inserto los items
        if len(self.items) == 1:
            self.editor.insertBundleItem(self.items[0], tabTriggered = True)
        else:
            self.editor.selectBundleItem(self.items, tabTriggered = True)

class CompleterHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Space
    def accept(self, event, cursor = None, scope = None):
        """Accept the completer event"""
        return event.modifiers() == QtCore.Qt.ControlModifier

    def execute(self, event, cursor = None, scope = None):
        self.editor.runCompleter()

class SmartTypingPairsHelper(CodeEditorKeyHelper):
    #TODO: Mas amor para la inteligencia de los cursores balanceados
    def accept(self, event, cursor = None, scope = None):
        settings = self.editor.preferenceSettings(scope)
        character = event.text()
        pairs = filter(lambda pair: character in pair, settings.smartTypingPairs)
        
        #Si no tengo nada retorno
        if not pairs: return False
        self.pair = pairs[0]
        
        self.skip = False
        self.cursor1 = self.cursor2 = None
        
        isOpen = character == self.pair[0]
        if isOpen and cursor.hasSelection():
            #El cursor tiene seleccion, veamos si es un brace de apertura y tiene seleccionado un brace de apertura 
            selectedText = cursor.selectedText()
            if any(map(lambda pair: selectedText == pair[0], settings.smartTypingPairs)):
                self.cursor1, self.cursor2 = self.editor.currentBracesPairs(cursor)
            return True
        
        isClose = character == self.pair[1]
        if isClose:
            #Es un caracter de cierre, veamos si tengo que saltarme algo hacia la derecha
            cursor1, cursor2 = self.editor.currentBracesPairs(cursor, direction = "right")
            self.skip = cursor1 is not None and cursor2 is not None and character == cursor2.selectedText()
            if self.skip or self.pair[0] != self.pair[1]:
                return self.skip

        meta_down = bool(event.modifiers() & QtCore.Qt.MetaModifier)
        if isOpen and meta_down:
            self.cursor1, self.cursor2 = self.editor.currentBracesPairs(cursor)
            if self.cursor1 is not None and self.cursor2 is not None:
                if cursor.position() == self.cursor1.selectionStart():
                    self.cursor1.setPosition(self.cursor1.selectionStart())
                    self.cursor2.setPosition(self.cursor2.selectionEnd())
                else:
                    self.cursor1.setPosition(self.cursor1.selectionEnd())
                    self.cursor2.setPosition(self.cursor2.selectionStart())
        word, wordStart, wordEnd = self.editor.currentWord(search = False)
        return not (wordStart <= cursor.position() < wordEnd)
        
    def execute(self, event, cursor = None, scope = None):
        cursor.beginEditBlock()
        if self.skip:
            cursor.movePosition(QtGui.QTextCursor.NextCharacter)
            self.editor.setTextCursor(cursor)
        elif cursor.hasSelection():
            if self.cursor2 is not None and self.cursor1 is not None:
                self.cursor1.insertText(self.pair[0])
                self.cursor2.insertText(self.pair[1])
            else:
                position = cursor.position()
                cursorBegin = cursor.selectionStart() == position
                text = self.pair[0] + cursor.selectedText() + self.pair[1]
                cursor.insertText(text)
                if cursorBegin:
                    cursor.setPosition(position + len(text))
                    cursor.setPosition(position, QtGui.QTextCursor.KeepAnchor)
                else:
                    cursor.setPosition(position - len(text) + 2)
                    cursor.setPosition(position + 2, QtGui.QTextCursor.KeepAnchor)
                self.editor.setTextCursor(cursor)
        elif self.cursor1 is not None and self.cursor2 is not None:
            self.cursor1.insertText(self.pair[0])
            self.cursor2.insertText(self.pair[1])
        else:
            position = cursor.position()
            cursor.insertText("%s%s" % (self.pair[0], self.pair[1]))
            cursor.setPosition(position + 1)
            self.editor.setTextCursor(cursor)
        cursor.endEditBlock()

class MoveCursorToHomeHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Home
    def accept(self, event, cursor = None, scope = None):
        #Solo si el cursor no esta al final de la indentacion
        block = cursor.block()
        self.newPosition = block.position() + len(block.userData().indent)
        return self.newPosition != cursor.position()
        
    def execute(self, event, cursor = None, scope = None):
        #Lo muevo al final de la indentacion
        cursor = self.editor.textCursor()
        cursor.setPosition(self.newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
        self.editor.setTextCursor(cursor)

class OverwriteHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Insert
    def execute(self, event, cursor = None, scope = None):
        self.editor.setOverwriteMode(not self.editor.overwriteMode())
        self.editor.modeChanged.emit()
        
class TabIndentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Tab
    def accept(self, event, cursor = None, scope = None):
        #Solo si el cursor tiene seleccion o usa soft Tab
        return cursor.hasSelection() or self.editor.tabStopSoft
        
    def execute(self, event, cursor = None, scope = None):
        start, end = self.editor.getSelectionBlockStartEnd()
        if start != end:
            #Tiene seleccion en distintos bloques, es un indentar
            self.editor.indentBlocks()
        else:
            #Insertar un numero multiplo de espacios a la posicion del cursor
            spaces = self.editor.tabStopSize - (cursor.columnNumber() % self.editor.tabStopSize)
            cursor.insertText(spaces * ' ')

class BacktabUnindentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Backtab
    #Siempre se come esta pulsacion solo que no unindenta si la linea ya esta al borde
    def execute(self, event, cursor = None, scope = None):
        self.editor.unindentBlocks()

class BackspaceUnindentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Backspace
    def accept(self, event, cursor = None, scope = None):
        if cursor.hasSelection(): return False
        lineText = cursor.block().text()
        return lineText[:cursor.columnNumber()].endswith(self.editor.tabKeyBehavior())
        
    def execute(self, event, cursor = None, scope = None):
        counter = cursor.columnNumber() % self.editor.tabStopSize or self.editor.tabStopSize
        for _ in range(counter):
            cursor.deletePreviousChar()

class BackspaceRemoveBracesHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Backspace
    def accept(self, event, cursor = None, scope = None):
        if cursor.hasSelection(): return False
        self.cursor1, self.cursor2 = self.editor.currentBracesPairs(cursor, direction = "left")
        return self.cursor1 is not None and self.cursor2 is not None and (self.cursor1.selectionStart() == self.cursor2.selectionEnd() or self.cursor1.selectionEnd() == self.cursor2.selectionStart())
        
    def execute(self, event, cursor = None, scope = None):
        cursor.beginEditBlock()
        self.cursor1.removeSelectedText()
        self.cursor2.removeSelectedText()
        cursor.endEditBlock()
        
class DeleteUnindentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Delete
    def accept(self, event, cursor = None, scope = None):
        if cursor.hasSelection(): return False
        lineText = cursor.block().text()
        return lineText[cursor.columnNumber():].startswith(self.editor.tabKeyBehavior())
        
    def execute(self, event, cursor = None, scope = None):
        counter = cursor.columnNumber() % self.editor.tabStopSize or self.editor.tabStopSize
        for _ in range(counter):
            cursor.deleteChar()

class DeleteRemoveBracesHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Delete
    def accept(self, event, cursor = None, scope = None):
        if cursor.hasSelection(): return False
        self.cursor1, self.cursor2 = self.editor.currentBracesPairs(cursor, direction = "right")
        return self.cursor1 is not None and self.cursor2 is not None and (self.cursor1.selectionStart() == self.cursor2.selectionEnd() or self.cursor1.selectionEnd() == self.cursor2.selectionStart())
        
    def execute(self, event, cursor = None, scope = None):
        cursor.beginEditBlock()
        self.cursor1.removeSelectedText()
        self.cursor2.removeSelectedText()
        cursor.endEditBlock()
        
class SmartIndentHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_Return
    def execute(self, event, cursor = None, scope = None):
        if self.editor.document().blockCount() == 1:
            syntax = self.application.supportManager.findSyntaxByFirstLine(cursor.block().text()[:cursor.columnNumber()])
            if syntax is not None:
                self.editor.setSyntax(syntax)
        self.editor.insertNewLine(cursor)

class MultiCursorHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_M
    def accept(self, event, cursor = None, scope = None):
        control_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        meta_down = bool(event.modifiers() & QtCore.Qt.MetaModifier)
        return event.key() == self.KEY and control_down and meta_down

    def execute(self, event, cursor = None, scope = None):
        cursor = cursor or self.editor.textCursor()
        flags = QtGui.QTextDocument.FindCaseSensitively | QtGui.QTextDocument.FindWholeWords
        if not cursor.hasSelection():
            text, start, end = self.editor.currentWord()
            newCursor = QtGui.QTextCursor(cursor)
            newCursor.setPosition(start)
            newCursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            self.editor.multiCursorMode.addMergeCursor(newCursor)
        else:
            text = cursor.selectedText()
            self.editor.multiCursorMode.addMergeCursor(cursor)
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                flags |= QtGui.QTextDocument.FindBackward
            newCursor = self.editor.document().find(text, cursor, flags)
            if not newCursor.isNull():
                self.editor.multiCursorMode.addMergeCursor(newCursor)
                self.editor.centerCursor(newCursor)

class PrintEditorStatusHelper(CodeEditorKeyHelper):
    KEY = QtCore.Qt.Key_P
    def accept(self, event, cursor = None, scope = None):
        control_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        meta_down = bool(event.modifiers() & QtCore.Qt.MetaModifier)
        return control_down and control_down
        
    def execute(self, event, cursor = None, scope = None):
        #Aca lo que queramos hacer
        userData = cursor.block().userData()
        print(self.editor.currentWord())
        print(self.editor.wordUnderCursor(), cursor.position())
        for group in [ "comment", "constant", "entity", "invalid", "keyword", "markup", "meta", "storage", "string", "support", "variable" ]:
            print("%s: %s" % (group, cursor.block().userData().wordsByGroup(group)))
        print("sin comentarios, sin cadenas", cursor.block().userData().wordsByGroup("-string -comment"))
