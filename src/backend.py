import csv
import uuid  # Add this import

class Individual:
    def __init__(self, name, vorname, reisegruppe, alter, geschlecht):
        self.id = str(uuid.uuid4())  # Generate a unique ID
        self.name = name
        self.vorname = vorname
        self.reisegruppe = reisegruppe
        self.alter = alter
        self.geschlecht = geschlecht
        self.anwesend = False
        self.evakuiert = False
        self.notiz = ""

class CheckInOutManager:
    def __init__(self):
        self.individuals = []

    def load_data(self, filepath):
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                individual = Individual(
                    name=row['Name'],
                    vorname=row['Vorname'],
                    reisegruppe=row['Reisegruppe'],
                    alter=row['Alter'],
                    geschlecht=row['Geschlecht']
                )
                self.individuals.append(individual)

    def toggle_presence(self, index):
        if 0 <= index < len(self.individuals):
            self.individuals[index].anwesend = not self.individuals[index].anwesend

    def toggle_evacuated(self, index):
        if 0 <= index < len(self.individuals):
            self.individuals[index].evakuiert = not self.individuals[index].evakuiert

    def toggle_presence_by_id(self, individual_id):
        for individual in self.individuals:
            if individual.id == individual_id:
                individual.anwesend = not individual.anwesend
                break

    def toggle_evacuated_by_id(self, individual_id):
        for individual in self.individuals:
            if individual.id == individual_id:
                individual.evakuiert = not individual.evakuiert
                break

    def get_present_count(self):
        return sum(1 for individual in self.individuals if individual.anwesend)

    def get_evacuated_count(self):
        """
        Returns the count of individuals marked as evacuated.
        """
        return sum(1 for individual in self.individuals if individual.evakuiert)

    def update_note(self, index, note):
        if 0 <= index < len(self.individuals):
            self.individuals[index].notiz = note

    def update_note_by_id(self, individual_id, note):
        for individual in self.individuals:
            if individual.id == individual_id:
                individual.notiz = note
                break

    def search(self, query):
        """
        Filters individuals based on the query in the first three columns.
        :param query: The search string (case-insensitive).
        :return: A list of individuals matching the query.
        """
        query = query.lower()
        return [
            individual for individual in self.individuals
            if query in individual.name.lower()
            or query in individual.vorname.lower()
            or query in individual.reisegruppe.lower()
        ]

    def sort_by_reisegruppe(self, individuals=None):
        """
        Sorts the list of individuals alphabetically by the 'Reisegruppe' column.
        :param individuals: Optional list of individuals to sort. Defaults to self.individuals.
        :return: Sorted list of individuals.
        """
        if individuals is None:
            individuals = self.individuals
        return sorted(individuals, key=lambda x: x.reisegruppe.lower())