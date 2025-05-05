import wx
import wx.grid
import pandas as pd
from utils.csv_loader import load_data  # Corrected import
from backend import CheckInOutManager, Individual  # Ensure Individual is imported

class CheckInCheckOutApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame()
        self.frame.Show()
        return True

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Check-In/Check-Out Tool')
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
        self.search_bar.Bind(wx.EVT_TEXT, self.on_search)

        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(0, 8)
        self.grid.SetColLabelValue(0, "Name")
        self.grid.SetColLabelValue(1, "Vorname")
        self.grid.SetColLabelValue(2, "Reisegruppe")
        self.grid.SetColLabelValue(3, "Alter")
        self.grid.SetColLabelValue(4, "Geschlecht")
        self.grid.SetColLabelValue(5, "Anwesend")
        self.grid.SetColLabelValue(6, "Evakuiert")
        self.grid.SetColLabelValue(7, "Notiz")

        # Hide grid lines
        self.grid.EnableGridLines(False)

        # Add alternating row colors
        self.grid.SetDefaultCellBackgroundColour(wx.Colour(240, 240, 240))
        self.grid.SetDefaultCellTextColour(wx.Colour(0, 0, 0))

        # Update buttons to look more modern
        self.load_button = wx.Button(self.panel, label='Load File')
        self.load_button.SetBackgroundColour(wx.Colour(30, 144, 255))  # Set button color
        self.load_button.SetForegroundColour(wx.Colour(255, 255, 255))  # Set text color
        self.load_button.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.load_button.Bind(wx.EVT_BUTTON, self.on_load_csv)

        self.present_count_label = wx.StaticText(self.panel, label='Anwesend: 0')
        self.present_count_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.present_count_label.SetForegroundColour(wx.Colour(34, 139, 34))

        self.evacuated_count_label = wx.StaticText(self.panel, label='Evakuiert: 0')
        self.evacuated_count_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.evacuated_count_label.SetForegroundColour(wx.Colour(178, 34, 34))

        # Add widgets to the sizer
        self.sizer.Add(title, 0, wx.CENTER | wx.ALL, 10)
        self.sizer.Add(description, 0, wx.CENTER | wx.BOTTOM, 10)
        self.sizer.Add(self.search_bar, 0, wx.EXPAND | wx.ALL, 5)  # Search bar expands horizontally
        self.sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)  # Grid expands in both directions with padding
        self.sizer.Add(self.load_button, 0, wx.CENTER | wx.ALL, 5)  # Load button stays centered
        self.sizer.Add(self.present_count_label, 0, wx.CENTER | wx.ALL, 5)  # Present count stays centered
        self.sizer.Add(self.evacuated_count_label, 0, wx.CENTER | wx.ALL, 5)  # Evacuated count stays centered

        self.panel.SetSizerAndFit(self.sizer)  # Ensure the sizer adapts to the panel
        self.SetSizeHints(800, 600)  # Set minimum window size
        self.Bind(wx.EVT_SIZE, self.on_resize)  # Bind resize event

        self.row_to_individual = {}  # Map grid rows to Individual objects

        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.on_cell_value_changed)

        # Bind column header click event for sorting
        self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_column_header_click)

    def on_resize(self, event):
        """Handle window resize events and adjust grid size dynamically."""
        self.Layout()  # Recalculate layout to adapt to new size

        # Dynamically adjust grid column widths
        total_width = self.grid.GetSize().GetWidth()
        num_columns = self.grid.GetNumberCols()
        if num_columns > 0:
            col_width = total_width // num_columns
            extra_space = total_width - (col_width * num_columns)
            for col in range(num_columns):
                if col == num_columns - 1:  # Add extra space to the last column
                    self.grid.SetColSize(col, col_width + extra_space)
                else:
                    self.grid.SetColSize(col, col_width)

        event.Skip()

    def on_load_csv(self, event):
        with wx.FileDialog(self, "Open File", wildcard="CSV and Excel files (*.csv;*.xls;*.xlsx)|*.csv;*.xls;*.xlsx",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled the dialog

            file_path = file_dialog.GetPath()
            data = load_data(file_path)  # Use the updated loader
            if data:
                self.manager.individuals = []  # Clear existing data
                for row in data:
                    if len(row) >= 5:  # Ensure the row has enough columns
                        individual = Individual(
                            name=row[0],
                            vorname=row[1],
                            reisegruppe=row[2],
                            alter=row[3],
                            geschlecht=row[4]
                        )
                        self.manager.individuals.append(individual)
                self.populate_grid(self.manager.individuals)

    def populate_grid(self, individuals):
        # Default to sorting by group if no specific sorting is applied
        if not hasattr(self, 'current_sort_column') or self.current_sort_column is None:
            individuals = sorted(individuals, key=lambda ind: ind.reisegruppe if ind.reisegruppe else "")

        self.grid.ClearGrid()
        self.row_to_individual.clear()  # Clear the mapping

        # Adjust the number of rows to match the data
        current_rows = self.grid.GetNumberRows()
        if current_rows > 0:
            self.grid.DeleteRows(0, current_rows)  # Remove all existing rows
        self.grid.AppendRows(len(individuals))  # Add rows for the new data

        # Populate the grid with the provided data
        for row_idx, individual in enumerate(individuals):
            self.row_to_individual[row_idx] = individual  # Map row to individual
            self.grid.SetCellValue(row_idx, 0, individual.name)
            self.grid.SetCellValue(row_idx, 1, individual.vorname)
            self.grid.SetCellValue(row_idx, 2, individual.reisegruppe)
            self.grid.SetCellValue(row_idx, 3, str(individual.alter))
            self.grid.SetCellValue(row_idx, 4, individual.geschlecht)

            # Add buttons for "Anwesend" and "Evakuiert" with text showing the current state
            self.grid.SetCellRenderer(row_idx, 5, wx.grid.GridCellStringRenderer())
            self.grid.SetCellValue(row_idx, 5, 'Anwesend' if individual.anwesend else 'Abwesend')
            self.grid.SetCellBackgroundColour(row_idx, 5, wx.Colour(0, 255, 0) if individual.anwesend else wx.Colour(255, 0, 0))

            self.grid.SetCellRenderer(row_idx, 6, wx.grid.GridCellStringRenderer())
            self.grid.SetCellValue(row_idx, 6, 'Evakuiert' if individual.evakuiert else 'Nicht evakuiert')
            self.grid.SetCellBackgroundColour(row_idx, 6, wx.Colour(0, 255, 0) if individual.evakuiert else wx.Colour(255, 0, 0))

            self.grid.SetCellValue(row_idx, 7, individual.notiz)
            self.grid.SetReadOnly(row_idx, 7, False)  # Ensure "Notizen" column is editable

            # Make the first six columns read-only (excluding "Notizen")
            for col_idx in range(5):
                self.grid.SetReadOnly(row_idx, col_idx, True)

        # Update column headers with sorting indicator
        self.update_column_headers()

        # Bind events for toggling "Anwesend" and "Evakuiert"
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_cell_click)

        self.update_counters()

    def update_column_headers(self):
        """Update column headers to show sorting indicator."""
        headers = ["Name", "Vorname", "Reisegruppe", "Alter", "Geschlecht", "Anwesend", "Evakuiert", "Notiz"]
        for col_idx, header in enumerate(headers):
            if hasattr(self, 'current_sort_column') and self.current_sort_column == col_idx:
                self.grid.SetColLabelValue(col_idx, f"{header} ↓")  # Add arrow for sorted column
            else:
                self.grid.SetColLabelValue(col_idx, header)

    def toggle_presence(self, event):
        row = event.GetRow()
        self.manager.toggle_presence(row)
        self.update_counters()
        self.populate_grid(self.manager.individuals)

    def toggle_evacuated(self, event):
        row = event.GetRow()
        self.manager.toggle_evacuated(row)
        self.update_counters()
        self.populate_grid(self.manager.individuals)

    def on_search(self, event):
        query = self.search_bar.GetValue()
        filtered_individuals = self.manager.search(query)  # Use the backend's search method
        sorted_individuals = self.manager.sort_by_reisegruppe(filtered_individuals)
        self.populate_grid(sorted_individuals)

    def update_counters(self):
        present_count = self.manager.get_present_count()
        evacuated_count = self.manager.get_evacuated_count()
        self.present_count_label.SetLabel(f'Anwesend: {present_count}')
        self.evacuated_count_label.SetLabel(f'Evakuiert: {evacuated_count}')

    def on_cell_click(self, event):
        row = event.GetRow()
        col = event.GetCol()

        individual = self.row_to_individual.get(row)  # Get the individual by row
        if not individual:
            return

        if col == 5:  # "Anwesend" column
            self.manager.toggle_presence_by_id(individual.id)
        elif col == 6:  # "Evakuiert" column
            self.manager.toggle_evacuated_by_id(individual.id)

        # Update the grid and counters after toggling
        self.update_counters()
        self.populate_grid(self.manager.individuals)

    def on_cell_value_changed(self, event):
        row = event.GetRow()
        col = event.GetCol()

        if col == 7:  # "Notizen" column
            individual = self.row_to_individual.get(row)
            if individual:
                new_value = self.grid.GetCellValue(row, col)
                self.manager.update_note_by_id(individual.id, new_value)  # Update backend
                print(f"Updated note for {individual.name}: {new_value}")  # Debugging

    def sort_by_anwesend(self, event):
        """Sort the grid by the 'Anwesend' column, placing true buttons at the top."""
        sorted_individuals = sorted(self.manager.individuals, key=lambda ind: not ind.anwesend)
        self.populate_grid(sorted_individuals)

    def sort_by_evakuiert(self, event):
        """Sort the grid by the 'Evakuiert' column, placing true buttons at the top."""
        sorted_individuals = sorted(self.manager.individuals, key=lambda ind: not ind.evakuiert)
        self.populate_grid(sorted_individuals)

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

if __name__ == '__main__':
    app = CheckInCheckOutApp()
    app.MainLoop()