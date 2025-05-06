import csv
import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_csv(file_path):
    """
    Reads data from a CSV file and returns it as a list of rows.
    Each row is represented as a list of values, excluding the header.

    :param file_path: Path to the CSV file
    :return: List of rows from the CSV file (excluding the header)
    """
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            data = [row for row in reader]
        logging.info(f"Successfully loaded CSV file: {file_path}")
        return data
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
    return []

def save_csv(file_path, data, headers=None):
    """
    Writes data to a CSV file.

    :param file_path: Path to the CSV file
    :param data: List of rows to write to the file
    :param headers: Optional list of column headers
    """
    try:
        with open(file_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            if headers:
                writer.writerow(headers)  # Write the header row
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
    if not os.path.exists(file_path):
        logging.error(f"File does not exist: {file_path}")
        return []

    file_extension = os.path.splitext(file_path)[1].lower()
    try:
        if file_extension == '.csv':
            return load_csv(file_path)
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
            logging.info(f"Successfully loaded Excel file: {file_path}")
            return df.values.tolist()
        else:
            logging.error(f"Unsupported file type: {file_extension}")
    except Exception as e:
        logging.error(f"Error loading file: {file_path}. Details: {e}")
    return []