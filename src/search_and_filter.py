
def on_search(event):
    """
    Handle search queries and filter the grid data based on the selected table.
    """
    query = event.GetEventObject().GetValue()
    selected_table = event.GetEventObject().GetParent().table_selection.GetStringSelection()

    if selected_table == "Team Table":
        filtered_team_members = event.GetEventObject().GetParent().manager.search(query, table="team")
        event.GetEventObject().GetParent().populate_team_grid(filtered_team_members)
    elif selected_table == "Guest Table":
        filtered_individuals = event.GetEventObject().GetParent().manager.search(query, table="guest")
        sorted_individuals = event.GetEventObject().GetParent().manager.sort_by_reisegruppe(filtered_individuals)
        event.GetEventObject().GetParent().populate_grid(sorted_individuals)