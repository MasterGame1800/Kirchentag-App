import wx
from backend import CheckInOutManager
from grids import create_grid
from counters import update_counters
from search_and_filter import on_search
from events import on_resize, on_load_csv
from utils.csv_loader import load_data  # Import the updated CSV loader
from backend import Individual  # Import the Individual class

class MainFrame(wx.Frame):
    def __init__(self):
        print("Initializing MainFrame...")
        super().__init__(parent=None, title='Check-In/Check-Out Tool')
        print("MainFrame initialized.")
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Add title and description
        title = wx.StaticText(self.panel, label='Check-In/Check-Out Management')
        title.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour(30, 144, 255))

        description = wx.StaticText(self.panel, label='Manage attendance and evacuation status efficiently.')
        description.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        description.SetForegroundColour(wx.Colour(105, 105, 105))

        # Add status bar
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText('Welcome to the Check-In/Check-Out Tool!')

        # Backend manager
        self.manager = CheckInOutManager()

        # Search bar
        self.search_bar = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.search_bar.Bind(wx.EVT_TEXT, on_search)

        # Add a dropdown to select the table for searching
        self.table_selection = wx.Choice(self.panel, choices=["Team Table", "Guest Table"])
        self.table_selection.SetSelection(0)  # Default to the first option

        # Adjust layout to place the search bar and table selection side by side
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(self.search_bar, 1, wx.EXPAND | wx.ALL, 5)
        search_sizer.Add(self.table_selection, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(search_sizer, 0, wx.EXPAND)

        # Create grids using the new helper method
        column_labels = ["Name", "Vorname", "Reisegruppe", "Alter", "Geschlecht", "Anwesend", "Evakuiert", "Notiz"]
        self.team_grid = create_grid(self.panel, len(column_labels), column_labels)
        self.grid = create_grid(self.panel, len(column_labels), column_labels)

        # Create a button to load data
        self.load_button = wx.Button(self.panel, label='Load File')
        self.load_button.SetBackgroundColour(wx.Colour(30, 144, 255))
        self.load_button.SetForegroundColour(wx.Colour(255, 255, 255))
        self.load_button.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.load_button.Bind(wx.EVT_BUTTON, self.on_load_csv)

        # Add widgets to the sizer
        self.sizer.Add(title, 0, wx.CENTER | wx.ALL, 10)
        self.sizer.Add(description, 0, wx.CENTER | wx.BOTTOM, 10)

        # Adjust the layout to stack the grids vertically with a 1/3 and 2/3 height ratio
        self.grid_sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid_sizer.Add(self.team_grid, 1, wx.EXPAND | wx.ALL, 10)
        self.grid_sizer.Add(self.grid, 2, wx.EXPAND | wx.ALL, 10)

        # Add the grid sizer to the main sizer
        self.sizer.Add(self.grid_sizer, 1, wx.EXPAND)

        # Add the load button
        self.sizer.Add(self.load_button, 0, wx.CENTER | wx.ALL, 5)

        # Ensure the layout is updated
        self.panel.SetSizerAndFit(self.sizer)
        self.SetSizeHints(800, 600)
        self.Bind(wx.EVT_SIZE, on_resize)

        self.row_to_individual = {}

        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.on_cell_value_changed)
        self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_column_header_click)
        self.team_grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_team_column_header_click)

        # Default sorting by group (Reisegruppe)
        self.current_sort_column = 2  # Index for "Reisegruppe"
        self.populate_grid(sorted(self.manager.individuals, key=lambda ind: ind.reisegruppe if ind.reisegruppe else ""))
        self.update_column_headers()

        self.ShowFullScreen(False)  # Lock the window in fullscreen mode
        self.Center()  # Ensure the window is centered
        self.SetSize(self.GetVirtualSize())  # Adjust the size to match the display

        print("Finalizing layout and showing MainFrame...")
        self.Layout()
        self.Show()
        print("MainFrame should now be visible.")

    def on_cell_value_changed(self, event):
        """Handle cell value changes to update notes."""
        row = event.GetRow()
        col = event.GetCol()

        if col == 7:  # "Notizen" column
            individual = self.row_to_individual.get(row)
            if individual:
                new_value = self.grid.GetCellValue(row, col)
                self.manager.update_note_by_id(individual.id, new_value)  # Update backend
                print(f"Updated note for {individual.name}: {new_value}")  # Debugging

    def on_column_header_click(self, event):
        """Handle column header click to sort the grid by the selected column or revert to group sorting."""
        col = event.GetCol()

        # If the same column is clicked again, unselect it and sort by group
        if hasattr(self, 'current_sort_column') and self.current_sort_column == col:
            self.current_sort_column = None
            sorted_individuals = sorted(self.manager.individuals, key=lambda ind: ind.reisegruppe if ind.reisegruppe else "")
        else:
            self.current_sort_column = col  # Track the current sort column

            if col == 0:  # Name
                sorted_individuals = sorted(self.manager.individuals, key=lambda ind: ind.name)
            elif col == 1:  # Vorname
                sorted_individuals = sorted(self.manager.individuals, key=lambda ind: ind.vorname)
            elif col == 2:  # Reisegruppe
                sorted_individuals = sorted(self.manager.individuals, key=lambda ind: ind.reisegruppe)
            elif col == 3:  # Alter
                sorted_individuals = sorted(self.manager.individuals, key=lambda ind: ind.alter)
            elif col == 4:  # Geschlecht
                sorted_individuals = sorted(self.manager.individuals, key=lambda ind: ind.geschlecht)
            elif col == 5:  # Anwesend
                sorted_individuals = sorted(self.manager.individuals, key=lambda ind: not ind.anwesend)
            elif col == 6:  # Evakuiert
                sorted_individuals = sorted(self.manager.individuals, key=lambda ind: not ind.evakuiert)
            elif col == 7:  # Notiz
                sorted_individuals = sorted(self.manager.individuals, key=lambda ind: ind.notiz)
            else:
                return  # Do nothing if an invalid column is clicked

        self.populate_grid(sorted_individuals)
        self.update_column_headers()

    def update_column_headers(self):
        """Update column headers to show sorting indicator."""
        headers = ["Name", "Vorname", "Reisegruppe", "Alter", "Geschlecht", "Anwesend", "Evakuiert", "Notiz"]
        for col_idx, header in enumerate(headers):
            if hasattr(self, 'current_sort_column') and self.current_sort_column == col_idx:
                self.grid.SetColLabelValue(col_idx, f"{header} ↓")  # Add arrow for sorted column
            else:
                self.grid.SetColLabelValue(col_idx, header)

    def populate_team_grid(self, individuals):
        """
        Populate the team grid with individual data and apply default sorting by group (Reisegruppe).
        :param individuals: List of Individual objects
        """
        # Apply default sorting by group
        individuals = sorted(individuals, key=lambda ind: ind.reisegruppe if ind.reisegruppe else "")

        self.team_grid.ClearGrid()
        if self.team_grid.GetNumberRows() > 0:
            self.team_grid.DeleteRows(0, self.team_grid.GetNumberRows())

        for row_idx, individual in enumerate(individuals):
            self.team_grid.AppendRows(1)
            self.team_grid.SetCellValue(row_idx, 0, individual.name)
            self.team_grid.SetCellValue(row_idx, 1, individual.vorname)
            self.team_grid.SetCellValue(row_idx, 2, individual.reisegruppe)
            self.team_grid.SetCellValue(row_idx, 3, str(individual.alter))
            self.team_grid.SetCellValue(row_idx, 4, individual.geschlecht)

        self.update_team_column_headers()

    def update_team_column_headers(self):
        """
        Update column headers of the team grid to show sorting indicator.
        """
        headers = ["Name", "Vorname", "Reisegruppe", "Alter", "Geschlecht"]
        for col_idx, header in enumerate(headers):
            if hasattr(self, 'current_team_sort_column') and self.current_team_sort_column == col_idx:
                self.team_grid.SetColLabelValue(col_idx, f"{header} ↓")  # Add arrow for sorted column
            else:
                self.team_grid.SetColLabelValue(col_idx, header)

    def on_team_column_header_click(self, event):
        """
        Handle column header click to sort the team grid by the selected column or revert to group sorting.
        """
        col = event.GetCol()

        # If the same column is clicked again, unselect it and sort by group
        if hasattr(self, 'current_team_sort_column') and self.current_team_sort_column == col:
            self.current_team_sort_column = None
            sorted_team_members = sorted(self.manager.individuals, key=lambda ind: ind.reisegruppe if ind.reisegruppe else "")
        else:
            self.current_team_sort_column = col  # Track the current sort column

            if col == 0:  # Name
                sorted_team_members = sorted(self.manager.individuals, key=lambda ind: ind.name)
            elif col == 1:  # Vorname
                sorted_team_members = sorted(self.manager.individuals, key=lambda ind: ind.vorname)
            elif col == 2:  # Reisegruppe
                sorted_team_members = sorted(self.manager.individuals, key=lambda ind: ind.reisegruppe)
            elif col == 3:  # Alter
                sorted_team_members = sorted(self.manager.individuals, key=lambda ind: ind.alter)
            elif col == 4:  # Geschlecht
                sorted_team_members = sorted(self.manager.individuals, key=lambda ind: ind.geschlecht)
            else:
                return  # Do nothing if an invalid column is clicked

        self.populate_team_grid(sorted_team_members)
        self.update_team_column_headers()

    def on_load_csv(self, event):
        """
        Provide a single menu to either add an entry manually or select a file to load data.
        """
        dialog = wx.Dialog(self, title="Add or Load Data", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create input fields for manual entry
        form_sizer = wx.FlexGridSizer(rows=6, cols=2, hgap=10, vgap=10)
        form_sizer.AddGrowableCol(1, 1)  # Make the input fields expand

        name_label = wx.StaticText(dialog, label="Name:")
        name_input = wx.TextCtrl(dialog)
        form_sizer.Add(name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        form_sizer.Add(name_input, 1, wx.EXPAND | wx.ALL, 5)

        vorname_label = wx.StaticText(dialog, label="Vorname:")
        vorname_input = wx.TextCtrl(dialog)
        form_sizer.Add(vorname_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        form_sizer.Add(vorname_input, 1, wx.EXPAND | wx.ALL, 5)

        reisegruppe_label = wx.StaticText(dialog, label="Reisegruppe:")
        reisegruppe_input = wx.TextCtrl(dialog)
        form_sizer.Add(reisegruppe_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        form_sizer.Add(reisegruppe_input, 1, wx.EXPAND | wx.ALL, 5)

        alter_label = wx.StaticText(dialog, label="Alter:")
        alter_input = wx.TextCtrl(dialog)
        form_sizer.Add(alter_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        form_sizer.Add(alter_input, 1, wx.EXPAND | wx.ALL, 5)

        geschlecht_label = wx.StaticText(dialog, label="Geschlecht:")
        geschlecht_dropdown = wx.Choice(dialog, choices=["Male", "Female", "Other"])
        form_sizer.Add(geschlecht_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        form_sizer.Add(geschlecht_dropdown, 1, wx.EXPAND | wx.ALL, 5)

        table_label = wx.StaticText(dialog, label="Select Table:")
        table_dropdown = wx.Choice(dialog, choices=["Team Table", "Guest Table"])
        form_sizer.Add(table_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        form_sizer.Add(table_dropdown, 1, wx.EXPAND | wx.ALL, 5)

        sizer.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 10)

        # Add file selection button
        file_button = wx.Button(dialog, label="Select File")
        sizer.Add(file_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Add OK and Cancel buttons
        button_sizer = wx.StdDialogButtonSizer()
        ok_button = wx.Button(dialog, wx.ID_OK, label="Add Entry")
        cancel_button = wx.Button(dialog, wx.ID_CANCEL)
        button_sizer.AddButton(ok_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()

        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        dialog.SetSizerAndFit(sizer)  # Ensure the dialog resizes dynamically
        dialog.SetMinSize((400, 300))  # Set a minimum size for the dialog

        def on_file_button_click(event):
            with wx.FileDialog(self, "Open File", wildcard="CSV and Excel files (*.csv;*.xls;*.xlsx)|*.csv;*.xls;*.xlsx",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
                if file_dialog.ShowModal() == wx.ID_CANCEL:
                    return  # User cancelled the dialog

                file_path = file_dialog.GetPath()
                data = load_data(file_path)  # Use the updated loader

                if data:
                    individuals = []
                    for row in data:
                        if len(row) >= 5:  # Ensure the row has enough columns
                            individual = Individual(
                                name=row[0],
                                vorname=row[1],
                                reisegruppe=row[2],
                                alter=row[3],
                                geschlecht=row[4]
                            )
                            individuals.append(individual)

                    selected_table = table_dropdown.GetStringSelection().strip()
                    if selected_table == "Team Table":
                        self.populate_team_grid(individuals)
                    elif selected_table == "Guest Table":
                        self.manager.individuals = individuals
                        self.populate_grid(self.manager.individuals)

        file_button.Bind(wx.EVT_BUTTON, on_file_button_click)

        if dialog.ShowModal() == wx.ID_OK:
            try:
                name = name_input.GetValue().strip()
                vorname = vorname_input.GetValue().strip()
                reisegruppe = reisegruppe_input.GetValue().strip()
                alter = int(alter_input.GetValue().strip())
                geschlecht = geschlecht_dropdown.GetStringSelection().strip()
                selected_table = table_dropdown.GetStringSelection().strip()

                individual = Individual(
                    name=name,
                    vorname=vorname,
                    reisegruppe=reisegruppe,
                    alter=alter,
                    geschlecht=geschlecht
                )

                if selected_table == "Team Table":
                    self.populate_team_grid([individual])
                elif selected_table == "Guest Table":
                    self.manager.individuals.append(individual)
                    self.populate_grid(self.manager.individuals)
            except ValueError:
                wx.MessageBox("Invalid input. Please ensure all fields are filled correctly.", "Error", wx.ICON_ERROR)

        dialog.Destroy()

    def populate_grid(self, individuals):
        """
        Populate the main grid with individual data.
        :param individuals: List of Individual objects
        """
        self.grid.ClearGrid()
        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())

        for row_idx, individual in enumerate(individuals):
            self.grid.AppendRows(1)
            self.grid.SetCellValue(row_idx, 0, individual.name)
            self.grid.SetCellValue(row_idx, 1, individual.vorname)
            self.grid.SetCellValue(row_idx, 2, individual.reisegruppe)
            self.grid.SetCellValue(row_idx, 3, str(individual.alter))
            self.grid.SetCellValue(row_idx, 4, individual.geschlecht)
            self.grid.SetCellValue(row_idx, 5, "Yes" if individual.anwesend else "No")
            self.grid.SetCellValue(row_idx, 6, "Yes" if individual.evakuiert else "No")
            self.grid.SetCellValue(row_idx, 7, individual.notiz)

        self.row_to_individual = {row_idx: individual for row_idx, individual in enumerate(individuals)}