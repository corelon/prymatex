# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dialogs/project.ui'
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

class Ui_NewProjectDialog(object):
    def setupUi(self, NewProjectDialog):
        NewProjectDialog.setObjectName(_fromUtf8("NewProjectDialog"))
        NewProjectDialog.setWindowModality(QtCore.Qt.WindowModal)
        NewProjectDialog.resize(464, 323)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/prymatex/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NewProjectDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(NewProjectDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label1 = QtGui.QLabel(NewProjectDialog)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label1)
        self.lineProjectName = QtGui.QLineEdit(NewProjectDialog)
        self.lineProjectName.setObjectName(_fromUtf8("lineProjectName"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineProjectName)
        self.label = QtGui.QLabel(NewProjectDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.textDescription = QtGui.QTextEdit(NewProjectDialog)
        self.textDescription.setObjectName(_fromUtf8("textDescription"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.textDescription)
        self.checkBoxUseDefaultLocation = QtGui.QCheckBox(NewProjectDialog)
        self.checkBoxUseDefaultLocation.setChecked(True)
        self.checkBoxUseDefaultLocation.setObjectName(_fromUtf8("checkBoxUseDefaultLocation"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBoxUseDefaultLocation)
        self.label2 = QtGui.QLabel(NewProjectDialog)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lineLocation = QtGui.QLineEdit(NewProjectDialog)
        self.lineLocation.setEnabled(False)
        self.lineLocation.setObjectName(_fromUtf8("lineLocation"))
        self.horizontalLayout_5.addWidget(self.lineLocation)
        self.buttonChoose = QtGui.QPushButton(NewProjectDialog)
        self.buttonChoose.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder"))
        self.buttonChoose.setIcon(icon)
        self.buttonChoose.setObjectName(_fromUtf8("buttonChoose"))
        self.horizontalLayout_5.addWidget(self.buttonChoose)
        self.formLayout_2.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.checkBoxUseTemplate = QtGui.QCheckBox(NewProjectDialog)
        self.checkBoxUseTemplate.setObjectName(_fromUtf8("checkBoxUseTemplate"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.checkBoxUseTemplate)
        self.label_2 = QtGui.QLabel(NewProjectDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboBoxTemplate = QtGui.QComboBox(NewProjectDialog)
        self.comboBoxTemplate.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxTemplate.sizePolicy().hasHeightForWidth())
        self.comboBoxTemplate.setSizePolicy(sizePolicy)
        self.comboBoxTemplate.setObjectName(_fromUtf8("comboBoxTemplate"))
        self.horizontalLayout_3.addWidget(self.comboBoxTemplate)
        self.buttonEnvironment = QtGui.QPushButton(NewProjectDialog)
        self.buttonEnvironment.setEnabled(False)
        self.buttonEnvironment.setMaximumSize(QtCore.QSize(32, 16777215))
        self.buttonEnvironment.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("code-variable"))
        self.buttonEnvironment.setIcon(icon)
        self.buttonEnvironment.setObjectName(_fromUtf8("buttonEnvironment"))
        self.horizontalLayout_3.addWidget(self.buttonEnvironment)
        self.formLayout_2.setLayout(6, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.line_2 = QtGui.QFrame(NewProjectDialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.SpanningRole, self.line_2)
        self.checkBoxAddToWorkingSet = QtGui.QCheckBox(NewProjectDialog)
        self.checkBoxAddToWorkingSet.setChecked(False)
        self.checkBoxAddToWorkingSet.setObjectName(_fromUtf8("checkBoxAddToWorkingSet"))
        self.formLayout_2.setWidget(8, QtGui.QFormLayout.FieldRole, self.checkBoxAddToWorkingSet)
        self.label3 = QtGui.QLabel(NewProjectDialog)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.formLayout_2.setWidget(9, QtGui.QFormLayout.LabelRole, self.label3)
        self.comboBoxWorkingSet = QtGui.QComboBox(NewProjectDialog)
        self.comboBoxWorkingSet.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxWorkingSet.sizePolicy().hasHeightForWidth())
        self.comboBoxWorkingSet.setSizePolicy(sizePolicy)
        self.comboBoxWorkingSet.setEditable(True)
        self.comboBoxWorkingSet.setObjectName(_fromUtf8("comboBoxWorkingSet"))
        self.formLayout_2.setWidget(9, QtGui.QFormLayout.FieldRole, self.comboBoxWorkingSet)
        self.line = QtGui.QFrame(NewProjectDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.SpanningRole, self.line)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonCreate = QtGui.QPushButton(NewProjectDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("project-development-new-template"))
        self.buttonCreate.setIcon(icon)
        self.buttonCreate.setObjectName(_fromUtf8("buttonCreate"))
        self.horizontalLayout.addWidget(self.buttonCreate)
        self.buttonCancel = QtGui.QPushButton(NewProjectDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("dialog-cancel"))
        self.buttonCancel.setIcon(icon)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NewProjectDialog)
        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), NewProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewProjectDialog)
        NewProjectDialog.setTabOrder(self.lineProjectName, self.lineLocation)
        NewProjectDialog.setTabOrder(self.lineLocation, self.buttonChoose)
        NewProjectDialog.setTabOrder(self.buttonChoose, self.buttonCreate)

    def retranslateUi(self, NewProjectDialog):
        NewProjectDialog.setWindowTitle(_('New Project'))
        self.label1.setText(_('Name:'))
        self.label.setText(_('Description:'))
        self.checkBoxUseDefaultLocation.setText(_('Use default location'))
        self.label2.setText(_('Location:'))
        self.buttonChoose.setText(_('Ch&oose'))
        self.checkBoxUseTemplate.setText(_('Use template'))
        self.label_2.setText(_('Template:'))
        self.checkBoxAddToWorkingSet.setText(_('Add to working set'))
        self.label3.setText(_('Working set:'))
        self.buttonCreate.setText(_('&Create'))
        self.buttonCancel.setText(_('C&ancel'))

