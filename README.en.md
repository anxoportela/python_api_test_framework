## 🐍 **API Testing Framework in Python** 🚀

[![Español](https://img.shields.io/badge/Language-Spanish-red)](README.md)
[![English](https://img.shields.io/badge/Language-English-blue)](README.en.md)

Welcome! Choose your preferred language.

### 🌟 **Project Description**

Welcome to the **API Testing Framework in Python**! This is an all-in-one solution for automating API tests, managing test data, and generating interactive reports. Built with Python and several modern libraries, this framework allows you to:

- **Test** RESTful APIs.
- **Manage** test data from Excel files.
- **Store** results in a database (SQLite).
- **Visualize** test results with a Dash-based dashboard.

---

### ⚙️ **Features**

✨ **Key Features**:

- 🧑‍💻 **API Client**: Sends HTTP requests (GET, POST, PUT, DELETE) to test APIs.
- 📊 **Excel Reader and Writer**: Reads test data from `.xlsx` files and writes test results back to Excel.
- 🗃️ **Database Manager**: Stores test results in an SQLite database.
- 📈 **Test Report Dashboard**: Displays test results in a Dash-based web application.
- 📅 **Advanced Reports**:
  - **Execution Summary**: Passed, Failed, and Skipped Tests.
  - **Status Distribution**: Visualize the distribution of test statuses.
  - **Duration Histograms**: Shows the distribution of test durations.
  - **Results Table**: Provides a detailed log of test results.

---

### 🚀 **Installation**

#### **1. Install Dependencies**

The framework requires Python 3.12+ and several dependencies. To get started, clone the repository and install the necessary packages from the `requirements.txt` file.

```bash
git clone https://github.com/anxoportela/python_api_test_framework.git
cd python-api-test-framework
```

#### **2. Set Up a Virtual Environment (optional, but recommended)**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

#### **3. Install the Required Dependencies**

```bash
pip install -r requirements.txt
```

---

### 🧪 **Running Tests**

Before launching the Dash dashboard, it’s important to run the tests to generate the data that will be displayed.

To run the framework’s tests, navigate to the root directory and execute the following:

```bash
pytest -s
```

This will execute the tests and provide feedback on the success of the test cases.

---

### 🚀 **Launch the Dash Dashboard** 💻

Once the tests have been executed and results generated, you can launch the Dash-based report dashboard. This will show the results of your tests in an interactive web interface.

```bash
python web/app.py
```

Open your browser and go to `http://127.0.0.1:8050/` to view the dashboard.

---

### 📊 **Test Data Format** (Excel)

The framework reads test data from an Excel file (`test_data.xlsx`) with the following columns in order:

| Column Name            | Description                                                          |
|------------------------|----------------------------------------------------------------------|
| **TestId**             | Unique identifier for the test case.                                 |
| **TestCase**           | Name or description of the test case.                                |
| **Run**                | Indicates if the test should be executed (`Y`/`N`).                   |
| **Method**             | HTTP method to use (GET, POST, PUT, DELETE).                         |
| **URL**                | The base URL of the API being tested.                                |
| **Endpoint**           | The specific endpoint to test, relative to the base URL.             |
| **Authorization**      | Required authorization string (e.g., `Bearer`, `Basic`, or `None`).  |
| **User**               | Username (if needed for authentication).                             |
| **Password**           | Password (if needed for authentication).                            |
| **Headers**            | HTTP headers in JSON format (optional).                              |
| **Body**               | Request body in JSON format (for POST/PUT requests).                  |
| **ExpectedStatusCode** | The expected HTTP status code (e.g., `200`, `404`).                  |
| **ExpectedResponse**   | The expected response body (optional, can be empty).                 |
| **Status**             | The result of the test (`Passed`, `Failed`, or `Skipped`).           |
| **Error**              | Any error message encountered during the test (optional).           |

---

#### 🧑‍💻 **How to Use Test Data**

- **TestCase**: The test case description is recorded for clarity.
- **Run**: This column determines whether the test case should be executed. If `Run` is set to `N`, the test will be skipped.
- **Method**: Defines the HTTP request method to use (e.g., `GET`, `POST`).
- **URL + Endpoint**: Together, these form the complete URL for the request. The base URL and specific `Endpoint` will be combined programmatically.
- **Authorization, User, Password**: These are used for authenticated requests (e.g., with Bearer tokens or Basic Authentication).
- **Headers & Body**: If necessary, HTTP headers and request bodies are sent as part of the API call.
- **ExpectedStatusCode & ExpectedResponse**: The actual response is compared against these values to determine whether the test passes or fails.
- **Status**: After each test execution, this column is updated with the result of the test.
- **Error**: If the test fails or an error occurs, the error message is logged here for further analysis.

---

### 📁 **Project Structure**

```bash
python_api_test_framework/
│
├── core/                    # Logic for API requests and test data management
│   ├── __init__.py          # Initialization of the main package
│   ├── api_client.py        # Handles API requests
│   ├── excel_reader.py      # Reads test data from Excel files
│   ├── excel_writer.py      # Writes test results to Excel files
│   ├── test_data_model.py   # Defines the test data model
│   ├── db_manager.py        # Manages database interactions
│
├── data/                    # Stores test data
│   ├── __init__.py          # Initialization of the data package
│   ├── test_data.xlsx       # Sample test data
│
├── reports/                 # Stores generated reports and test results
│   ├── __init__.py          # Initialization of the reports package
│   ├── results.db           # SQLite database for test results
│
├── tests/                   # Unit and functional tests for the framework
│   ├── __init__.py          # Initialization of the tests package
│   └── test_api.py          # Test launcher for the framework
│
├── web/                     # Web application for test reports
│   ├── __init__.py          # Initialization of the web package
│   ├── app.py               # Dash application to view test reports
│
├── config.py                # Global project configuration
├── requirements.txt         # List of required dependencies
├── LICENSE                  # Project license
├── README.md                # README file in Spanish
├── README.en.md             # You're here right now 😅
```

---

### 🛠️ **How It Works**

#### 📡 **API Client**

The `api_client.py` file handles the API requests and responses. It supports various HTTP methods (GET, POST, PUT, DELETE) and stores results, including status codes and response times.

#### 📂 **Test Data Management**

Test data is read from an Excel file (`test_data.xlsx`) using the `excel_reader.py` script. This data typically includes API endpoints, request methods, and expected results. After the tests are executed, the results are written back into a new sheet in the Excel file using `excel_writer.py`.

#### 🗄️ **Database Management**

Test results are stored in an SQLite database (`results.db`). The `db_manager.py` file handles inserting and retrieving test results.

#### 📊 **Report Dashboard**

The `web/app.py` file serves as the entry point for the Dash-based web dashboard. This dashboard provides a comprehensive view of test results, including:

- **Test Stats**: Summary of tests that passed, failed, or were skipped.
- **Graphs**:
  - **Status Distribution**: Shows a bar chart of test statuses (Passed, Failed, Skipped).
  - **Duration Distribution**: Visualizes the distribution of test durations.
  - **Results Table**: A detailed table of individual test results, including status, duration, and additional logs.

---

### 📍 **Contributing**

Contributions are welcome! If you want to contribute to this project, please follow these steps:

1. Fork the project.
2. Create a new branch for your feature or bugfix (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push your changes to your fork (`git push origin feature/new-feature`).
5. Create a pull request.

---

### 📄 **License**

This project is licensed under the **MIT License**. For more details, see the [LICENSE](LICENSE) file.

---

### 📧 **Contact**

For any issues, questions, or suggestions, feel free to reach out to the project maintainers:

**Email**: [hello@anxoportela.dev](mailto:hello@anxoportela.dev
