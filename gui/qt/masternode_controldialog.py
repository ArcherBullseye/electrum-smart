from base64 import b64encode
from datetime import datetime
import os
import traceback

from PyQt5.QtGui import *
from PyQt5.QtCore import *

from electrum_smart import bitcoin
from electrum_smart.i18n import _
from electrum_smart.masternode import MasternodeAnnounce
from electrum_smart.masternode_manager import parse_masternode_conf
from electrum_smart.util import PrintError, bfh

from .masternode_widgets import *
from . import util

class MasternodeControlDialog(QDialog, PrintError):

    def __init__(self, manager, parent):
        super(MasternodeControlDialog, self).__init__(parent)
        self.gui = parent
        self.manager = manager
        self.setWindowTitle(_('Smartnode Manager'))

        self.waiting_dialog = None
        self.setupUi()

    def setupUi(self):
        self.setObjectName("SmartnodeControlDialog")
        self.resize(900, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.ipField = QLineEdit(self)
        self.ipField.setAlignment(Qt.AlignCenter)
        self.ipField.setObjectName("ipField")
        self.gridLayout.addWidget(self.ipField, 1, 1, 1, 1)
        self.aliasField = QLineEdit(self)
        self.aliasField.setAlignment(Qt.AlignCenter)
        self.aliasField.setObjectName("aliasField")
        self.gridLayout.addWidget(self.aliasField, 0, 1, 1, 1)
        self.label_3 = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_2 = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.collateralView = QStackedWidget(self)
        self.collateralView.setObjectName("collateralView")
        self.stackedWidgetPage1 = QWidget()
        self.stackedWidgetPage1.setObjectName("stackedWidgetPage1")
        self.verticalLayout_3 = QVBoxLayout(self.stackedWidgetPage1)
        self.verticalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QLabel(self.stackedWidgetPage1)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.collateralTable = QTableWidget(self.stackedWidgetPage1)
        font = QFont()
        font.setPointSize(12)
        self.collateralTable.setFont(font)
        self.collateralTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.collateralTable.setObjectName("collateralTable")
        self.collateralTable.setColumnCount(4)
        self.collateralTable.setRowCount(0)
        item = QTableWidgetItem()
        self.collateralTable.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.collateralTable.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.collateralTable.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.collateralTable.setHorizontalHeaderItem(3, item)
        self.verticalLayout_3.addWidget(self.collateralTable)
        self.collateralView.addWidget(self.stackedWidgetPage1)
        self.page = QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_4 = QVBoxLayout(self.page)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.verticalLayout_4.addItem(spacerItem2)
        self.label_7 = QLabel(self.page)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.addressViewLabel = QLabel(self.page)
        self.addressViewLabel.setTextInteractionFlags(
            Qt.LinksAccessibleByMouse | Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
        self.addressViewLabel.setObjectName("addressViewLabel")
        self.gridLayout_2.addWidget(self.addressViewLabel, 0, 1, 1, 1)
        self.label_8 = QLabel(self.page)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)
        self.txIndexViewLabel = QLabel(self.page)
        self.txIndexViewLabel.setTextInteractionFlags(
            Qt.LinksAccessibleByMouse | Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
        self.txIndexViewLabel.setObjectName("txIndexViewLabel")
        self.gridLayout_2.addWidget(self.txIndexViewLabel, 2, 1, 1, 1)
        self.label_9 = QLabel(self.page)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)
        self.txHashViewLabel = QLabel(self.page)
        self.txHashViewLabel.setTextInteractionFlags(
            Qt.LinksAccessibleByMouse | Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
        self.txHashViewLabel.setObjectName("txHashViewLabel")
        self.gridLayout_2.addWidget(self.txHashViewLabel, 1, 1, 1, 1)
        self.label_10 = QLabel(self.page)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 2, 1, 1)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 2, 2, 1, 1)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 1, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        spacerItem6 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem6)
        self.collateralView.addWidget(self.page)
        self.verticalLayout.addWidget(self.collateralView)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.smartnodeKeyLabel = QLabel(self)
        font = QFont()
        font.setPointSize(14)
        self.smartnodeKeyLabel.setFont(font)
        self.smartnodeKeyLabel.setStyleSheet("color: rgb(120, 18, 25);")
        self.smartnodeKeyLabel.setTextInteractionFlags(
            Qt.LinksAccessibleByMouse | Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
        self.smartnodeKeyLabel.setObjectName("smartnodeKeyLabel")
        self.horizontalLayout.addWidget(self.smartnodeKeyLabel)
        spacerItem7 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.copySmartnodeKeyButton = QPushButton(self)
        self.copySmartnodeKeyButton.setObjectName("copySmartnodeKeyButton")
        self.horizontalLayout.addWidget(self.copySmartnodeKeyButton)
        self.customSmartnodeKeyButton = QPushButton(self)
        self.customSmartnodeKeyButton.setObjectName("customSmartnodeKeyButton")
        self.horizontalLayout.addWidget(self.customSmartnodeKeyButton)
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_6 = QLabel(self)
        font = QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem9 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem9)
        self.viewButtonBox = QDialogButtonBox(self)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewButtonBox.sizePolicy().hasHeightForWidth())
        self.viewButtonBox.setSizePolicy(sizePolicy)
        self.viewButtonBox.setOrientation(Qt.Horizontal)
        self.viewButtonBox.setStandardButtons(QDialogButtonBox.Close)
        self.viewButtonBox.setObjectName("viewButtonBox")
        self.verticalLayout.addWidget(self.viewButtonBox)
        self.defaultButtonBox = QDialogButtonBox(self)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.defaultButtonBox.sizePolicy().hasHeightForWidth())
        self.defaultButtonBox.setSizePolicy(sizePolicy)
        self.defaultButtonBox.setOrientation(Qt.Horizontal)
        self.defaultButtonBox.setStandardButtons(QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self.defaultButtonBox.setObjectName("defaultButtonBox")
        self.verticalLayout.addWidget(self.defaultButtonBox)

        self.retranslateUi(self)
        QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.aliasField, self.ipField)
        self.setTabOrder(self.ipField, self.collateralTable)
        self.setTabOrder(self.collateralTable, self.copySmartnodeKeyButton)

    def retranslateUi(self, SmartnodeControlDialog):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("SmartnodeControlDialog", "Create new Smartnode"))
        self.ipField.setPlaceholderText(_translate("SmartnodeControlDialog", "000.000.000.000"))
        self.aliasField.setPlaceholderText(_translate("SmartnodeControlDialog", "MyNode1"))
        self.label_3.setText(_translate("SmartnodeControlDialog", "IP-Address"))
        self.label_2.setText(_translate("SmartnodeControlDialog", "Alias"))
        self.label_4.setText(_translate("SmartnodeControlDialog", "Select a collateral for your new node"))
        self.collateralTable.setSortingEnabled(False)
        item = self.collateralTable.horizontalHeaderItem(0)
        item.setText(_translate("SmartnodeControlDialog", "Label"))
        item = self.collateralTable.horizontalHeaderItem(1)
        item.setText(_translate("SmartnodeControlDialog", "Address"))
        item = self.collateralTable.horizontalHeaderItem(2)
        item.setText(_translate("SmartnodeControlDialog", "TX-Hash"))
        item = self.collateralTable.horizontalHeaderItem(3)
        item.setText(_translate("SmartnodeControlDialog", "TX-Index"))
        self.label_7.setText(_translate("SmartnodeControlDialog", "Collateral"))
        self.addressViewLabel.setText(_translate("SmartnodeControlDialog", "0000000000000000000000000"))
        self.label_8.setText(_translate("SmartnodeControlDialog", "Address"))
        self.txIndexViewLabel.setText(_translate("SmartnodeControlDialog", "1"))
        self.label_9.setText(_translate("SmartnodeControlDialog", "Transaction hash"))
        self.txHashViewLabel.setText(
            _translate("SmartnodeControlDialog", "00000000000000000000000000000000000000000000"))
        self.label_10.setText(_translate("SmartnodeControlDialog", "Transaction output id"))
        self.label_5.setText(_translate("SmartnodeControlDialog", "Smartnode Key"))
        self.smartnodeKeyLabel.setText(
            _translate("SmartnodeControlDialog", "00000000000000000000000000000000000000000"))
        self.copySmartnodeKeyButton.setText(_translate("SmartnodeControlDialog", "Copy SmartnodeKey"))
        self.customSmartnodeKeyButton.setText(_translate("SmartnodeControlDialog", "Custom SmartnodeKey"))
        self.label_6.setText(_translate("SmartnodeControlDialog",
                                        "Its required to use the \"Smartnode Key\" above when you install your new node. You can manually insert it into your node\'s smartcash.conf or provide it to the bash installer when prompted."))

#if __name__ == "__main__":
    import sys
    #self.gui = parent
    #self.setWindowTitle(_('Smartnode'))
    #self.waiting_dialog = None
    #self.setupUi()
    #app = QApplication(sys.argv)
    #SmartnodeControlDialog = QDialog()
    #ui = Ui_SmartnodeControlDialog()
    #ui.setupUi(self)
    #self.show()
    #sys.exit(app.exec_())