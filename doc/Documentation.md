# <img src="../UniDataTracker.ico" alt="App Screenshot" width="40"/> UniDataTracker Documentation

## Overview
UniDataTracker is a PyQt5-based application designed to manage and track university data, such as faculty and course information. The application connects to a SQL Server database, fetches data based on user inputs, and displays it in a tabular format. Additionally, it provides search functionality within the data.

## Features
- **Faculty and Course Selection**: Users can select faculty and courses from dropdown menus.
- **Data Fetching**: Fetch data from the database based on selected faculty and course.
- **Search Functionality**: Search the displayed data using keywords and date ranges.
- **Responsive UI**: The application uses a grid layout to ensure a responsive user interface.

## Code Structure
### Importing Libraries
The application imports necessary libraries including `configparser`, `pyodbc`, and various modules from `PyQt5`.

### Main Window Class
The `MyWindow` class inherits from `QMainWindow` and sets up the user interface and functionalities.

#### Initialization
- Sets up the window properties (title, size, icon).
- Creates and arranges UI elements using a `QGridLayout`.
- Reads database configuration from `config.ini`.

#### UI Elements
- **Labels**: `QLabel` for faculty, course, and date labels.
- **Combo Boxes**: `QComboBox` for faculty and course selection.
- **Buttons**: `QPushButton` for fetching data, searching, and exiting.
- **Table Widget**: `QTableWidget` for displaying fetched data.
- **Line Edit**: `QLineEdit` for search input.
- **Date Edit**: `QDateEdit` for selecting date ranges.

#### Styles
The application defines styles for buttons, labels, date edits, and line edits to enhance the visual appearance.

#### Methods
- `update_faculty()`: Fetches and updates the faculty list from the database.
- `update_courses()`: Updates the course list based on the selected faculty.
- `fetch_data()`: Fetches data from the database based on selected faculty and course and displays it in the table widget.
- `search_data_db()`: Searches the database for records matching the search text and date range.
- `handleQuit()`: Handles the exit confirmation dialog.

## Database Configuration
Database connection details are read from the `config.ini` file, which should be placed in the application's directory.

Example `config.ini` format:
```ini
[Database_Con]
Server=your_server_name
Database=your_database_name
UID=your_user_id
PWD=your_password
```

## Usage
1. **Run the Application**: Start the application and the main window will appear.
2. **Select Faculty and Course**: Use the dropdown menus to select faculty and course.
3. **Fetch Data**: Click the "Fetch Data" button to load data into the table.
4. **Search Data**: Enter keywords and select date ranges to search within the displayed data.
5. **Exit**: Click the "Exit" button to close the application.

