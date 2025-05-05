# Kirchentag-App Check-in/Check-out Tool

## Overview
The Kirchentag-App is a check-in/check-out tool developed using wxPython. It allows users to manage attendance for events by tracking individuals' presence and providing a platform for personal notes.

## Project Structure
```
Kirchentag-App
├── src
│   ├── frontend.py      # wxPython GUI implementation
│   ├── backend.py       # Business logic and data management
│   ├── main.py          # Entry point for the application
│   └── utils
│       └── csv_loader.py # Utility functions for CSV loading
├── data
│   └── sample_data.csv   # Sample data for testing
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Features
- Eight columns in the main interface: 
  - Name
  - Vorname
  - Reisegruppe
  - Alter
  - Geschlecht
  - Anwesend (Presence button)
  - Evakuiert (Evacuated button)
  - Notiz (Personal notes area)
- Count of present individuals displayed.
- CSV file loading managed through a separate window.

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd Kirchentag-App
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage
- Upon launching the application, the main window will display the attendance table.
- Use the "Anwesend" and "Evakuiert" buttons to update the status of individuals.
- Enter personal notes in the designated area.
- Load data from the CSV file through the provided interface.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.