import sqlite3

class DBManager:
    """
    A class to manage interactions with an SQLite database for storing test execution results.

    This class provides methods to:
    - Connect to the SQLite database.
    - Create necessary tables to store test execution data.
    - Insert individual test results, test execution summaries, and test execution metadata.

    Attributes:
        db_file (str): The path to the SQLite database file.
    """

    def __init__(self, db_file):
        """
        Initializes the DBManager with the path to the SQLite database file.

        Args:
            db_file (str): Path to the SQLite database file.
        """
        self.db_file = db_file

    def _connect(self):
        """
        Establishes and returns a connection to the SQLite database.

        Returns:
            sqlite3.Connection: The database connection object.
        """
        return sqlite3.connect(self.db_file)

    def create_tables(self):
        """
        Creates the necessary tables in the database for storing test execution data.

        The following tables will be created if they don't exist:
            - test_executions: Stores metadata about test execution (e.g., execution name, date).
            - test_results: Stores detailed results of each test run, including status, method, response details.
            - test_summary: Stores aggregated summary information about the test execution (e.g., total tests, passed, failed).

        If the tables already exist, this method will do nothing.
        """
        try:
            with self._connect() as conn:
                c = conn.cursor()

                # Create the 'test_executions' table if it doesn't exist
                c.execute('''CREATE TABLE IF NOT EXISTS test_executions (
                            ExecutionId INTEGER PRIMARY KEY AUTOINCREMENT,
                            ExecutionName TEXT NOT NULL,
                            ExecutionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')

                # Create the 'test_results' table if it doesn't exist
                c.execute('''CREATE TABLE IF NOT EXISTS test_results (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ExecutionId INTEGER,  -- Foreign key referencing 'test_executions'
                            TestId TEXT,
                            TestCase TEXT,
                            Status TEXT,
                            Error TEXT,
                            Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            Method TEXT,
                            URL TEXT,
                            Endpoint TEXT,
                            ExpectedStatusCode INT,
                            ActualStatusCode INT,
                            Duration REAL,
                            ResponseSize INT,
                            FOREIGN KEY (ExecutionId) REFERENCES test_executions(ExecutionId)
                        )''')

                # Create the 'test_summary' table if it doesn't exist
                c.execute('''CREATE TABLE IF NOT EXISTS test_summary (
                            ExecutionId INTEGER PRIMARY KEY,
                            TotalTests INT,
                            PassedTests INT,
                            FailedTests INT,
                            AvgDuration REAL,
                            TotalResponseSize INT,
                            FOREIGN KEY (ExecutionId) REFERENCES test_executions(ExecutionId)
                        )''')

        except Exception as e:
            print(f"Error creating tables: {e}")

    def insert_test_result(self, execution_id, test_result):
        """
        Inserts a test result into the 'test_results' table.

        Args:
            execution_id (int): The ID of the test execution (foreign key from 'test_executions').
            test_result (dict): A dictionary containing the test case data to be inserted,
                                including test ID, status, method, response size, etc.
        """
        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('''INSERT INTO test_results
                            (ExecutionId, TestId, TestCase, Status, Error, Method, URL, Endpoint,
                             ExpectedStatusCode, ActualStatusCode, Duration, ResponseSize)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (execution_id, test_result['TestId'], test_result['TestCase'],
                           test_result['Status'], test_result['Error'], test_result['Method'],
                           test_result['URL'], test_result['Endpoint'], test_result['ExpectedStatusCode'],
                           test_result['ActualStatusCode'], test_result['Duration'],
                           test_result['ResponseSize']))
        except Exception as e:
            print(f"Error inserting test result: {e}")

    def insert_test_summary(self, execution_id, summary):
        """
        Inserts a test summary into the 'test_summary' table.

        Args:
            execution_id (int): The ID of the test execution (foreign key from 'test_executions').
            summary (dict): A dictionary containing the aggregated test execution summary data,
                            including total tests, passed tests, failed tests, average duration, and total response size.
        """
        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('''INSERT INTO test_summary
                            (ExecutionId, TotalTests, PassedTests, FailedTests, AvgDuration, TotalResponseSize)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                          (execution_id, summary['TotalTests'], summary['PassedTests'], summary['FailedTests'],
                           summary['AvgDuration'], summary['TotalResponseSize']))
        except Exception as e:
            print(f"Error inserting test summary: {e}")

    def insert_test_execution(self, execution_name):
        """
        Inserts a new test execution entry into the 'test_executions' table.

        Args:
            execution_name (str): The name or identifier of the test execution.

        Returns:
            int: The ID of the newly inserted test execution, or None if the insert failed.
        """
        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('''INSERT INTO test_executions (ExecutionName) VALUES (?)''', (execution_name,))
                return c.lastrowid  # Return the ID of the last inserted row
        except Exception as e:
            print(f"Error inserting test execution: {e}")
            return None
