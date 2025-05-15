# Kirchentag-App Check-in/Check-out Tool

## Overview
The Kirchentag-App is a check-in/check-out tool developed using wxPython and PyQt6. It allows users to manage attendance for events by tracking individuals' presence and providing a platform for personal notes. The app supports both local and networked (REST API) database backends.

## Project Structure
```
Kirchentag-App
├── src
│   ├── main.py            # Entry point for the application (PyQt6)
│   ├── main_frame.py      # UI class for the main window (PyQt6)
│   ├── main_frame_class.py# MainFrame logic (PyQt6)
│   ├── backend.py         # Business logic and data management
│   ├── db.py              # SQLite and networked DB backend
│   ├── api_server.py      # Flask REST API for networked mode
│   └── utils
│       └── csv_loader.py  # Utility functions for CSV loading
├── data
│   └── sample_data_X.csv  # Sample data for testing
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
- Count of present and evacuated individuals displayed.
- CSV file loading managed through a separate window.
- Real-time UI updates (polling every 2 seconds).
- Log field is scrollable and preserves scroll position.
- Supports both local SQLite and networked REST API database backends.

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

4. (Optional) To use networked mode, run the API server:
   ```
   python src/api_server.py
   ```
   And set the environment variable `NETWORK_DB=1` before starting the app.

## Usage
- Upon launching the application, the main window will display the attendance table.
- Use the "Anwesend" and "Evakuiert" buttons to update the status of individuals.
- Enter personal notes in the designated area.
- Load data from the CSV file through the provided interface.
- The log field is scrollable and will not snap to the bottom unless you are already at the bottom.
- The UI updates automatically every 2 seconds to reflect database changes.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.