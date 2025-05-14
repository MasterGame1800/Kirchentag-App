# main_frame.py
# This file defines the main window and UI logic for the CheckIn/Out System application using PyQt6.
# It includes the UI setup, table configuration, data loading, entry addition, and counter updates.

from PyQt6 import QtCore, QtGui, QtWidgets
from backend import CheckInOutManager, Individual
import datetime
import db

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
        self.horizontalLayout.addWidget(self.loadFileButton)
        self.horizontalLayout.addWidget(self.tableSelection)
        self.addEntryButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addEntryButton.setObjectName("addEntryButton")
        self.horizontalLayout.addWidget(self.addEntryButton)
        self.verticalLayoutRight.addLayout(self.horizontalLayout)
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

    def retranslateUi(self, MainWindow):
        # Set the text for UI elements (for translation/localization)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CheckIn/Out System"))
        self.evacuatedCountLabel.setText(_translate("MainWindow", "TextLabel"))
        self.loadFileButton.setText(_translate("MainWindow", "Lade Datei"))
        self.addEntryButton.setText(_translate("MainWindow", "Neuer Eintrag"))
        self.log_label.setText(_translate("MainWindow", "Verlauf"))

# Main application window and logic
class MainFrame(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.manager = CheckInOutManager()  # Not used directly, but could be for future logic
        db.init_db()  # Ensure database is initialized
        # Connect UI signals to slots
        self.ui.addEntryButton.clicked.connect(self.add_entry)
        self.ui.loadFileButton.clicked.connect(self.load_file)
        self.ui.searchLineEdit.textChanged.connect(self.search_guest_table)
        self.ui.tableSelection.currentIndexChanged.connect(self.update_table_selection)
        self.selected_table = self.ui.guest_table  # Default to guest table
        # Load data from database
        self.guest_individuals = db.load_individuals('guest')
        self.team_individuals = db.load_individuals('team')
        # Set up both tables
        self.setup_table(self.ui.team_table)
        self.setup_table(self.ui.guest_table)
        self.populate_table(self.ui.guest_table, self.guest_individuals)
        self.populate_table(self.ui.team_table, self.team_individuals)
        self.update_counters()
        self.load_log_to_widget()

    def load_log_to_widget(self):
        """
        Load all log entries from the database and display them in the QTextEdit log screen.
        """
        self.ui.logScreen.clear()
        for ts, fullname, reisegruppe, status in db.load_log():
            self.ui.logScreen.append(f"[{ts}] {fullname} ({reisegruppe}) {status}")

    def save_all(self):
        """
        Save all individuals (guests and team) to the database.
        """
        db.save_individuals('guest', self.guest_individuals)
        db.save_individuals('team', self.team_individuals)

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
        # QTableWidget shows sort arrow automatically

    def load_file(self):
        """
        Load data from a CSV file and append the entries at the bottom of the selected table.
        Only append to the currently selected table's data.
        """
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.selected_table.setSortingEnabled(False)
            new_individuals = []
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
                        ind = Individual(name, vorname, reisegruppe, int(alter), geschlecht)
                        ind.anwesend = anwesend
                        ind.evakuiert = evakuiert
                        ind.notiz = notiz
                        new_individuals.append(ind)
            if self.selected_table == self.ui.guest_table:
                self.guest_individuals.extend(new_individuals)
                self.populate_table(self.ui.guest_table, self.guest_individuals)
            else:
                self.team_individuals.extend(new_individuals)
                self.populate_table(self.ui.team_table, self.team_individuals)
            self.update_counters()
            self.selected_table.setSortingEnabled(True)
            self.selected_table.sortItems(2, QtCore.Qt.SortOrder.AscendingOrder)
            self.save_all()

    def add_entry(self):
        """
        Add a new entry to the currently selected table only.
        """
        new_individual = Individual("New", "Entry", "Group", 0, "Unknown")
        if self.selected_table == self.ui.guest_table:
            self.guest_individuals.append(new_individual)
            self.populate_table(self.ui.guest_table, self.guest_individuals)
        else:
            self.team_individuals.append(new_individual)
            self.populate_table(self.ui.team_table, self.team_individuals)
        self.update_counters()
        self.save_all()

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

            # 6th column: Anwesend as button (toggle present/absent)
            present_btn = QtWidgets.QPushButton("Yes" if individual.anwesend else "No")
            present_btn.setCheckable(True)
            present_btn.setChecked(individual.anwesend)
            def present_handler(checked, btn=present_btn, idx=row_idx, table_ref=table):
                # Handler for toggling present status
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if table_ref == self.ui.guest_table:
                    person = self.guest_individuals[idx]
                    table_type = "Gäste"
                else:
                    person = self.team_individuals[idx]
                    table_type = "Team"
                status = "arrived" if checked else "left"
                log_entry = f"[{now}] [{table_type}] {person.vorname} {person.name} ({person.reisegruppe})  {status}"
                self.ui.logScreen.append(log_entry)  # Write to log widget
                db.add_log_entry(f"{table_type} {status}", f"{person.vorname} {person.name}", person.reisegruppe)  # Write to DB
                btn.setText("Yes" if checked else "No")
                self.save_all()
                # Dynamically create and add the evacuated button only when checked for the first time
                if checked and not table.cellWidget(idx, 6):
                    evacuated_btn = QtWidgets.QPushButton("No")
                    evacuated_btn.setCheckable(True)
                    evacuated_btn.setChecked(False)
                    def evacuated_handler(checked, btn=evacuated_btn, idx=idx, table_ref=table):
                        # Handler for toggling evacuated status
                        if table_ref == self.ui.guest_table:
                            self.guest_individuals[idx].evakuiert = checked
                        else:
                            self.team_individuals[idx].evakuiert = checked
                        btn.setText("Yes" if checked else "No")
                        self.update_counters()
                        self.save_all()
                    evacuated_btn.toggled.connect(evacuated_handler)
                    table.setCellWidget(idx, 6, evacuated_btn)
                # If unchecked, remove the evacuated button
                elif not checked and table.cellWidget(idx, 6):
                    if table_ref == self.ui.guest_table:
                        self.guest_individuals[idx].evakuiert = False
                    else:
                        self.team_individuals[idx].evakuiert = False
                    table.removeCellWidget(idx, 6)
                self.update_counters()
            present_btn.toggled.connect(present_handler)
            table.setCellWidget(row_idx, 5, present_btn)

            # 8th column: Notiz (editable text, with word wrap)
            notiz_item = QtWidgets.QTableWidgetItem(individual.notiz)
            notiz_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
            table.setItem(row_idx, 7, notiz_item)
        # Enable word wrap for the Notiz column
        table.setWordWrap(True)
        table.resizeRowsToContents()
        self.save_all()

    def update_counters(self):
        """
        Update the counters for present and evacuated individuals across both tables.
        """
        present_count = sum(1 for ind in self.guest_individuals if ind.anwesend) + sum(1 for ind in self.team_individuals if ind.anwesend)
        evacuated_count = sum(1 for ind in self.guest_individuals if ind.evakuiert) + sum(1 for ind in self.team_individuals if ind.evakuiert)
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