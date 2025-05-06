import wx
from wx.lib.agw.aui import AuiManager
from backend import Individual
from utils.csv_loader import load_data  # Import the updated CSV loader

def on_resize(event):
    """Handle window resize events."""
    frame = event.GetEventObject()
    frame.Layout()  # Recalculate layout to adapt to new size
    frame.panel.SetSizerAndFit(frame.sizer)
    frame.Fit()  # Adjust the frame size to fit the new layout
    event.Skip()

def on_load_csv(event):
    """
    Open a dialog to select which table to populate and load data from a CSV or Excel file.
    """
    frame = event.GetEventObject().GetParent().GetParent()  # Ensure we get the MainFrame instance
    with wx.SingleChoiceDialog(frame, "Select Table", "Load Data", ["Team Table", "Guest Table"]) as choice_dialog:
        if choice_dialog.ShowModal() == wx.ID_CANCEL:
            return  # User cancelled the dialog

        selected_table = choice_dialog.GetStringSelection()

    with wx.FileDialog(frame, "Open File", wildcard="CSV and Excel files (*.csv;*.xls;*.xlsx)|*.csv;*.xls;*.xlsx",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return  # User cancelled the dialog

        file_path = file_dialog.GetPath()
        data = load_data(file_path)  # Use the updated loader

        # Validate the data format
        if not data or not all(len(row) >= 5 for row in data):
            wx.MessageBox("The selected file is not in the correct format.", "Error", wx.ICON_ERROR)
            return

        if data:
            individuals = []
            for row in data:
                if len(row) >= 5:
                    individual = Individual(
                        name=row[0],
                        vorname=row[1],
                        reisegruppe=row[2],
                        alter=row[3],
                        geschlecht=row[4]
                    )
                    individuals.append(individual)

            if selected_table == "Team Table":
                frame.populate_team_grid(individuals)
            elif selected_table == "Guest Table":
                frame.manager.individuals = individuals
                frame.populate_grid(frame.manager.individuals)