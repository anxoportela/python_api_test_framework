import pytest
import time
import config
from core.api_client import APIClient
from core.db_manager import DBManager
from core.excel_reader import ExcelReader
from core.excel_writer import ExcelWriter


@pytest.fixture(scope="module")
def test_data():
    """
    Carga los datos de prueba desde un archivo Excel y los valida. Si no se encuentran datos en el archivo,
    se marca la prueba como fallida.

    Retorna:
        list: Lista de casos de prueba cargados desde el archivo Excel.
    """
    reader = ExcelReader(config.EXCEL_PATH)  # Inicializa el lector de Excel
    data = reader.load_data()  # Carga los datos desde la hoja "TestSuite"

    if not data:  # Si no se encontraron datos, falla el test
        pytest.fail("No se encontraron datos en el archivo Excel.")

    return data  # Retorna los datos cargados


def prepare_headers_and_auth(test_case):
    """
    Prepara los encabezados HTTP y la autenticación según los datos del caso de prueba.

    Args:
        test_case (APIData): Caso de prueba que contiene los detalles de la solicitud.

    Returns:
        tuple: Un diccionario con los encabezados y un valor de autenticación (None o tupla de usuario y contraseña).
    """
    if test_case.Authorization:
        # Si hay un token de autorización, se añade al encabezado
        headers = test_case.Headers if test_case.Headers else {}
        headers['Authorization'] = test_case.Authorization
        auth = None
    elif test_case.User and test_case.Password:
        # Si hay usuario y contraseña, se configura la autenticación básica
        headers = test_case.Headers if test_case.Headers else {}
        auth = (test_case.User, test_case.Password)
    else:
        # Si no hay ninguna de las opciones anteriores, solo se devuelven los encabezados
        headers = test_case.Headers if test_case.Headers else {}
        auth = None

    return headers, auth


def send_request_and_measure_time(client, test_case, headers, auth):
    """
    Envía una solicitud HTTP utilizando el cliente de la API y mide el tiempo de ejecución.

    Args:
        client (APIClient): Instancia del cliente de la API.
        test_case (APIData): Caso de prueba con los parámetros necesarios para la solicitud.
        headers (dict): Encabezados HTTP a incluir en la solicitud.
        auth (tuple or None): Información de autenticación, si es necesario.

    Returns:
        tuple: La respuesta de la API, el tiempo de duración de la solicitud y el tamaño de la respuesta.
    """
    start_time = time.time()  # Captura el tiempo antes de la solicitud
    try:
        # Realiza la solicitud HTTP usando los parámetros proporcionados
        response = client.send_request(
            test_case.Method,
            test_case.URL,
            test_case.Endpoint,
            headers=headers,
            body=test_case.Body,
            auth=auth
        )
    except Exception as e:
        pytest.fail(f"API request failed: {e}")  # Si hay un error, falla el test

    end_time = time.time()  # Captura el tiempo después de la solicitud
    duration = end_time - start_time  # Calcula la duración de la solicitud
    response_size = len(response.text)  # Calcula el tamaño de la respuesta

    return response, duration, response_size


def check_response(response, test_case):
    """
    Verifica la respuesta de la API comparando el código de estado y el cuerpo de la respuesta con las expectativas.

    Args:
        response (Response): Respuesta de la API obtenida.
        test_case (APIData): Caso de prueba con los valores esperados.

    Returns:
        tuple: El estado de la prueba ("PASSED" o "FAILED") y un mensaje de error, si corresponde.
    """
    if response.status_code == test_case.ExpectedStatusCode:
        # Si el código de estado es el esperado, la prueba pasa
        status = "PASSED"
        error = None
    else:
        # Si el código de estado no es el esperado, la prueba falla
        status = "FAILED"
        error = f"Expected status code: {test_case.ExpectedStatusCode}, Got: {response.status_code}"

    try:
        # Compara la respuesta con la esperada
        response_body = response.json() if 'application/json' in response.headers.get('Content-Type',
                                                                                      '') else response.text
        if response_body != test_case.ExpectedResponse:
            status = "FAILED"
            error = f"Expected response: {test_case.ExpectedResponse}, Got: {response_body}"
    except ValueError as e:
        status = "FAILED"
        error = f"Failed to parse response: {str(e)}"

    return status, error


def test_api(test_data):
    """
    Función principal que ejecuta las pruebas API según los datos de prueba cargados desde un archivo Excel.

    Esta función se encarga de realizar las solicitudes a la API, verificar los resultados, guardar los resultados
    en una base de datos y generar un resumen de las pruebas ejecutadas.

    Args:
        test_data (list): Lista de datos de prueba cargados desde un archivo Excel.
    """
    client = APIClient()  # Crea una instancia del cliente de la API
    db_manager = DBManager(config.DB_PATH)  # Crea una instancia del gestor de base de datos
    db_manager.create_tables()  # Crea las tablas necesarias en la base de datos

    # Inserta la ejecución de prueba en la base de datos
    execution_name = f"TestExecution_{time.strftime('%Y%m%d_%H%M%S')}"
    execution_id = db_manager.insert_test_execution(execution_name)
    if not execution_id:
        pytest.fail("No se pudo crear la ejecución en la base de datos.")

    durations = []  # Lista para almacenar la duración de cada prueba
    response_sizes = []  # Lista para almacenar el tamaño de la respuesta de cada prueba
    results = []  # Lista para almacenar los resultados de las pruebas

    for test_case in test_data:
        if test_case.Run == "N":  # Si la prueba está marcada como no ejecutarse, se marca como saltada
            status = "SKIPPED"
            error = "Test skipped (Run = N)"
        else:
            # Prepara los encabezados y autenticación para la solicitud
            headers, auth = prepare_headers_and_auth(test_case)

            # Envía la solicitud y mide el tiempo
            response, duration, response_size = send_request_and_measure_time(client, test_case, headers, auth)

            # Verifica la respuesta recibida
            status, error = check_response(response, test_case)

        # Guarda el resultado de la prueba en la base de datos
        result = {
            "TestId": test_case.TestId,
            "TestCase": test_case.TestCase,
            "Status": status,
            "Error": error,
            "Method": test_case.Method,
            "URL": test_case.URL,
            "Endpoint": test_case.Endpoint,
            "ExpectedStatusCode": test_case.ExpectedStatusCode,
            "ActualStatusCode": response.status_code if status != "SKIPPED" else None,
            "Duration": duration if status != "SKIPPED" else None,
            "ResponseSize": response_size if status != "SKIPPED" else None
        }

        db_manager.insert_test_result(execution_id, result)  # Inserta el resultado en la base de datos

        durations.append(duration)
        response_sizes.append(response_size)
        results.append(result)

    # Inserta el resumen de las pruebas en la base de datos
    summary = {
        "TotalTests": len(test_data),
        "PassedTests": sum(1 for r in results if r['Status'] == "PASSED"),
        "FailedTests": sum(1 for r in results if r['Status'] == "FAILED"),
        "SkippedTests": sum(1 for r in results if r['Status'] == "SKIPPED"),
        "AvgDuration": sum(durations) / len(durations) if durations else 0,
        "TotalResponseSize": sum(response_sizes),
    }

    db_manager.insert_test_summary(execution_id, summary)

    # Imprime un resumen de la ejecución de pruebas
    print("\n--- Resumen de la Ejecución de Pruebas ---")
    print(f"Total de pruebas: {summary['TotalTests']}")
    print(f"Pruebas pasadas: {summary['PassedTests']}")
    print(f"Pruebas falladas: {summary['FailedTests']}")
    print(f"Pruebas saltadas: {summary['SkippedTests']}")
    print(f"Duración promedio: {summary['AvgDuration']:.2f} segundos")
    print(f"Tamaño total de respuestas: {summary['TotalResponseSize']} bytes")

    # Actualiza los resultados en el archivo Excel
    ExcelWriter(config.EXCEL_PATH).update_results(results, execution_name)
