## 🐍 **Framework de Pruebas de API en Python** 🚀

[![Español](https://img.shields.io/badge/Language-Spanish-red)](README.es.md)
[![English](https://img.shields.io/badge/Language-English-blue)](README.md)

Bienvenido! Escoge tu lenguaje preferido.

### 🌟 **Descripción del Proyecto**

¡Bienvenido al **Framework de Pruebas de API en Python**! Esta es una solución todo en uno para automatizar las pruebas de API, gestionar datos de prueba y generar informes interactivos. Construido con Python y varias bibliotecas modernas, este framework te permite:

- **Probar** APIs RESTful.
- **Gestionar** los datos de prueba desde archivos Excel.
- **Almacenar** los resultados en una base de datos (SQLite).
- **Visualizar** los resultados de las pruebas con un panel de control basado en dash.

---

### ⚙️ **Características**

✨ **Características clave**:

- 🧑‍💻 **Cliente de API**: Envía solicitudes HTTP (GET, POST, PUT, DELETE) para probar las APIs.
- 📊 **Lector y Escritor de Excel**: Lee los datos de prueba desde archivos `.xlsx` y escribe los resultados de vuelta en Excel.
- 🗃️ **Gestor de Base de Datos**: Almacena los resultados de las pruebas en una base de datos SQLite.
- 📈 **Panel de Informes de Pruebas**: Muestra los resultados en una aplicación web basada en Dash.
- 📅 **Informes Complejos**:
  - **Resumen de Ejecución**: Pruebas Pasadas, Falladas y Saltadas.
  - **Distribución de Estados**: Visualiza la distribución de los estados de las pruebas.
  - **Histogramas de Duración**: Muestra la distribución de las duraciones de las pruebas.
  - **Tabla de Resultados**: Proporciona un registro detallado de los resultados de las pruebas.

---

### 🚀 **Instalación**

#### **1. Instalar Dependencias**

El framework requiere Python 3.12+ y varias dependencias. Para comenzar, clona el repositorio e instala los paquetes necesarios desde el archivo `requirements.txt`.

```bash
git clone https://github.com/anxoportela/python_api_test_framework.git
cd python-api-test-framework
```

#### **2. Configurar un Entorno Virtual (opcional, pero recomendado)**

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows usa venv\Scripts\activate
```

#### **3. Instalar las Dependencias Requeridas**

```bash
pip install -r requirements.txt
```

---

### 🧪 **Ejecutar Pruebas**

Antes de lanzar el panel de Dash, es importante ejecutar las pruebas para generar los datos que se visualizarán.

Para ejecutar las pruebas del framework, navega hasta el directorio raíz y ejecuta lo siguiente:

```bash
pytest -s
```

Esto ejecutará las pruebas y proporcionará retroalimentación sobre el éxito de los casos de prueba.

---

### 🚀 **Lanzar el Panel de Control de Dash** 💻

Una vez que las pruebas se han ejecutado y los resultados se han generado, puedes lanzar el panel de informes basado en Dash. Este mostrará los resultados de tus pruebas en una interfaz web interactiva.

```bash
python web/app.py
```

Abre tu navegador y accede a `http://127.0.0.1:8050/` para ver el panel.

---

### 📊 **Formato de los Datos de Prueba** (Excel)

El framework lee los datos de prueba desde un archivo Excel (`test_data.xlsx`) con las siguientes columnas en orden:

| Nombre de Columna      | Descripción                                                         |
|------------------------|---------------------------------------------------------------------|
| **TestId**             | Identificador único del caso de prueba.                             |
| **TestCase**           | Nombre o descripción del caso de prueba.                            |
| **Run**                | Indica si la prueba debe ejecutarse (`Y`/`N`).                      |
| **Method**             | Método HTTP a utilizar (GET, POST, PUT, DELETE).                    |
| **URL**                | La URL base de la API que se está probando.                         |
| **Endpoint**           | El endpoint específico a probar, relativo a la URL base.            |
| **Authorization**      | Cadena de autorización requerida (ej., `Bearer`, `Basic` o `None`). |
| **User**               | Nombre de usuario (si es necesario para la autenticación).          |
| **Password**           | Contraseña (si es necesario para la autenticación).                 |
| **Headers**            | Cabeceras HTTP en formato JSON (opcional).                          |
| **Body**               | Cuerpo de la solicitud en formato JSON (para peticiones POST/PUT).  |
| **ExpectedStatusCode** | El código de estado HTTP esperado (ej., `200`, `404`).              |
| **ExpectedResponse**   | El cuerpo de la respuesta esperado (opcional, puede estar vacío).   |
| **Status**             | El resultado de la prueba (`Passed`, `Failed` o `Skipped`).         |
| **Error**              | Cualquier mensaje de error encontrado durante la prueba (opcional). |

---

#### 🧑‍💻 **Cómo se Usan los Datos de Prueba**

- **TestCase**: La descripción del caso de prueba se registra para mayor claridad.
- **Run**: Esta columna determina si el caso de prueba debe ejecutarse. Si `Run` está establecido en `N`, la prueba se omite.
- **Method**: Define el método de solicitud HTTP a utilizar (ej., `GET`, `POST`).
- **URL + Endpoint**: Combinados, estos forman la URL completa para la solicitud. La URL base y el `Endpoint` específico se unirán programáticamente.
- **Authorization, User, Password**: Se utilizan para solicitudes autenticadas (ej., con tokens Bearer o Autenticación Básica).
- **Headers & Body**: Si es necesario, las cabeceras HTTP y los cuerpos de las solicitudes se envían como parte de la llamada a la API.
- **ExpectedStatusCode & ExpectedResponse**: La respuesta real se compara con estos valores para determinar si la prueba pasa o falla.
- **Status**: Después de cada ejecución de prueba, esta columna se actualiza con el resultado de la prueba.
- **Error**: Si la prueba falla o ocurre un error, el mensaje de error se registra aquí para un análisis posterior.

---

### 📁 **Estructura del Proyecto**

```bash
python_api_test_framework/
│
├── core/                    # Lógica para solicitudes API y gestión de datos de prueba
│   ├── __init__.py          # Inicialización del paquete principal
│   ├── api_client.py        # Maneja las solicitudes de API
│   ├── excel_reader.py      # Lee los datos de prueba desde archivos Excel
│   ├── excel_writer.py      # Escribe los resultados de las pruebas en archivos Excel
│   ├── test_data_model.py   # Define el modelo de datos de prueba
│   ├── db_manager.py        # Maneja las interacciones con la base de datos
│
├── data/                    # Almacena los datos de prueba
│   ├── __init__.py          # Inicialización del paquete de datos
│   ├── test_data.xlsx       # Datos de prueba de ejemplo
│
├── reports/                 # Almacena los informes generados y los resultados de las pruebas
│   ├── __init__.py          # Inicialización del paquete de informes
│   ├── results.db           # Base de datos SQLite para los resultados de las pruebas
│
├── tests/                   # Pruebas unitarias y funcionales para el framework
│   ├── __init__.py          # Inicialización del paquete de pruebas
│   └── test_api.py          # Lanzador de pruebas para el framework
│
├── web/                     # Aplicación web para los informes de pruebas
│   ├── __init__.py          # Inicialización del paquete web
│   ├── app.py               # Aplicación Dash para visualizar los informes de pruebas
│
├── config.py                # Configuración global del proyecto
├── requirements.txt         # Lista de dependencias necesarias
├── LICENSE                  # Licencia del proyecto
├── README.es.md             # Estás aquí ahora mismo 😅
├── README.md                # README en Inglés
```

---

### 🛠️ **Cómo Funciona**

#### 📡 **Cliente de API**

El archivo `api_client.py` maneja las solicitudes y respuestas de la API. Soporta varios métodos HTTP (GET, POST, PUT, DELETE) y almacena los resultados, incluidos los códigos de estado y los tiempos de respuesta.

#### 📂 **Gestión de Datos de Prueba**

Los datos de prueba se leen desde un archivo Excel (`test_data.xlsx`) utilizando el script `excel_reader.py`. Estos datos incluyen típicamente los endpoints de la API, los métodos de solicitud y los resultados esperados. Después de ejecutar las pruebas, los resultados se escriben de nuevo en una nueva hoja del Excel utilizando `excel_writer.py`.

#### 🗄️ **Gestión de Base de Datos**

Los resultados de las pruebas se guardan en una base de datos SQLite (`results.db`). El archivo `db_manager.py` se encarga de insertar y recuperar los resultados de las pruebas.

#### 📊 **Panel de Informes**

El archivo `web/app.py` sirve como punto de entrada para el panel web basado en Dash. Este panel proporciona una vista completa de los resultados de las pruebas, incluyendo:

- **Estadísticas de Pruebas**: Resumen de las pruebas que pasaron, fallaron y fueron omitidas.
- **Gráficos**:
  - **Distribución de Estados**: Muestra un gráfico de barras de los estados de las pruebas (Aprobadas, Fallidas, Omitidas).
  - **Distribución de Duraciones**: Visualiza la distribución de las duraciones de las pruebas.
  - **Tabla de Resultados**: Una tabla detallada de los resultados individuales de las pruebas, que incluye el estado, la duración y registros adicionales.

---

### 📍 Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama para tu feature o bugfix (`git checkout -b feature/nueva-feature`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`).
4. Sube tus cambios a tu fork (`git push origin feature/nueva-feature`).
5. Crea un pull request.

---

### 📄 **Licencia**

Este proyecto está bajo la **Licencia MIT**. Para más detalles, consulta el archivo [LICENSE](LICENSE).

---

### 📧 **Contacto**

Para cualquier problema, pregunta o sugerencia, no dudes en contactar con los mantenedores del proyecto:

**Correo electrónico**: [hello@anxoportela.dev](mailto:hello@anxoportela.dev)

---

#### 🎉 **¡Disfruta utilizando el Framework de Pruebas de API en Python!** 🎉
