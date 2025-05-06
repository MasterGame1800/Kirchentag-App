import csv
import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_csv(file_path):
    """
    Reads data from a CSV file and returns it as a list of dictionaries.
    :param file_path: Path to the CSV file
    :return: List of dictionaries representing rows in the CSV file
    """
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        logging.info(f"Successfully loaded CSV file: {file_path}")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
    return data

def save_csv(file_path, data):
    """
    Writes data to a CSV file.
    :param file_path: Path to the CSV file
    :param data: List of dictionaries to write to the file
    """
    try:
        with open(file_path, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = data[0].keys()  # Use keys from the first dictionary as column headers
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row
            writer.writerows(data)  # Write the data rows
        logging.info(f"Successfully saved data to CSV file: {file_path}")
    except Exception as e:
        logging.error(f"Error writing to CSV file: {e}")

def load_data(file_path):
    """
    Loads data from a file (CSV or Excel) and returns it as a list of rows.
    Each row is represented as a list of values.

    :param file_path: Path to the file
    :return: List of rows from the file
    """
    try:
        file_extension = os.path.splitext(file_path)[1].lower()  # Get the file extension
        if file_extension == '.csv':
            try:
                # Read CSV file and skip problematic rows
                df = pd.read_csv(file_path, on_bad_lines='skip')
                logging.info(f"Successfully loaded CSV file: {file_path}")
            except Exception as e:
                logging.error(f"Error reading CSV file: {e}")
                return []
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)  # Read Excel file
            logging.info(f"Successfully loaded Excel file: {file_path}")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        return df.values.tolist()  # Convert DataFrame to a list of lists
    except ValueError as ve:
        logging.error(f"Value error: {ve}")
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        return []