import requests
from requests.exceptions import RequestException


class APIClient:
    """
    Clase para gestionar las solicitudes HTTP a una API externa.
    Esta clase proporciona un método estático para enviar peticiones HTTP de forma flexible,
    permitiendo especificar el método HTTP, la URL, los encabezados, el cuerpo de la solicitud y la autenticación.
    """

    @staticmethod
    def send_request(method, url, endpoint, headers=None, body=None, auth=None):
        """
        Envía una solicitud HTTP a una API externa.

        Parámetros:
        - method (str): El método HTTP a utilizar (por ejemplo, 'GET', 'POST', etc.).
        - url (str): La URL base del API.
        - endpoint (str): El endpoint específico que se añadirá a la URL base.
        - headers (dict, opcional): Los encabezados HTTP que se incluirán en la solicitud. Por defecto es None.
        - body (dict, opcional): El cuerpo de la solicitud, utilizado en métodos como 'POST' o 'PUT'. Por defecto es None.
        - auth (tuple, opcional): Los detalles de autenticación en formato (usuario, contraseña). Por defecto es None.

        Retorna:
        - dict: El objeto de respuesta de la solicitud. Si la solicitud es exitosa, devuelve el objeto `response`.
        - dict: En caso de error, devuelve un diccionario con la clave 'error' y el mensaje del error.
        """
        try:
            # Se forma la URL completa concatenando la URL base y el endpoint
            full_url = f"{url}{endpoint}"

            # Realiza la solicitud HTTP utilizando el método indicado
            response = requests.request(
                method=method,  # Método HTTP (GET, POST, etc.)
                url=full_url,  # URL completa
                headers=headers,  # Encabezados de la solicitud, en formato JSON
                json=body,  # Cuerpo de la solicitud, en formato JSON
                auth=auth,  # Datos de autenticación
            )

            # Retorna la respuesta de la solicitud
            return response

        except RequestException as e:
            # Si ocurre un error durante la solicitud, devuelve un diccionario con el error
            return {"error": f"La solicitud falló: {e}"}
