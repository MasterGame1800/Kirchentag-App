import wx
from backend import CheckInOutManager
from grids import create_grid
from counters import update_counters
from search_and_filter import on_search
from events import on_resize, on_load_csv

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
        self.load_button.Bind(wx.EVT_BUTTON, on_load_csv)

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
        """Handle column header click to sort the grid by the selected column."""
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