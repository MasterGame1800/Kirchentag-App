# main_frame_class.py
# This file contains the MainFrame class, moved from main_frame.py for modularity.

from PyQt6 import QtCore, QtGui, QtWidgets
from backend import CheckInOutManager, Individual
import datetime
import os
from main_frame import Ui_MainWindow  # Import the UI class

class MainFrame(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.manager = CheckInOutManager()
        # --- Choose DB backend: local or network ---
        network_mode = os.environ.get('NETWORK_DB', '0') == '1'
        if network_mode:
            from db import NetworkDB
            self.db = NetworkDB()
        else:
            import db
            self.db = db
        # --- Use self.db instead of db below ---
        self.ui.addEntryButton.clicked.connect(self.add_entry)
        self.ui.loadFileButton.clicked.connect(self.load_file)
        self.ui.searchLineEdit.textChanged.connect(self.search_guest_table)
        self.ui.tableSelection.currentIndexChanged.connect(self.update_table_selection)
        self.ui.reloadButton.clicked.connect(self.reload_from_db)  # Connect reload button
        self.selected_table = self.ui.guest_table  # Default to guest table
        # Load data from database
        self.guest_individuals = self.db.load_individuals('guest')
        self.team_individuals = self.db.load_individuals('team')
        # Set up both tables
        self.setup_table(self.ui.team_table)
        self.setup_table(self.ui.guest_table)
        self.populate_table(self.ui.guest_table, self.guest_individuals)
        self.populate_table(self.ui.team_table, self.team_individuals)
        self.update_counters()
        self.load_log_to_widget()

        # --- Real-time polling for all modes ---
        self.poll_timer = QtCore.QTimer(self)
        self.poll_timer.setInterval(450)  # 2 seconds
        self.poll_timer.timeout.connect(self.reload_from_db)
        self.poll_timer.start()

    def load_log_to_widget(self):
        log_screen = self.ui.logScreen
        scrollbar = log_screen.verticalScrollBar()
        at_bottom = scrollbar.value() == scrollbar.maximum()
        log_screen.clear()
        for ts, fullname, reisegruppe, status in self.db.load_log():
            log_screen.append(f"[{ts}] {fullname} ({reisegruppe}) {status}")
        if at_bottom:
            scrollbar.setValue(scrollbar.maximum())
        # else: keep current position

    def append_log_entry(self, entry):
        log_screen = self.ui.logScreen
        scrollbar = log_screen.verticalScrollBar()
        at_bottom = scrollbar.value() == scrollbar.maximum()
        log_screen.append(entry)
        if at_bottom:
            scrollbar.setValue(scrollbar.maximum())
        # else: keep current position

    def save_all(self):
        self.db.save_individuals('guest', self.guest_individuals)
        self.db.save_individuals('team', self.team_individuals)

    def update_table_selection(self):
        if self.ui.tableSelection.currentText() == "Gäste":
            self.selected_table = self.ui.guest_table
        else:
            self.selected_table = self.ui.team_table

    def setup_table(self, table):
        headers = ["Name", "Vorname", "Reisegruppe", "Alter", "Geschlecht", "Anwesend", "Evakuiert", "Notiz"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.setSortingEnabled(True)
        table.sortItems(2, QtCore.Qt.SortOrder.AscendingOrder)

    def load_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.selected_table.setSortingEnabled(False)
            new_individuals = []
            import csv
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
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
        table.setRowCount(len(individuals))
        for row_idx, individual in enumerate(individuals):
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
            present_btn = QtWidgets.QPushButton("Yes" if individual.anwesend else "No")
            present_btn.setCheckable(True)
            present_btn.setChecked(individual.anwesend)
            # Ensure button text matches checked state
            present_btn.setText("Yes" if individual.anwesend else "No")
            def present_handler(checked, btn=present_btn, idx=row_idx, table_ref=table):
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if table_ref == self.ui.guest_table:
                    person = self.guest_individuals[idx]
                    table_type = "Gäste"
                else:
                    person = self.team_individuals[idx]
                    table_type = "Team"
                # Always update the individual's state to match the button
                person.anwesend = checked
                status = "arrived" if checked else "left"
                log_entry = f"[{now}] [{table_type}] {person.vorname} {person.name} ({person.reisegruppe})  {status}"
                self.append_log_entry(log_entry)
                self.db.add_log_entry(f"{table_type} {status}", f"{person.vorname} {person.name}", person.reisegruppe)
                btn.setText("Yes" if checked else "No")
                self.save_all()
                if checked and not table.cellWidget(idx, 6):
                    evacuated_btn = QtWidgets.QPushButton("Yes" if person.evakuiert else "No")
                    evacuated_btn.setCheckable(True)
                    evacuated_btn.setChecked(person.evakuiert)
                    evacuated_btn.setText("Yes" if person.evakuiert else "No")
                    def evacuated_handler(checked, btn=evacuated_btn, idx=idx, table_ref=table):
                        if table_ref == self.ui.guest_table:
                            self.guest_individuals[idx].evakuiert = checked
                        else:
                            self.team_individuals[idx].evakuiert = checked
                        btn.setText("Yes" if checked else "No")
                        self.update_counters()
                        self.save_all()
                    evacuated_btn.toggled.connect(evacuated_handler)
                    table.setCellWidget(idx, 6, evacuated_btn)
                elif not checked and table.cellWidget(idx, 6):
                    if table_ref == self.ui.guest_table:
                        self.guest_individuals[idx].evakuiert = False
                    else:
                        self.team_individuals[idx].evakuiert = False
                    table.removeCellWidget(idx, 6)
                self.update_counters()
            present_btn.toggled.connect(present_handler)
            table.setCellWidget(row_idx, 5, present_btn)
            # Set up evacuated button if present and anwesend is True
            if individual.anwesend:
                evacuated_btn = QtWidgets.QPushButton("Yes" if individual.evakuiert else "No")
                evacuated_btn.setCheckable(True)
                evacuated_btn.setChecked(individual.evakuiert)
                evacuated_btn.setText("Yes" if individual.evakuiert else "No")
                def evacuated_handler(checked, btn=evacuated_btn, idx=row_idx, table_ref=table):
                    if table_ref == self.ui.guest_table:
                        self.guest_individuals[idx].evakuiert = checked
                    else:
                        self.team_individuals[idx].evakuiert = checked
                    btn.setText("Yes" if checked else "No")
                    self.update_counters()
                    self.save_all()
                evacuated_btn.toggled.connect(evacuated_handler)
                table.setCellWidget(row_idx, 6, evacuated_btn)
            notiz_item = QtWidgets.QTableWidgetItem(individual.notiz)
            notiz_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
            table.setItem(row_idx, 7, notiz_item)
        table.setWordWrap(True)
        table.resizeRowsToContents()

    def update_counters(self):
        present_count = sum(1 for ind in self.guest_individuals if ind.anwesend) + sum(1 for ind in self.team_individuals if ind.anwesend)
        evacuated_count = sum(1 for ind in self.guest_individuals if ind.evakuiert) + sum(1 for ind in self.team_individuals if ind.evakuiert)
        self.ui.presentCountLabel.setText(f"Anwesend: {present_count}")
        self.ui.evacuatedCountLabel.setText(f"Evakuiert: {evacuated_count}")

    def search_guest_table(self, text):
        for row in range(self.ui.guest_table.rowCount()):
            match = False
            for col in range(self.ui.guest_table.columnCount()):
                item = self.ui.guest_table.item(row, col)
                if item and text.lower() in item.text().lower():
                    match = True
                    break
            self.ui.guest_table.setRowHidden(row, not match)

    def reload_from_db(self):
        self.guest_individuals = self.db.load_individuals('guest')
        self.team_individuals = self.db.load_individuals('team')
        self.populate_table(self.ui.guest_table, self.guest_individuals)
        self.populate_table(self.ui.team_table, self.team_individuals)
        self.update_counters()
        self.load_log_to_widget()
