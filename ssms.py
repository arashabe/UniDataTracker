import configparser

import pyodbc
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QComboBox, QLabel, QPushButton, \
    QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox, QDateEdit


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UniDataTracker")
        self.setMinimumSize(1100, 600)
        self.setGeometry(350, 200, 1200, 600)
        self.setWindowIcon(QIcon('UniDataTracker.ico'))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        central_widget.setLayout(layout)

        self.faculty_label = QLabel("Faculty:")
        self.faculty_combo = QComboBox()
        self.faculty_combo.currentIndexChanged.connect(self.update_courses)

        self.course_label = QLabel("Course:")
        self.course_combo = QComboBox()

        self.btn_fetch_data = QPushButton("Fetch Data")
        self.btn_fetch_data.clicked.connect(self.fetch_data)

        self.table_widget = QTableWidget()

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search ....")
        self.search_edit.setMinimumSize(200, 25)
        self.search_edit.setMaximumSize(300, 25)
        self.date_edit_start_label = QLabel("From:")
        self.date_edit_start = QDateEdit()
        self.date_edit_start.setCalendarPopup(True)
        self.date_edit_start.setDate(QDate.currentDate())
        self.date_edit_end_label = QLabel("To:")
        self.date_edit_end = QDateEdit()
        self.date_edit_end.setCalendarPopup(True)
        self.date_edit_end.setDate(QDate.currentDate())
        self.search_edit.returnPressed.connect(self.search_data_db)
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_data_db)

        # file config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.server_name = config['Database_Con']['Server']
        self.database_name = config['Database_Con']['Database']
        self.uid = config['Database_Con']['UID']
        self.pwd = config['Database_Con']['PWD']

        layout.setSpacing(5)
        layout.addWidget(self.faculty_label, 0, 0)
        layout.addWidget(self.faculty_combo, 0, 1)
        layout.setColumnStretch(1, 1)
        layout.addWidget(self.course_label, 0, 2)
        layout.addWidget(self.course_combo, 0, 3)
        layout.setColumnStretch(3, 1)
        layout.addWidget(self.btn_fetch_data, 0, 4)
        layout.setColumnStretch(4, 1)
        layout.addWidget(self.table_widget, 1, 0, 1, 11)

        # search field
        layout.addWidget(self.search_edit, 0, 5)
        layout.addWidget(self.date_edit_start_label, 0, 6)
        layout.addWidget(self.date_edit_start, 0, 7)
        layout.addWidget(self.date_edit_end_label, 0, 8)
        layout.addWidget(self.date_edit_end, 0, 9)
        layout.addWidget(self.search_button, 0, 10)

        # "EXIT" Button
        self.pushButtonExit = QPushButton(self)
        self.pushButtonExit.setText("Exit")
        self.pushButtonExit.clicked.connect(self.handleQuit)
        layout.addWidget(self.pushButtonExit, 2, 10)

        # Style sheet
        button_style = """
        QPushButton {
            background-color: #017d14;  
            color: white; 
            font-weight: bold;
            border: 2px solid #02540e; 
            border-radius: 10px;  
            padding: 5px 10px;
            min-height: 10px;
            max-height: 10px;  
        }

        QPushButton:hover {
            background-color: #02540e; 
        }

        QPushButton:pressed {
            background-color: #017d14; 
        }
        """
        self.btn_fetch_data.setStyleSheet(button_style)
        self.search_button.setStyleSheet(button_style)
        self.pushButtonExit.setStyleSheet(button_style)
        self.update_faculty()

        label_style = """
        QLabel {
            font-size: 14px; 
            font-weight: bold; 
            color: #333333; 
            margin: 5px;
 
        }
        """

        date_edit_style = """
        QDateEdit {
            background-color: #FFFFFF; 
            color: #333333; 
            border: 1px solid #CCCCCC;  
            border-radius: 5px;  
            padding: 2px 5px;
            min-height: 15px;
            max-height: 15px; 
        }
    
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 1px;
            border-left-color: #CCCCCC;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }
        """

        line_edit_style = """
        QLineEdit {
            background-color: #FFFFFF;  
            color: #333333;  
            border: 1px solid #CCCCCC;  
            border-radius: 5px;  
            padding: 2px 5px;
            min-height: 15px;
            max-height: 15px;  
        }
    
        QLineEdit:focus {
            border: 1px solid #4CAF50;  
        }
        """

        self.course_label.setStyleSheet(label_style)
        self.faculty_label.setStyleSheet(label_style)
        self.date_edit_start.setStyleSheet(date_edit_style)
        self.date_edit_end.setStyleSheet(date_edit_style)
        self.search_edit.setStyleSheet(line_edit_style)

    def update_faculty(self):
        self.faculty_combo.clear()

        # Connection to the database with login uid and pwd
        # conn = pyodbc.connect(f'Driver={{SQL Server Native Client 11.0}};Server={self.server_name};Database={self.database_name};UID={self.uid};PWD={self.pwd};')

        # Connection to the database with Windows authentication
        try:
            conn = pyodbc.connect(f'Driver={{SQL Server Native Client 11.0}};Server={self.server_name};Database={self.database_name};Trusted_Connection=yes;')

            cursor = conn.cursor()

        except pyodbc.Error as e:
        # Handle the exception
            error_msg = f"Error during database connection: {str(e)}"
            QMessageBox.critical(self, "Connection Error", error_msg)

        # Query to retrieve distinct faculties
        query = "SELECT DISTINCT faculty FROM students_info"
        cursor.execute(query)

        # Populate faculty_combo with distinct faculties obtained from the query
        for row in cursor.fetchall():
            self.faculty_combo.addItem(row[0])

        conn.close()

    def update_courses(self):
        self.course_combo.clear()
        faculty = self.faculty_combo.currentText()

        # Connection to the database with login uid and pwd
        # try:
            # conn = pyodbc.connect(f'Driver={{SQL Server Native Client 11.0}};Server={self.server_name};Database={self.database_name};UID={self.uid};PWD={self.pwd};')

        # Connection to the database with Windows authentication
        try:
            conn = pyodbc.connect(f'Driver={{SQL Server Native Client 11.0}};Server={self.server_name};Database={self.database_name};Trusted_Connection=yes;')

            cursor = conn.cursor()

        except pyodbc.Error as e:
        # Handle the exception
            error_msg = f"Error during database connection: {str(e)}"
            QMessageBox.critical(self, "Connection Error", error_msg)

        # Query to retrieve distinct courses related to the selected faculty
        query = "SELECT DISTINCT Course FROM students_info WHERE faculty = ?"
        cursor.execute(query, (faculty,))

        # Populate course_combo with distinct courses obtained from the query
        for row in cursor.fetchall():
            self.course_combo.addItem(row[0])

        conn.close()

    def fetch_data(self):
        # Connection to the database with login uid and pwd
        # conn = pyodbc.connect(f'Driver={{SQL Server Native Client 11.0}};Server={self.server_name};Database={self.database_name};UID={self.uid};PWD={self.pwd};')
        # Connection to the database with Windows authentication
        conn = pyodbc.connect(f'Driver={{SQL Server Native Client 11.0}};Server={self.server_name};Database={self.database_name};Trusted_Connection=yes;')

        cursor = conn.cursor()

        # Query to search the table students_info
        query = "SELECT * FROM students_info WHERE faculty = ? AND Course = ?"
        params = (self.faculty_combo.currentText(), self.course_combo.currentText())
        cursor.execute(query, params)

        # Create results table
        self.table_widget.setColumnCount(len(cursor.description))
        self.table_widget.setRowCount(0)
        self.table_widget.setHorizontalHeaderLabels([column[0] for column in cursor.description])

        # Populate table with search results
        for row_idx, row_data in enumerate(cursor.fetchall()):
            self.table_widget.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        self.table_widget.resizeColumnsToContents()

        conn.close()

    def search_data_df(self):
        search_text = self.search_edit.text()

        # Iterate through all table rows to hide those that do not contain the search text
        for row in range(self.table_widget.rowCount()):
            row_hidden = True
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item is not None and search_text.lower() in item.text().lower():
                    row_hidden = False
                    break
            self.table_widget.setRowHidden(row, row_hidden)

    def search_data_db(self):
        search_text = self.search_edit.text()
        search_date_satrt = self.date_edit_start.date().toString("yyyy-MM-dd")
        search_date_end = self.date_edit_end.date().toString("yyyy-MM-dd")

        # Connection to the database with login uid and pwd
        # try:
        #     conn = pyodbc.connect(f'Driver={{SQL Server Native Client 11.0}};Server={self.server_name};Database={self.database_name};UID={self.uid};PWD={self.pwd};')
        #     cursor = conn.cursor()
        # Connection to the database with Windows authentication
        try:
            conn = pyodbc.connect(f'Driver={{SQL Server Native Client 11.0}};Server={self.server_name};Database={self.database_name};Trusted_Connection=yes;')

            cursor = conn.cursor()

        except pyodbc.Error as e:
        # Handle the exception
            error_msg = f"Error during database connection: {str(e)}"
            QMessageBox.critical(self, "Connection Error", error_msg)

        # Query to search the table students_info
        query = "SELECT * FROM students_info WHERE (LOWER(faculty) LIKE ? OR LOWER(Course) LIKE ? OR LOWER(FirstName) LIKE ? OR LOWER(LastName) LIKE ?) AND DateOfBirth >= ? and DateOfBirth <= ? ORDER BY DateOfBirth DESC"
        params = ['%' + search_text.lower() + '%'] * 4 + [search_date_satrt] + [search_date_end]

        # Query to search only the name field and the date
        # query = "SELECT * FROM students_info WHERE ( LOWER(FirstName) LIKE ? ) AND DateOfBirth >= ? and DateOfBirth <= ? ORDER BY DateOfBirth DESC"
        # params = ['%' + search_text.lower() + '%'] * 1 + [search_date_satrt] + [search_date_end]

        cursor.execute(query, params)

        # Fetch all results and save them in a variable
        results = cursor.fetchall()

        # Check if there are results
        if not results:
            QMessageBox.information(self, "Result", "No results found.")
            return

        # Create results table
        self.table_widget.setColumnCount(len(cursor.description))
        self.table_widget.setRowCount(0)
        self.table_widget.setHorizontalHeaderLabels([column[0] for column in cursor.description])

        # Populate table with search results
        for row_idx, row_data in enumerate(results):
            self.table_widget.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        # Resize table columns to fit content
        self.table_widget.resizeColumnsToContents()

    def handleQuit(self):
        reply = QMessageBox.question(self, 'Exit Confirmation',
                                     "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
