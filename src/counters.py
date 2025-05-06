def update_counters(manager, present_count_label, evacuated_count_label):
    """
    Update the counters for present and evacuated individuals.
    :param manager: The backend manager instance
    :param present_count_label: Label for present count
    :param evacuated_count_label: Label for evacuated count
    """
    present_count = manager.get_present_count()
    evacuated_count = manager.get_evacuated_count()
    present_count_label.SetLabel(f'Anwesend: {present_count}')
    evacuated_count_label.SetLabel(f'Evakuiert: {evacuated_count}')