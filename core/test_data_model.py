from typing import Optional
from pydantic import BaseModel


class APIData(BaseModel):
    """
    Modelo de datos para representar los resultados y parámetros de una prueba API.

    Este modelo se utiliza para validar los datos de las pruebas API, asegurando que todos los campos
    estén presentes con los tipos correctos. Además, proporciona validación automática de los datos.
    """

    TestId: str
    """
    Identificador único de la prueba.

    Tipo: str
    """

    TestCase: str
    """
    Nombre o descripción del caso de prueba.

    Tipo: str
    """

    Run: str
    """
    Indica si la prueba debe ejecutarse o no (Y/N).

    Tipo: str
    """

    Method: str
    """
    Método HTTP utilizado en la prueba (por ejemplo, 'GET', 'POST', 'PUT', 'DELETE').

    Tipo: str
    """

    URL: str
    """
    URL base de la API donde se enviará la solicitud.

    Tipo: str
    """

    Endpoint: str
    """
    Ruta o endpoint de la API donde se realizará la prueba.

    Tipo: str
    """

    Authorization: Optional[str] = None
    """
    Información de autorización, como un token o una clave API, si es necesario.

    Tipo: Optional[str]
    Valor por defecto: None
    """

    User: Optional[str] = None
    """
    Nombre de usuario para la autenticación si es necesario.

    Tipo: Optional[str]
    Valor por defecto: None
    """

    Password: Optional[str] = None
    """
    Contraseña asociada al nombre de usuario para la autenticación.

    Tipo: Optional[str]
    Valor por defecto: None
    """

    Headers: Optional[dict] = None
    """
    Encabezados HTTP adicionales que se incluirán en la solicitud (por ejemplo, Content-Type, Authorization).

    Tipo: Optional[dict]
    Valor por defecto: None
    """

    Body: Optional[dict] = None
    """
    Cuerpo de la solicitud, utilizado para enviar datos en métodos como POST o PUT.

    Tipo: Optional[dict]
    Valor por defecto: None
    """

    ExpectedStatusCode: int
    """
    Código de estado HTTP esperado en la respuesta (por ejemplo, 200, 404, 500).

    Tipo: int
    """

    ExpectedResponse: Optional[dict] = None
    """
    Respuesta esperada en formato JSON. Esta es la estructura que debería tener la respuesta de la API.

    Tipo: Optional[dict]
    Valor por defecto: None
    """

    Status: Optional[str] = None
    """
    Estado de la prueba, indicando si pasó, falló o fue saltada (por ejemplo, 'PASSED', 'FAILED', 'SKIPPED').

    Tipo: Optional[str]
    Valor por defecto: None
    """

    Error: Optional[str] = None
    """
    Mensaje de error en caso de que la prueba haya fallado, proporcionando detalles sobre el problema encontrado.

    Tipo: Optional[str]
    Valor por defecto: None
    """
