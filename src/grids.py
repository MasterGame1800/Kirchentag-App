import wx.grid

def create_grid(parent, num_columns, column_labels):
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