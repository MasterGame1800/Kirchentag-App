import csv
import os
import pandas as pd

def load_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def save_csv(file_path, data):
    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def load_data(file_path):
    """
    Loads data from a file (CSV or Excel) and returns it as a list of rows.
    Each row is represented as a list of values.

    :param file_path: Path to the file
    :return: List of rows from the file
    """
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.csv':
            try:
                # Read CSV file and skip problematic rows
                df = pd.read_csv(file_path, on_bad_lines='skip')
            except Exception as e:
                print(f"Error reading CSV file: {e}")
                return []
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        return df.values.tolist()
    except Exception as e:
        print(f"Error loading file: {e}")
        return []