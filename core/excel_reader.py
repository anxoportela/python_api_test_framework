import pandas as pd
import json
from core.test_data_model import APIData


def _convert_to_dict(value):
    """
    Convierte una cadena JSON a un diccionario. Si la cadena está vacía o no es un JSON válido,
    devuelve un diccionario vacío.

    Parámetros:
    - value (str): Cadena que se intentará convertir a un diccionario.

    Retorna:
    - dict: El diccionario resultante si la conversión es exitosa, o un diccionario vacío en caso de error o si la cadena está vacía.
    """
    if isinstance(value, str) and value:
        try:
            # Si la cadena no es '{}' (un diccionario vacío), la intentamos convertir
            if value != '{}':
                return json.loads(value)
            else:
                return {}
        except json.JSONDecodeError:
            # Si ocurre un error en la conversión, imprimimos un mensaje de error
            print(f"Error al convertir la cadena a diccionario: {value}")
            return {}
    return {}


def _validate(record):
    """
    Valida un registro utilizando el modelo `APIData`. Si el registro no es válido, se captura la excepción y se imprime un error.

    Parámetros:
    - record (dict): Registro a validar.

    Retorna:
    - bool: `True` si el registro es válido según el modelo `APIData`, `False` en caso contrario.
    """
    try:
        # Se valida el registro creando una instancia de APIData
        APIData(**record)
        return True
    except Exception as e:
        # Si ocurre un error de validación, imprimimos el mensaje de error
        print(f"Validation error: {e}")
        return False


class ExcelReader:
    """
    Clase para leer datos desde un archivo de Excel, procesarlos y convertirlos en registros válidos para pruebas API.

    Esta clase lee una hoja llamada 'TestSuite' y convierte las columnas específicas en diccionarios o listas de diccionarios,
    validando los datos con el modelo `APIData`.
    """

    def __init__(self, file_path):
        """
        Inicializa la clase `ExcelReader` con la ruta del archivo de Excel.

        Parámetros:
        - file_path (str): Ruta al archivo de Excel que se va a procesar.
        """
        self.file_path = file_path

    def load_data(self):
        """
        Lee los datos del archivo de Excel y los procesa para convertirlos en registros válidos.

        Retorna:
        - list: Una lista de instancias de `APIData` que representan los registros válidos de la hoja de Excel.
        Si ocurre un error durante la carga o procesamiento de los datos, retorna una lista vacía.
        """
        try:
            # Leemos la hoja 'TestSuite' del archivo de Excel
            df = pd.read_excel(self.file_path, sheet_name="TestSuite")

            # Rellenamos valores nulos con cadenas vacías
            df = df.fillna('')

            # Convertimos la columna 'TestId' a tipo string
            df['TestId'] = df['TestId'].apply(str)

            # Convertimos las columnas 'Headers', 'Body', y 'ExpectedResponse' de JSON a diccionarios
            df['Headers'] = df['Headers'].apply(_convert_to_dict)
            df['Body'] = df['Body'].apply(_convert_to_dict)
            df['ExpectedResponse'] = df['ExpectedResponse'].apply(_convert_to_dict)

            # Convertimos el DataFrame a una lista de diccionarios
            records = df.to_dict(orient="records")

            # Validamos los registros y los convertimos en instancias de APIData
            validated_data = [APIData(**record) for record in records if _validate(record)]

            return validated_data

        except Exception as e:
            # Si ocurre un error durante la lectura del archivo de Excel, lo imprimimos
            print(f"Error al leer el archivo de Excel: {e}")
            return []
