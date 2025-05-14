# main_frame.py
# This file defines the main window and UI logic for the CheckIn/Out System application using PyQt6.
# It includes the UI setup, table configuration, data loading, entry addition, and counter updates.

from PyQt6 import QtCore, QtGui, QtWidgets
from backend import CheckInOutManager, Individual

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
        
        self.verticalLayoutLeft = QtWidgets.QVBoxLayout()
        self.verticalLayoutLeft.setObjectName("verticalLayoutLeft")
        self.team_table = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.team_table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.team_table.setObjectName("team_table")
        self.team_table.setColumnCount(8)
        self.verticalLayoutLeft.addWidget(self.team_table)

        self.spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayoutLeft.addItem(self.spacerItem)
        self.searchLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.searchLineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.searchLineEdit.setPlaceholderText("Suchen")
        self.verticalLayoutLeft.addWidget(self.searchLineEdit)
        self.spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayoutLeft.addItem(self.spacerItem1)
        
        self.guest_table = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.guest_table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.guest_table.setObjectName("guest_table")
        self.guest_table.setColumnCount(8)
        self.verticalLayoutLeft.addWidget(self.guest_table)
        
        self.gridLayout.addLayout(self.verticalLayoutLeft, 0, 0, 1, 1)
        self.verticalLayoutRight = QtWidgets.QVBoxLayout()
        self.verticalLayoutRight.setObjectName("verticalLayoutRight")
        self.presentCountLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.presentCountLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.presentCountLabel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.presentCountLabel.setObjectName("presentCountLabel")
        self.verticalLayoutRight.addWidget(self.presentCountLabel)
        # Move the tableSelection ComboBox next to the loadFileButton
        self.tableSelection = QtWidgets.QComboBox(parent=self.centralwidget)
        self.tableSelection.setObjectName("tableSelection")
        self.tableSelection.addItem("Gäste")
        self.tableSelection.addItem("Team")
        self.evacuatedCountLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.evacuatedCountLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.evacuatedCountLabel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.evacuatedCountLabel.setObjectName("evacuatedCountLabel")
        self.verticalLayoutRight.addWidget(self.evacuatedCountLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadFileButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loadFileButton.setObjectName("loadFileButton")
        self.horizontalLayout.addWidget(self.loadFileButton)
        self.horizontalLayout.addWidget(self.tableSelection)
        self.addEntryButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addEntryButton.setObjectName("addEntryButton")
        self.horizontalLayout.addWidget(self.addEntryButton)
        self.verticalLayoutRight.addLayout(self.horizontalLayout)
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
        # Set the text for UI elements (for translation/localization)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CheckIn/Out System"))
        self.evacuatedCountLabel.setText(_translate("MainWindow", "TextLabel"))
        self.loadFileButton.setText(_translate("MainWindow", "Lade Datei"))
        self.addEntryButton.setText(_translate("MainWindow", "Neuer Eintrag"))
        self.log_label.setText(_translate("MainWindow", "Verlauf"))

class MainFrame(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize the backend manager for handling data
        self.manager = CheckInOutManager()

        # Connect UI buttons to their respective functions
        self.ui.addEntryButton.clicked.connect(self.add_entry)
        self.ui.loadFileButton.clicked.connect(self.load_file)
        # Connect search line edit to search function
        self.ui.searchLineEdit.textChanged.connect(self.search_guest_table)
        # Connect table selection change to update which table is loaded
        self.ui.tableSelection.currentIndexChanged.connect(self.update_table_selection)
        self.selected_table = self.ui.guest_table  # Default

        # Set up the team and guest tables
        self.setup_table(self.ui.team_table)
        self.setup_table(self.ui.guest_table)

        # Update the present and evacuated counters
        self.update_counters()

    def update_table_selection(self):
        """
        Update the selected_table reference based on ComboBox selection.
        Do not reload or repopulate the table here, only switch the reference.
        """
        if self.ui.tableSelection.currentText() == "Gäste":
            self.selected_table = self.ui.guest_table
        else:
            self.selected_table = self.ui.team_table
        # Do NOT call populate_table or load_file here!

    def setup_table(self, table):
        """
        Configure the table widget with appropriate headers and stretch them to fill the table width.
        Enable sorting and set default sort to the group column (Reisegruppe).
        """
        headers = ["Name", "Vorname", "Reisegruppe", "Alter", "Geschlecht", "Anwesend", "Evakuiert", "Notiz"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        # Make headers fill the complete table width
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        # Enable sorting
        table.setSortingEnabled(True)
        # Default sort by 'Reisegruppe' (index 2), ascending
        table.sortItems(2, QtCore.Qt.SortOrder.AscendingOrder)

        # Optionally: visually indicate the sorted column (arrow is shown by default in QTableWidget)
        # No extra code needed for arrow, as QTableWidget handles it automatically

    def load_file(self):
        """
        Load data from a CSV file and append the entries at the bottom of the selected table.
        Temporarily disable sorting to avoid issues when loading data.
        """
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            # Disable sorting before populating
            self.selected_table.setSortingEnabled(False)
            # Load new individuals from file (do not clear existing)
            previous_count = len(self.manager.individuals)
            new_individuals = self.manager.load_data(file_path, append=True) if 'append' in self.manager.load_data.__code__.co_varnames else None
            if new_individuals is None:
                # Fallback: if load_data does not support append, manually append
                import csv
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader, None)  # skip header
                    for row in reader:
                        if len(row) >= 5:
                            name, vorname, reisegruppe, alter, geschlecht = row[:5]
                            anwesend = row[5].strip().lower() == 'yes' if len(row) > 5 else False
                            evakuiert = row[6].strip().lower() == 'yes' if len(row) > 6 else False
                            notiz = row[7] if len(row) > 7 else ''
                            self.manager.individuals.append(Individual(name, vorname, reisegruppe, int(alter), geschlecht))
                            self.manager.individuals[-1].anwesend = anwesend
                            self.manager.individuals[-1].evakuiert = evakuiert
                            self.manager.individuals[-1].notiz = notiz
            # Repopulate only the selected table
            self.populate_table(self.selected_table, self.manager.individuals)
            self.update_counters()
            self.selected_table.setSortingEnabled(True)
            self.selected_table.sortItems(2, QtCore.Qt.SortOrder.AscendingOrder)

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
        Populate the table with individual data. The first 5 columns are set to read-only.
        The 6th and 7th columns (Anwesend, Evakuiert) are displayed as buttons.
        The 8th column (Notiz) wraps text so long notes remain visible.
        """
        table.setRowCount(len(individuals))
        for row_idx, individual in enumerate(individuals):
            # Create items for first 5 columns (read-only)
            items = [
                QtWidgets.QTableWidgetItem(individual.name),
                QtWidgets.QTableWidgetItem(individual.vorname),
                QtWidgets.QTableWidgetItem(individual.reisegruppe),
                QtWidgets.QTableWidgetItem(str(individual.alter)),
                QtWidgets.QTableWidgetItem(individual.geschlecht)
            ]
            for col in range(5):
                items[col].setFlags(items[col].flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                table.setItem(row_idx, col, items[col])

            # 6th column: Anwesend as button
            present_btn = QtWidgets.QPushButton("Yes" if individual.anwesend else "No")
            present_btn.setCheckable(True)
            present_btn.setChecked(individual.anwesend)
            def present_handler(checked, btn=present_btn, idx=row_idx):
                self.manager.individuals[idx].anwesend = checked
                btn.setText("Yes" if checked else "No")
                self.update_counters()
            present_btn.toggled.connect(present_handler)
            table.setCellWidget(row_idx, 5, present_btn)

            # 7th column: Evakuiert as button
            evacuated_btn = QtWidgets.QPushButton("Yes" if individual.evakuiert else "No")
            evacuated_btn.setCheckable(True)
            evacuated_btn.setChecked(individual.evakuiert)
            def evacuated_handler(checked, btn=evacuated_btn, idx=row_idx):
                self.manager.individuals[idx].evakuiert = checked
                btn.setText("Yes" if checked else "No")
                self.update_counters()
            evacuated_btn.toggled.connect(evacuated_handler)
            table.setCellWidget(row_idx, 6, evacuated_btn)

            # 8th column: Notiz (editable text, with word wrap)
            notiz_item = QtWidgets.QTableWidgetItem(individual.notiz)
            notiz_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
            table.setItem(row_idx, 7, notiz_item)
        # Enable word wrap for the Notiz column
        table.setWordWrap(True)
        table.resizeRowsToContents()

    def update_counters(self):
        """
        Update the counters for present and evacuated individuals.
        """
        present_count = self.manager.get_present_count()
        evacuated_count = self.manager.get_evacuated_count()
        self.ui.presentCountLabel.setText(f"Anwesend: {present_count}")
        self.ui.evacuatedCountLabel.setText(f"Evakuiert: {evacuated_count}")

    def search_guest_table(self, text):
        """
        Filter the guest_table rows based on the search text (case-insensitive, any column).
        """
        for row in range(self.ui.guest_table.rowCount()):
            match = False
            for col in range(self.ui.guest_table.columnCount()):
                item = self.ui.guest_table.item(row, col)
                if item and text.lower() in item.text().lower():
                    match = True
                    break
            self.ui.guest_table.setRowHidden(row, not match)

if __name__ == "__main__":
    # Entry point for the application
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec())