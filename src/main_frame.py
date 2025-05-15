# main_frame.py
# This file defines the main window and UI logic for the CheckIn/Out System application using PyQt6.
# It includes the UI setup, table configuration, data loading, entry addition, and counter updates.

from PyQt6 import QtCore, QtGui, QtWidgets
from backend import CheckInOutManager, Individual
import datetime
import os

# UI class for the main window, sets up all widgets and layout
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Set up the main window and its widgets
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1284, 844)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, -1, -1)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        
        # Left side: tables and search
        self.verticalLayoutLeft = QtWidgets.QVBoxLayout()
        self.verticalLayoutLeft.setObjectName("verticalLayoutLeft")
        # Team table (top, 1/3 height)
        self.team_table = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.team_table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.team_table.setObjectName("team_table")
        self.team_table.setColumnCount(8)
        self.verticalLayoutLeft.addWidget(self.team_table)

        # Spacer between tables and search
        self.spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayoutLeft.addItem(self.spacerItem)
        # Search bar
        self.searchLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.searchLineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.searchLineEdit.setPlaceholderText("Suchen")
        self.verticalLayoutLeft.addWidget(self.searchLineEdit)
        self.spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayoutLeft.addItem(self.spacerItem1)
        
        # Guest table (bottom, 2/3 height)
        self.guest_table = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.guest_table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.guest_table.setObjectName("guest_table")
        self.guest_table.setColumnCount(8)
        self.verticalLayoutLeft.addWidget(self.guest_table)
        
        self.gridLayout.addLayout(self.verticalLayoutLeft, 0, 0, 1, 1)
        # Right side: counters, controls, and log
        self.verticalLayoutRight = QtWidgets.QVBoxLayout()
        self.verticalLayoutRight.setObjectName("verticalLayoutRight")
        # Present counter label
        self.presentCountLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.presentCountLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.presentCountLabel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.presentCountLabel.setObjectName("presentCountLabel")
        self.verticalLayoutRight.addWidget(self.presentCountLabel)
        # Table selection ComboBox (for file loading)
        self.tableSelection = QtWidgets.QComboBox(parent=self.centralwidget)
        self.tableSelection.setObjectName("tableSelection")
        self.tableSelection.addItem("Gäste")
        self.tableSelection.addItem("Team")
        # Evacuated counter label
        self.evacuatedCountLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.evacuatedCountLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.evacuatedCountLabel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.evacuatedCountLabel.setObjectName("evacuatedCountLabel")
        self.verticalLayoutRight.addWidget(self.evacuatedCountLabel)
        # Horizontal layout for file and entry buttons
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadFileButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loadFileButton.setObjectName("loadFileButton")
        self.horizontalLayout.addWidget(self.tableSelection)
        self.horizontalLayout.addWidget(self.loadFileButton)
        self.addEntryButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addEntryButton.setObjectName("addEntryButton")
        self.horizontalLayout.addWidget(self.addEntryButton)
        self.verticalLayoutRight.addLayout(self.horizontalLayout)
        # Add a Reload button to the right panel
        self.reloadButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.reloadButton.setObjectName("reloadButton")
        self.reloadButton.setText("Reload")
        self.verticalLayoutRight.addWidget(self.reloadButton)
        # Log label
        self.log_label = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_label.sizePolicy().hasHeightForWidth())
        self.log_label.setSizePolicy(sizePolicy)
        self.log_label.setObjectName("log_label")
        self.log_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.log_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayoutRight.addWidget(self.log_label)
        # Log screen (QTextEdit)
        self.logScreen = QtWidgets.QTextEdit(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logScreen.sizePolicy().hasHeightForWidth())
        self.logScreen.setSizePolicy(sizePolicy)
        self.logScreen.setObjectName("logScreen")
        self.logScreen.setReadOnly(True)
        self.logScreen.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayoutRight.addWidget(self.logScreen)
        self.gridLayout.addLayout(self.verticalLayoutRight, 0, 1, 1, 1)

        # Adjust the layout proportions: left 2/3, right 1/3
        self.gridLayout.setColumnStretch(0, 2)  # Left side (tables) gets 2/3
        self.gridLayout.setColumnStretch(1, 1)  # Right side gets 1/3

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1284, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.evacuatedCountLabel.setStyleSheet("color: red; font-weight: bold; font-size: 60px;")
        self.presentCountLabel.setStyleSheet("color: green; font-weight: bold; font-size: 60px;")
        self.log_label.setStyleSheet("font-weight: bold; font-size: 20px;")
        self.logScreen.setStyleSheet("font-size: 12px;")
        self.tableSelection.setStyleSheet("font-size: 12px;")
        self.searchLineEdit.setStyleSheet("font-size: 12px;")
        self.loadFileButton.setStyleSheet("font-size: 12px;")
        self.addEntryButton.setStyleSheet("font-size: 12px;")
        self.reloadButton.setStyleSheet("font-size: 12px;")
        self.team_table.setStyleSheet("font-size: 12px;")
        self.guest_table.setStyleSheet("font-size: 12px;")

 
    def retranslateUi(self, MainWindow):
        # Set the text for UI elements (for translation/localization)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CheckIn/Out System"))
        self.evacuatedCountLabel.setText(_translate("MainWindow", "TextLabel"))
        self.loadFileButton.setText(_translate("MainWindow", "Lade Datei"))
        self.addEntryButton.setText(_translate("MainWindow", "Neuer Eintrag"))
        self.log_label.setText(_translate("MainWindow", "Verlauf"))
