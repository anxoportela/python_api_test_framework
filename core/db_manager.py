import sqlite3


class DBManager:
    """
    Clase para gestionar las operaciones con una base de datos SQLite.
    Permite crear tablas, insertar resultados de pruebas y resúmenes de ejecución.
    """

    def __init__(self, db_file):
        """
        Inicializa la clase DBManager con el archivo de base de datos proporcionado.

        Parámetros:
        - db_file (str): Ruta al archivo de base de datos SQLite que se va a utilizar.
        """
        self.db_file = db_file

    def _connect(self):
        """
        Establece una conexión con la base de datos.

        Retorna:
        - conn: Conexión a la base de datos SQLite.
        """
        return sqlite3.connect(self.db_file)

    def create_tables(self):
        """
        Crea las tablas necesarias en la base de datos si no existen.
        Estas tablas son:
        - test_executions: Para registrar las ejecuciones de las pruebas.
        - test_results: Para almacenar los resultados de cada prueba individual.
        - test_summary: Para almacenar el resumen de la ejecución de las pruebas.

        Si ocurre algún error durante la creación de las tablas, se muestra un mensaje de error.
        """
        try:
            with self._connect() as conn:
                c = conn.cursor()

                # Creación de la tabla 'test_executions'
                c.execute('''CREATE TABLE IF NOT EXISTS test_executions (
                            ExecutionId INTEGER PRIMARY KEY AUTOINCREMENT,
                            ExecutionName TEXT NOT NULL,
                            ExecutionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')

                # Creación de la tabla 'test_results'
                c.execute('''CREATE TABLE IF NOT EXISTS test_results (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ExecutionId INTEGER,  -- Clave foránea que referencia 'test_executions'
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

                # Creación de la tabla 'test_summary'
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
            print(f"Error al crear las tablas: {e}")

    def insert_test_result(self, execution_id, test_result):
        """
        Inserta un resultado de prueba en la tabla 'test_results'.

        Parámetros:
        - execution_id (int): ID de la ejecución de la prueba correspondiente.
        - test_result (dict): Diccionario que contiene los resultados de la prueba.
          Debe tener las claves: 'TestId', 'TestCase', 'Status', 'Error', 'Method', 'URL',
          'Endpoint', 'ExpectedStatusCode', 'ActualStatusCode', 'Duration', 'ResponseSize'.

        Si ocurre algún error durante la inserción, se muestra un mensaje de error.
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
            print(f"Error al insertar el resultado de la prueba: {e}")

    def insert_test_summary(self, execution_id, summary):
        """
        Inserta un resumen de la ejecución en la tabla 'test_summary'.

        Parámetros:
        - execution_id (int): ID de la ejecución de las pruebas correspondiente.
        - summary (dict): Diccionario que contiene el resumen de la ejecución.
          Debe tener las claves: 'TotalTests', 'PassedTests', 'FailedTests', 'AvgDuration', 'TotalResponseSize'.

        Si ocurre algún error durante la inserción, se muestra un mensaje de error.
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
            print(f"Error al insertar el resumen de la prueba: {e}")

    def insert_test_execution(self, execution_name):
        """
        Inserta una nueva ejecución de prueba en la tabla 'test_executions'.

        Parámetros:
        - execution_name (str): Nombre de la ejecución de la prueba.

        Retorna:
        - int: El ID de la ejecución insertada si la operación es exitosa, o None en caso de error.
        """
        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('''INSERT INTO test_executions (ExecutionName) VALUES (?)''', (execution_name,))
                return c.lastrowid  # Retorna el ID de la última fila insertada (ID de la ejecución)
        except Exception as e:
            print(f"Error al insertar la ejecución de la prueba: {e}")
            return None
