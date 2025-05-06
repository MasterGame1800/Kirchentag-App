import csv
import uuid  # Import for generating unique IDs
from utils.csv_loader import load_data, save_csv  # Import the updated CSV functions

class Individual:
    """
    Represents an individual with attributes such as name, group, age, gender, and status.
    """
    def __init__(self, name, vorname, reisegruppe, alter, geschlecht):
        self.id = str(uuid.uuid4())  # Generate a unique ID for the individual
        self.name = name  # Last name of the individual
        self.vorname = vorname  # First name of the individual
        self.reisegruppe = reisegruppe  # Group the individual belongs to
        self.alter = alter  # Age of the individual
        self.geschlecht = geschlecht  # Gender of the individual
        self.anwesend = False  # Presence status (default: False)
        self.evakuiert = False  # Evacuation status (default: False)
        self.notiz = ""  # Personal notes (default: empty string)

class CheckInOutManager:
    """
    Manages a list of individuals and provides methods for updating their status and notes.
    """
    def __init__(self):
        self.individuals = []  # List to store Individual objects

    def load_data(self, filepath):
        """
        Loads individual data from a file and populates the individuals list.
        :param filepath: Path to the file (CSV or Excel)
        """
        data = load_data(filepath)  # Use the updated loader
        if not data:
            print(f"Failed to load data from {filepath}. Please check the file format.")
            return

        self.individuals = []  # Clear existing data
        for row in data:
            if len(row) >= 5:  # Ensure the row has enough columns
                individual = Individual(
                    name=row[0],
                    vorname=row[1],
                    reisegruppe=row[2],
                    alter=row[3],
                    geschlecht=row[4]
                )
                self.individuals.append(individual)

    def toggle_presence(self, index):
        """
        Toggles the presence status of an individual by index.
        :param index: Index of the individual in the list
        """
        if 0 <= index < len(self.individuals):
            self.individuals[index].anwesend = not self.individuals[index].anwesend

    def toggle_evacuated(self, index):
        """
        Toggles the evacuation status of an individual by index.
        :param index: Index of the individual in the list
        """
        if 0 <= index < len(self.individuals):
            self.individuals[index].evakuiert = not self.individuals[index].evakuiert

    def toggle_presence_by_id(self, individual_id):
        """
        Toggles the presence status of an individual by their unique ID.
        :param individual_id: Unique ID of the individual
        """
        for individual in self.individuals:
            if individual.id == individual_id:
                individual.anwesend = not individual.anwesend
                break

    def toggle_evacuated_by_id(self, individual_id):
        """
        Toggles the evacuation status of an individual by their unique ID.
        :param individual_id: Unique ID of the individual
        """
        for individual in self.individuals:
            if individual.id == individual_id:
                individual.evakuiert = not individual.evakuiert
                break

    def get_present_count(self):
        """
        Returns the count of individuals marked as present.
        :return: Count of present individuals
        """
        return sum(1 for individual in self.individuals if individual.anwesend)

    def get_evacuated_count(self):
        """
        Returns the count of individuals marked as evacuated.
        :return: Count of evacuated individuals
        """
        return sum(1 for individual in self.individuals if individual.evakuiert)

    def update_note(self, index, note):
        """
        Updates the personal note of an individual by index.
        :param index: Index of the individual in the list
        :param note: New note to be set
        """
        if 0 <= index < len(self.individuals):
            self.individuals[index].notiz = note

    def update_note_by_id(self, individual_id, note):
        """
        Updates the personal note of an individual by their unique ID.
        :param individual_id: Unique ID of the individual
        :param note: New note to be set
        """
        for individual in self.individuals:
            if individual.id == individual_id:
                individual.notiz = note
                break

    def search(self, query, table=None):
        """
        Filters individuals based on a search query and optionally by table.
        :param query: The search string (case-insensitive)
        :param table: Optional table name to filter individuals (e.g., 'guest', 'staff')
        :return: List of individuals matching the query and table
        """
        query = query.lower()
        filtered = [
            individual for individual in self.individuals
            if query in individual.name.lower()
            or query in individual.vorname.lower()
            or query in individual.reisegruppe.lower()
        ]

        if table:
            # Example logic for filtering by table (adjust as needed)
            if table == "guest":
                filtered = [ind for ind in filtered if ind.reisegruppe == "Guest"]
            elif table == "staff":
                filtered = [ind for ind in filtered if ind.reisegruppe == "Staff"]

        return filtered

    def sort_by_reisegruppe(self, individuals=None):
        """
        Sorts individuals alphabetically by their group.
        :param individuals: Optional list of individuals to sort (defaults to self.individuals)
        :return: Sorted list of individuals
        """
        if individuals is None:
            individuals = self.individuals
        return sorted(individuals, key=lambda x: x.reisegruppe.lower())