# 🐍 **Python API Test Framework** 🚀

## 🌟 **Project Overview**

Welcome to the **Python API Test Framework**! This is an all-in-one solution for automating API tests, managing test data, and generating interactive reports. Built using Python and a variety of modern libraries, this framework allows you to:

- **Test** RESTful APIs.
- **Manage** test data from Excel.
- **Store** results in a database (SQLite).
- **Visualize** test results with a web-based dashboard.

---

## ⚙️ **Features**

✨ **Key Features**:

- 🧑‍💻 **API Client**: Sends HTTP requests (GET, POST, PUT, DELETE) to test APIs.
- 📊 **Excel Reader & Writer**: Reads test data from `.xlsx` files and writes results back to Excel.
- 🗃️ **Database Manager**: Stores test results in an SQLite database.
- 📈 **Test Reporting Dashboard**: Displays results in a Dash-based web application.
- 📅 **Comprehensive Reporting**:
    - **Execution Summary**: Passed, Failed, Skipped tests.
    - **Status Distribution**: Visualizes the breakdown of test statuses.
    - **Duration Histograms**: Shows the distribution of test durations.
    - **Results Table**: Provides detailed test result logs.

---

## 🚀 **Installation**

### **1. Install Dependencies**

The framework requires Python 3.6+ and several dependencies. To get started, clone the repository and install the required packages from the `requirements.txt`.

```bash
git clone https://github.com/anxoportela/python_api_test_framework.git
cd python-api-test-framework
```

#### **2. Set up a Virtual Environment (optional but recommended)**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

#### **3. Install the Required Dependencies**

```bash
pip install -r requirements.txt
```

---

## 🧪 **Running Tests**

Before launching the Dash dashboard, it's important to run the tests to generate the data that will be visualized.

To run the framework's tests, navigate to the root directory and execute the following:

```bash
pytest
```

This will run the tests and provide feedback on the success of each test case.

---

## 🚀 **Launch the Dash Dashboard** 💻

Once the tests are run and results are generated, you can launch the Dash-based reporting dashboard. This will display your test results in an interactive, web-based interface.

```bash
python web/app.py
```

Open your browser and go to `http://127.0.0.1:8050/` to view the dashboard.

---

## 📊 **Test Data Format** (Excel)

The framework reads the test data from an Excel file (`test_data.xlsx`) with the following columns in order:

| Column Name            | Description                                                            |
|------------------------|------------------------------------------------------------------------|
| **TestId**             | Unique identifier for the test case.                                   |
| **TestCase**           | Name or description of the test case.                                  |
| **Run**                | Whether the test should be run (`Y`/`N`).                              |
| **Method**             | HTTP method to be used (GET, POST, PUT, DELETE).                       |
| **URL**                | The base URL of the API being tested.                                  |
| **Endpoint**           | The specific endpoint to test, relative to the base URL.               |
| **Authorization**      | String of Authorization required (e.g., `Bearer`, `Basic`, or `None`). |
| **User**               | Username (if needed for authentication).                               |
| **Password**           | Password (if needed for authentication).                               |
| **Headers**            | HTTP headers in JSON format (optional).                                |
| **Body**               | Request body in JSON format (for POST/PUT requests).                   |
| **ExpectedStatusCode** | The expected HTTP status code (e.g., `200`, `404`).                    |
| **ExpectedResponse**   | The expected response body (optional, can be empty).                   |
| **Status**             | The result of the test (`Passed`, `Failed`, or `Skipped`).             |
| **Error**              | Any error message encountered during the test (optional).              |

---

### 🧑‍💻 **How Test Data is Used**

- **TestCase**: The description of the test case is logged for clarity.
- **Run**: This column determines if the test case should be executed. If `Run` is set to `N`, the test is skipped.
- **Method**: Defines the HTTP request method to use (e.g., `GET`, `POST`).
- **URL + Endpoint**: Combined, these form the complete URL for the request. The base `URL` and the specific `Endpoint` will be joined programmatically.
- **Authorization, User, Password**: These are used for authenticated requests (e.g., with Bearer tokens or Basic Authentication).
- **Headers & Body**: If required, HTTP headers and request bodies are sent as part of the API call.
- **ExpectedStatusCode & ExpectedResponse**: The actual response is compared against these values to determine if the test passes or fails.
- **Status**: After each test run, this column is updated with the test result.
- **Error**: If the test fails or an error occurs, the error message is logged here for further analysis.

---

## 📁 **Project Structure**

```
python_api_test_framework/
│
├── core/                    # Core logic for API requests and test data management
│   ├── __init__.py          # Core package initialization
│   ├── api_client.py        # Handles API requests
│   ├── excel_reader.py      # Reads test data from Excel files
│   ├── excel_writer.py      # Writes test results to Excel files
│   ├── test_data_model.py   # Defines the test data model
│   ├── db_manager.py        # Manages database interactions
│
├── data/                    # Stores test data and configuration files
│   ├── __init__.py          # Data package initialization
│   ├── test_data.xlsx       # Sample test data
│
├── reports/                 # Stores generated reports and test results
│   ├── __init__.py          # Reports package initialization
│   ├── results.db           # SQLite database for test results
│
├── tests/                   # Unit and functional tests for the framework
│   ├── __init__.py          # Test package initialization
│   └── test_api.py          # Tests launcher for the framework
│
├── web/                     # Dash web application for test reports
│   ├── __init__.py          # Web package initialization
│   ├── app.py               # Dash app for visualizing test reports
│
├── config.py                # Global configuration settings
├── requirements.txt         # List of required dependencies
```

---

## 🛠️ **How It Works**

### **API Client** 📡
The `api_client.py` handles API requests and responses. It supports multiple HTTP methods (GET, POST, PUT, DELETE) and stores the results, including status codes and response times.

### **Test Data Management** 📂
Test data is read from an Excel file (`test_data.xlsx`) using the `excel_reader.py` script. This data typically includes API endpoints, request methods, and expected results. After running the tests, results are written back to an Excel file using `excel_writer.py`.

### **Database Management** 🗄️
Test results are saved in an SQLite database (`results.db`). The `db_manager.py` file takes care of inserting and retrieving test results.

### **Reporting Dashboard** 📊
The `web/app.py` file serves as the entry point for the Dash-based web dashboard. This dashboard provides a comprehensive view of test results, including:

- **Test Statistics**: Overview of tests that passed, failed, and were skipped.
- **Graphs**:
    - **Status Distribution**: Displays a bar chart of test statuses (Passed, Failed, Skipped).
    - **Duration Distribution**: Visualizes the distribution of test durations.
- **Results Table**: A detailed table of individual test results, including status, duration, and additional logs.

---

## 📄 **License**

This project is licensed under the **MIT License**. For more details, see the [LICENSE](LICENSE) file.

---

## 📧 **Contact**

For any issues, questions, or suggestions, feel free to reach out to the project maintainers:

**Email**: hello@anxoportela.dev

---

### 🎉 **Enjoy using the Python API Test Framework!** 🎉