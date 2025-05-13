from PyQt6 import QtCore, QtGui, QtWidgets
from backend import CheckInOutManager, Individual

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.team_table = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.team_table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.team_table.setObjectName("team_table")
        self.team_table.setColumnCount(8)
        self.verticalLayout.addWidget(self.team_table)

        self.searchLineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.verticalLayout.addWidget(self.searchLineEdit)

        self.guest_table = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.guest_table.setObjectName("guest_table")
        self.guest_table.setColumnCount(8)
        self.verticalLayout.addWidget(self.guest_table)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.presentCountLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.presentCountLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.presentCountLabel.setObjectName("presentCountLabel")
        self.verticalLayout_2.addWidget(self.presentCountLabel)
        self.evacuatedCountLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.evacuatedCountLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.evacuatedCountLabel.setObjectName("evacuatedCountLabel")
        self.verticalLayout_2.addWidget(self.evacuatedCountLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadFileButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loadFileButton.setObjectName("loadFileButton")
        self.horizontalLayout.addWidget(self.loadFileButton)
        self.addEntryButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addEntryButton.setObjectName("addEntryButton")
        self.horizontalLayout.addWidget(self.addEntryButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.log_label = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_label.sizePolicy().hasHeightForWidth())
        self.log_label.setSizePolicy(sizePolicy)
        self.log_label.setObjectName("log_label")
        self.log_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_2.addWidget(self.log_label)
        self.textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        # Adjust the layout proportions
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.evacuatedCountLabel.setText(_translate("MainWindow", "TextLabel"))
        self.loadFileButton.setText(_translate("MainWindow", "Load File"))
        self.addEntryButton.setText(_translate("MainWindow", "Add Entry"))
        self.log_label.setText(_translate("MainWindow", "Log"))

class MainFrame(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize the backend manager
        self.manager = CheckInOutManager()

        # Connect buttons to their respective functions
        self.ui.addEntryButton.clicked.connect(self.add_entry)
        self.ui.loadFileButton.clicked.connect(self.load_file)

        # Initialize the table widgets
        self.setup_table(self.ui.team_table)
        self.setup_table(self.ui.guest_table)

        # Update counters
        self.update_counters()

    def setup_table(self, table):
        """
        Configure the table widget with appropriate headers.
        """
        headers = ["Name", "Vorname", "Reisegruppe", "Alter", "Geschlecht", "Anwesend", "Evakuiert", "Notiz"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

    def load_file(self):
        """
        Load data from a CSV file and populate the table.
        """
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.manager.load_data(file_path)
            self.populate_table(self.ui.guest_table, self.manager.individuals)
            self.update_counters()

    def add_entry(self):
        """
        Add a new entry to the table.
        """
        new_individual = Individual("New", "Entry", "Group", 0, "Unknown")
        self.manager.individuals.append(new_individual)
        self.populate_table(self.ui.guest_table, self.manager.individuals)
        self.update_counters()

    def populate_table(self, table, individuals):
        """
        Populate the table with individual data.
        """
        table.setRowCount(len(individuals))
        for row_idx, individual in enumerate(individuals):
            table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(individual.name))
            table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(individual.vorname))
            table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(individual.reisegruppe))
            table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(individual.alter)))
            table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(individual.geschlecht))
            table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem("Yes" if individual.anwesend else "No"))
            table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem("Yes" if individual.evakuiert else "No"))
            table.setItem(row_idx, 7, QtWidgets.QTableWidgetItem(individual.notiz))

    def update_counters(self):
        """
        Update the counters for present and evacuated individuals.
        """
        present_count = self.manager.get_present_count()
        evacuated_count = self.manager.get_evacuated_count()
        self.ui.presentCountLabel.setText(f"Anwesend: {present_count}")
        self.ui.evacuatedCountLabel.setText(f"Evakuiert: {evacuated_count}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec())