import wx
import wx.grid
import pandas as pd
from utils.csv_loader import load_data  # Import the CSV/Excel data loader
from backend import CheckInOutManager, Individual  # Import backend classes

class CheckInCheckOutApp(wx.App):
    """
    Main application class for the Check-In/Check-Out tool.
    """
    def OnInit(self):
        self.frame = MainFrame()  # Create the main frame
        self.frame.Show()  # Show the frame
        return True

class MainFrame(wx.Frame):
    """
    Main GUI frame for the Check-In/Check-Out tool.
    """
    def create_grid(self, parent, num_columns, column_labels):
        """
        Create and configure a wx.Grid with specified columns and labels.
        :param parent: Parent widget for the grid
        :param num_columns: Number of columns in the grid
        :param column_labels: List of column labels
        :return: Configured wx.Grid instance
        """
        grid = wx.grid.Grid(parent)
        grid.CreateGrid(0, num_columns)
        for col_idx, label in enumerate(column_labels):
            grid.SetColLabelValue(col_idx, label)
        grid.EnableGridLines(False)
        grid.SetDefaultCellBackgroundColour(wx.Colour(240, 240, 240))
        grid.SetDefaultCellTextColour(wx.Colour(0, 0, 0))
        return grid

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
        self.search_bar.Bind(wx.EVT_TEXT, self.on_search)

        # Add a dropdown to select the table for searching
        self.table_selection = wx.Choice(self.panel, choices=["Team Table", "Guest Table"])
        self.table_selection.SetSelection(0)  # Default to the first option

        # Adjust layout to place the search bar and table selection side by side
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(self.search_bar, 1, wx.EXPAND | wx.ALL, 5)
        search_sizer.Add(self.table_selection, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(search_sizer, 0, wx.EXPAND)

        # Fix the search functionality to filter based on the selected table
        self.search_bar.Bind(wx.EVT_TEXT, self.on_search)
        self.table_selection.Bind(wx.EVT_CHOICE, self.on_search)

        # Create grids using the new helper method
        column_labels = ["Name", "Vorname", "Reisegruppe", "Alter", "Geschlecht", "Anwesend", "Evakuiert", "Notiz"]
        self.team_grid = self.create_grid(self.panel, len(column_labels), column_labels)
        self.grid = self.create_grid(self.panel, len(column_labels), column_labels)

        # Create a button to load data
        self.load_button = wx.Button(self.panel, label='Load File')
        self.load_button.SetBackgroundColour(wx.Colour(30, 144, 255))
        self.load_button.SetForegroundColour(wx.Colour(255, 255, 255))
        self.load_button.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.load_button.Bind(wx.EVT_BUTTON, self.on_load_csv)

        # Labels to display counts
        self.present_count_label = wx.StaticText(self.panel, label='Anwesend: 0')
        self.present_count_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.present_count_label.SetForegroundColour(wx.Colour(34, 139, 34))

        self.evacuated_count_label = wx.StaticText(self.panel, label='Evakuiert: 0')
        self.evacuated_count_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.evacuated_count_label.SetForegroundColour(wx.Colour(178, 34, 34))

        # Add widgets to the sizer
        self.sizer.Add(title, 0, wx.CENTER | wx.ALL, 10)
        self.sizer.Add(description, 0, wx.CENTER | wx.BOTTOM, 10)

        # Adjust the layout to stack the grids vertically with a 1/3 and 2/3 height ratio
        self.grid_sizer = wx.BoxSizer(wx.VERTICAL)

        # Center both tables within the grid sizer
        self.grid_sizer.Add(self.team_grid, 1, wx.EXPAND | wx.ALL, 10)
        self.grid_sizer.Add(self.grid, 2, wx.EXPAND | wx.ALL, 10)

        # Add the grid sizer to the main sizer
        self.sizer.Add(self.grid_sizer, 1, wx.EXPAND)

        # Adjust the grid size to fill the width of the window with a spacer
        self.sizer.AddSpacer(10)  # Add a spacer to the top
        self.grid_sizer.AddSpacer(10)  # Add a spacer to the left
        self.grid_sizer.AddSpacer(10)  # Add a spacer to the right
        self.sizer.AddSpacer(10)  # Add a spacer to the bottom

        # Ensure the layout is updated
        self.panel.SetSizerAndFit(self.sizer)

        self.sizer.Add(self.load_button, 0, wx.CENTER | wx.ALL, 5)

        self.panel.SetSizerAndFit(self.sizer)
        self.SetSizeHints(800, 600)
        self.Bind(wx.EVT_SIZE, self.on_resize)

        self.row_to_individual = {}

        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.on_cell_value_changed)
        self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_column_header_click)
        self.bind_team_grid_sorting()

        self.ShowFullScreen(False)  # Lock the window in fullscreen mode
        self.Center()  # Ensure the window is centered
        self.SetSize(self.GetVirtualSize())  # Adjust the size to match the display

        # Limit the team grid to show only 10 rows and make the rest scrollable
        self.team_grid.SetScrollLineY(10)

        # Lock the first table (team grid) to only 10 rows and keep it consistent on resize
        row_height = self.team_grid.GetDefaultRowSize()
        self.team_grid.SetMinSize(wx.Size(-1, row_height * 10))
        self.team_grid.SetMaxSize(wx.Size(-1, row_height * 10))

        # Calculate the initial size to fit all columns
        total_width = 800  # Default width for the window
        num_columns = len(column_labels)
        if num_columns > 0:
            column_width = total_width // num_columns
            total_width = column_width * num_columns  # Adjust total width to fit all columns

        self.SetSize(total_width, 600)  # Set the initial window size

        # Move the counters to the right of the tables and make them more prominent
        counter_sizer = wx.BoxSizer(wx.VERTICAL)

        self.present_count_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.evacuated_count_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        counter_sizer.Add(self.present_count_label, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        counter_sizer.Add(self.evacuated_count_label, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        # Add the counter sizer to the right of the grid sizer
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(counter_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        # Update the main sizer
        self.sizer.Clear(True)  # Clear existing layout
        self.sizer.Add(main_sizer, 1, wx.EXPAND)
        self.panel.SetSizerAndFit(self.sizer)

        # Finalize layout and explicitly show the frame
        print("Finalizing layout and showing MainFrame...")
        self.Layout()
        self.Show()
        print("MainFrame should now be visible.")

    def on_resize(self, event):
        """Handle window resize events."""
        self.Layout()  # Recalculate layout to adapt to new size
        self.panel.SetSizerAndFit(self.sizer)
        self.Fit()  # Adjust the frame size to fit the new layout
        event.Skip()

    def on_load_csv(self, event):
        """
        Open a dialog to select which table to populate and load data from a CSV or Excel file.
        """
        # Dialog to select the table
        with wx.SingleChoiceDialog(self, "Select Table", "Load Data", ["Team Table", "Guest Table"]) as choice_dialog:
            if choice_dialog.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled the dialog

            selected_table = choice_dialog.GetStringSelection()

        # File dialog to select the file
        with wx.FileDialog(self, "Open File", wildcard="CSV and Excel files (*.csv;*.xls;*.xlsx)|*.csv;*.xls;*.xlsx",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled the dialog

            file_path = file_dialog.GetPath()
            data = load_data(file_path)  # Use the updated loader
            if data:
                individuals = []  # Temporary list to store individuals
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

                # Populate the selected table
                if selected_table == "Team Table":
                    self.populate_team_grid(individuals)
                elif selected_table == "Guest Table":
                    self.manager.individuals = individuals  # Update the manager's individuals list
                    self.populate_grid(self.manager.individuals)

    def populate_grid(self, individuals):
        """
        Populate the grid with individual data.
        """
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

    def populate_team_grid(self, team_members):
        """
        Populate the team grid with team member data.
        """
        self.team_grid.ClearGrid()

        # Adjust the number of rows to match the data
        current_rows = self.team_grid.GetNumberRows()
        if current_rows > 0:
            self.team_grid.DeleteRows(0, current_rows)  # Remove all existing rows
        self.team_grid.AppendRows(len(team_members))  # Add rows for the new data

        # Populate the grid with the provided data
        for row_idx, member in enumerate(team_members):
            self.team_grid.SetCellValue(row_idx, 0, member.name)
            self.team_grid.SetCellValue(row_idx, 1, member.vorname)
            self.team_grid.SetCellValue(row_idx, 2, member.reisegruppe)
            self.team_grid.SetCellValue(row_idx, 3, str(member.alter))
            self.team_grid.SetCellValue(row_idx, 4, member.geschlecht)

            # Add buttons for "Anwesend" and "Evakuiert" with text showing the current state
            self.team_grid.SetCellRenderer(row_idx, 5, wx.grid.GridCellStringRenderer())
            self.team_grid.SetCellValue(row_idx, 5, 'Anwesend' if member.anwesend else 'Abwesend')
            self.team_grid.SetCellBackgroundColour(row_idx, 5, wx.Colour(0, 255, 0) if member.anwesend else wx.Colour(255, 0, 0))

            self.team_grid.SetCellRenderer(row_idx, 6, wx.grid.GridCellStringRenderer())
            self.team_grid.SetCellValue(row_idx, 6, 'Evakuiert' if member.evakuiert else 'Nicht evakuiert')
            self.team_grid.SetCellBackgroundColour(row_idx, 6, wx.Colour(0, 255, 0) if member.evakuiert else wx.Colour(255, 0, 0))

            self.team_grid.SetCellValue(row_idx, 7, member.notiz)
            self.team_grid.SetReadOnly(row_idx, 7, False)  # Ensure "Notizen" column is editable

            # Make the first six columns read-only (excluding "Notizen")
            for col_idx in range(5):
                self.team_grid.SetReadOnly(row_idx, col_idx, True)

        self.update_team_column_headers()  # Update headers with sorting indicator

    def update_column_headers(self):
        """
        Update column headers to show sorting indicator.
        """
        headers = ["Name", "Vorname", "Reisegruppe", "Alter", "Geschlecht", "Anwesend", "Evakuiert", "Notiz"]
        for col_idx, header in enumerate(headers):
            if hasattr(self, 'current_sort_column') and self.current_sort_column == col_idx:
                self.grid.SetColLabelValue(col_idx, f"{header} ↓")  # Add arrow for sorted column
            else:
                self.grid.SetColLabelValue(col_idx, header)

    def update_team_column_headers(self):
        """
        Update column headers of the team grid to show sorting indicator.
        """
        headers = ["Name", "Vorname", "Reisegruppe", "Alter", "Geschlecht", "Anwesend", "Evakuiert", "Notiz"]
        for col_idx, header in enumerate(headers):
            if hasattr(self, 'current_team_sort_column') and self.current_team_sort_column == col_idx:
                self.team_grid.SetColLabelValue(col_idx, f"{header} ↓")  # Add arrow for sorted column
            else:
                self.team_grid.SetColLabelValue(col_idx, header)

    def toggle_presence(self, event):
        """
        Toggle the presence status of an individual.
        """
        row = event.GetRow()
        self.manager.toggle_presence(row)
        self.update_counters()
        self.populate_grid(self.manager.individuals)

    def toggle_evacuated(self, event):
        """
        Toggle the evacuation status of an individual.
        """
        row = event.GetRow()
        self.manager.toggle_evacuated(row)
        self.update_counters()
        self.populate_grid(self.manager.individuals)

    def on_search(self, event):
        """
        Handle search queries and filter the grid data based on the selected table.
        """
        query = self.search_bar.GetValue()
        selected_table = self.table_selection.GetStringSelection()

        if selected_table == "Team Table":
            filtered_team_members = self.manager.search(query, table="team")  # Use the backend's search method for team
            self.populate_team_grid(filtered_team_members)
        elif selected_table == "Guest Table":
            filtered_individuals = self.manager.search(query, table="guest")  # Use the backend's search method for guests
            sorted_individuals = self.manager.sort_by_reisegruppe(filtered_individuals)
            self.populate_grid(sorted_individuals)

    def update_counters(self):
        """
        Update the counters for present and evacuated individuals.
        """
        present_count = self.manager.get_present_count()
        evacuated_count = self.manager.get_evacuated_count()
        self.present_count_label.SetLabel(f'Anwesend: {present_count}')
        self.evacuated_count_label.SetLabel(f'Evakuiert: {evacuated_count}')

    def on_cell_click(self, event):
        """
        Handle cell click events to toggle presence or evacuation status.
        """
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
        """
        Handle cell value changes to update notes.
        """
        row = event.GetRow()
        col = event.GetCol()

        if col == 7:  # "Notizen" column
            individual = self.row_to_individual.get(row)
            if individual:
                new_value = self.grid.GetCellValue(row, col)
                self.manager.update_note_by_id(individual.id, new_value)  # Update backend
                print(f"Updated note for {individual.name}: {new_value}")  # Debugging

    def sort_by_anwesend(self, event):
        """
        Sort the grid by the 'Anwesend' column, placing true buttons at the top.
        """
        sorted_individuals = sorted(self.manager.individuals, key=lambda ind: not ind.anwesend)
        self.populate_grid(sorted_individuals)

    def sort_by_evakuiert(self, event):
        """
        Sort the grid by the 'Evakuiert' column, placing true buttons at the top.
        """
        sorted_individuals = sorted(self.manager.individuals, key=lambda ind: not ind.evakuiert)
        self.populate_grid(sorted_individuals)

    def on_column_header_click(self, event):
        """
        Handle column header click to sort the grid by the selected column or revert to group sorting.
        """
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

    def on_team_column_header_click(self, event):
        """
        Handle column header click to sort the team grid by the selected column.
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
            elif col == 5:  # Anwesend
                sorted_team_members = sorted(self.manager.individuals, key=lambda ind: not ind.anwesend)
            elif col == 6:  # Evakuiert
                sorted_team_members = sorted(self.manager.individuals, key=lambda ind: not ind.evakuiert)
            elif col == 7:  # Notiz
                sorted_team_members = sorted(self.manager.individuals, key=lambda ind: ind.notiz)
            else:
                return  # Do nothing if an invalid column is clicked

        self.populate_team_grid(sorted_team_members)
        self.update_team_column_headers()  # Update headers with sorting indicator

    def bind_team_grid_sorting(self):
        """
        Bind the column header click event for sorting the team grid.
        """
        self.team_grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_team_column_header_click)

if __name__ == '__main__':
    app = CheckInCheckOutApp()
    app.MainLoop()