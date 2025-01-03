# StudentTrackApp

**StudentTrackApp** is an intuitive and user-friendly application designed to manage and track student information using **SQL Server** and **PyQt5**. 
This application enables users to select courses and faculties, perform detailed searches, retrieve data from the database, and display the results in a clear and organized manner.

## Features

- **Course and Faculty Selection**: Easily select and manage faculties and courses.
- **Detailed Search**: Perform detailed searches with multiple filters including date ranges.
- **Data Retrieval**: Retrieve and display student information in a structured format.
- **User-Friendly Interface**: Designed with an intuitive and easy-to-navigate interface using PyQt5.
- **Secure Configuration**: Securely manage database connection settings.

## Installation

To install and run StudentTrackApp, follow these steps:

1. **Clone the repository and open it in your IDE, like PyCharm**

2. **Configure the database connection**:
    Update the `config.ini` file with your database connection settings:
    ```ini
    [Database_Con]
    Server = YOUR_SERVER_NAME
    Database = YOUR_DATABASE_NAME
    UID = YOUR_USER_ID
    PWD = YOUR_PASSWORD
    ```

---


## Usage

1. **Run the application**:
    ```bash
    python ssms.py
    ```

2. **Navigate the UI**:
    - Select the faculty and course from the dropdown menus.
    - Use the search bar and date range filters to perform detailed searches.
    - Click "Fetch Data" to retrieve and display the student information.

## Building the Executable

To create an executable for StudentTrackApp using `cx_Freeze`, follow these steps:

1. **Install cx_Freeze**:
    ```bash
    pip install cx_Freeze
    ```

2. **Run the setup script**:
    ```bash
    python setup.py bdist_msi
    ```

The executable will be created in the `build` and `dist` directory.

