import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import sqlite3
import json
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])


# Function to fetch test data from the database
def fetch_test_data(execution_id=None, page=0, page_size=10):
    """
    Fetches test data from the 'test_results' table in the database.

    Args:
    - execution_id (int): The execution ID to filter by (optional).
    - page (int): The page number for pagination (default is 0).
    - page_size (int): The number of records per page (default is 10).

    Returns:
    - pd.DataFrame: A dataframe containing the test results.
    """
    try:
        conn = sqlite3.connect('reports/results.db')
        query = "SELECT * FROM test_results"
        if execution_id:
            query += f" WHERE ExecutionId = {execution_id}"
        query += f" LIMIT {page_size} OFFSET {page * page_size}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching test data: {e}")
        return pd.DataFrame()


# Function to fetch execution details from the database
def fetch_executions():
    """
    Fetches distinct execution IDs and names from the 'test_executions' table.

    Returns:
    - pd.DataFrame: A dataframe containing execution details.
    """
    try:
        conn = sqlite3.connect('reports/results.db')
        query = "SELECT DISTINCT ExecutionId, ExecutionName FROM test_executions"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching executions: {e}")
        return pd.DataFrame()


# Function to get execution name for a given execution ID
def get_execution_name(execution_id):
    """
    Fetches the name of an execution given its ID.

    Args:
    - execution_id (int): The execution ID.

    Returns:
    - str: The name of the execution.
    """
    try:
        conn = sqlite3.connect('reports/results.db')
        query = f"SELECT ExecutionName FROM test_executions WHERE ExecutionId = {execution_id}"
        df = pd.read_sql(query, conn)
        conn.close()
        if not df.empty:
            return df['ExecutionName'].iloc[0]
        return None
    except Exception as e:
        print(f"Error fetching execution name: {e}")
        return None


# Function to format test duration as a human-readable string
def format_duration(duration):
    """
    Formats a duration (in seconds) into a human-readable string.

    Args:
    - duration (float): The duration in seconds.

    Returns:
    - str: A formatted string representing the duration (e.g., "2 sec 500 ms").
    """
    if duration > 0:
        seconds = int(duration)  # Whole seconds
        milliseconds = int((duration - seconds) * 1000)  # Remaining milliseconds
        return f"{seconds} sec {milliseconds} ms"
    else:
        return "0 sec 0 ms"


# Define the layout of the app (HTML structure using Dash components)
app.layout = html.Div([
    dbc.Container([
        # Header Row
        dbc.Row([
            dbc.Col(
                html.H1("🔍 Reporte de Ejecuciones de Pruebas API 🚀",
                        style={"textAlign": "center", "marginTop": "40px", "color": "#2c3e50",
                               "fontFamily": "Arial, sans-serif"}),
                width=12
            ),
        ], style={"marginBottom": "40px"}),

        # Execution Filter Dropdown
        dbc.Row([
            dbc.Col(
                html.H4("👨‍💻 Seleccionar Ejecución",
                        style={"textAlign": "center", "fontWeight": "bold", "marginBottom": "10px",
                               "fontFamily": "Arial, sans-serif"}),
                width=12
            ),
            dbc.Col(
                dcc.Dropdown(
                    id="execution-filter",
                    options=[],  # Options will be populated by callback
                    value=None,
                    clearable=False,
                    placeholder="Seleccione una ejecución",
                    style={"borderRadius": "0px", "backgroundColor": "#ecf0f1", "fontSize": "16px"}
                ), width=3, style={"margin": "0 auto"}
            ),
        ], style={"marginBottom": "40px"}),

        # Cards for displaying test statistics
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("📊 Total de Pruebas", style={"backgroundColor": "#34495e", "color": "#fff"}),
                dbc.CardBody(
                    html.H4(id="total-tests", style={"color": "#34495e", "fontSize": "20px", "fontWeight": "bold"}))
            ]), width=2, style={"margin": "0 auto", "borderRadius": "0px"}),
            dbc.Col(dbc.Card([
                dbc.CardHeader(" ✅ Pruebas Pasadas", style={"backgroundColor": "#28A745", "color": "#fff"}),
                dbc.CardBody(
                    html.H4(id="passed-tests", style={"color": "#28A745", "fontSize": "20px", "fontWeight": "bold"}))
            ]), width=2, style={"margin": "0 auto", "borderRadius": "0px"}),
            dbc.Col(dbc.Card([
                dbc.CardHeader("❌ Pruebas Falladas", style={"backgroundColor": "#DC3545", "color": "#fff"}),
                dbc.CardBody(
                    html.H4(id="failed-tests", style={"color": "#DC3545", "fontSize": "20px", "fontWeight": "bold"}))
            ]), width=2, style={"margin": "0 auto", "borderRadius": "0px"}),
            dbc.Col(dbc.Card([
                dbc.CardHeader("⏭️ Pruebas Saltadas", style={"backgroundColor": "#FFC107", "color": "#fff"}),
                dbc.CardBody(
                    html.H4(id="skipped-tests", style={"color": "#FFC107", "fontSize": "20px", "fontWeight": "bold"}))
            ]), width=2, style={"margin": "0 auto", "borderRadius": "0px"}),
            dbc.Col(dbc.Card([
                dbc.CardHeader("⏱ Duración Promedio", style={"backgroundColor": "#007BFF", "color": "#fff"}),
                dbc.CardBody(
                    html.H4(id="avg-duration", style={"color": "#007BFF", "fontSize": "20px", "fontWeight": "bold"}))
            ]), width=2, style={"margin": "0 auto", "borderRadius": "0px"}),
        ], justify="center", style={"marginBottom": "40px"}),

        # Graphs for status distribution and duration histogram
        dbc.Row([
            dbc.Col(dcc.Graph(id='status-distribution-graph', config={'displayModeBar': False}), width=6),
            dbc.Col(dcc.Graph(id='duration-histogram', config={'displayModeBar': False}), width=6),
        ]),

        # Table for displaying test results
        dbc.Row([
            dbc.Col(dash_table.DataTable(
                id='test-results-table',
                page_size=10,
                style_cell={'textAlign': 'left', 'fontFamily': 'Arial, sans-serif'},
                columns=[
                    {'name': 'Test ID', 'id': 'TestId'},
                    {'name': 'TestCase', 'id': 'TestCase'},
                    {'name': 'Status', 'id': 'Status'},
                    {'name': 'Duration', 'id': 'Duration'}
                ],
                row_selectable='single',
                selected_rows=[],
                style_table={'overflowX': 'auto', 'borderRadius': '0px'},
                style_cell_conditional=[
                    {'if': {'column_id': 'TestId'}, 'width': '10%'},
                    {'if': {'column_id': 'TestCase'}, 'width': '50%'},
                    {'if': {'column_id': 'Status'}, 'width': '20%'},
                    {'if': {'column_id': 'Duration'}, 'width': '20%'}
                ],
                style_data_conditional=[
                    {'if': {'column_id': 'Status', 'filter_query': '{Status} = "PASSED"'},
                     'backgroundColor': 'green', 'color': 'white'},
                    {'if': {'column_id': 'Status', 'filter_query': '{Status} = "FAILED"'},
                     'backgroundColor': 'red', 'color': 'white'},
                    {'if': {'column_id': 'Status', 'filter_query': '{Status} = "SKIPPED"'},
                     'backgroundColor': 'yellow', 'color': 'black'}
                ]
            ), width=8, style={'margin': '0 auto'}),
        ], style={"marginBottom": "40px"}),

        # Modal for displaying test details
        dbc.Modal(
            [
                dbc.ModalHeader("Detalles del Test", close_button=True),
                dbc.ModalBody(html.Div(id="test-details")),
                dbc.ModalFooter(
                    dbc.Button("Cerrar", id="close-modal", className="ml-auto",
                               style={"backgroundColor": "#28A745", "color": "white"})
                ),
            ],
            id="test-modal",
            is_open=False,
            centered=True,
            style={
                'position': 'fixed',
                'top': '50%',
                'left': '50%',
                'transform': 'translate(-50%, -50%)',
                'borderRadius': '0px',
            }
        ),

        # Footer with contact info
        dbc.Row([
            dbc.Col(
                html.Footer(
                    html.P("🚀 Reporte generado con ❤️ por tu equipo de QA. Contacto: qa@ejemplo.com",
                           style={"textAlign": "center", "fontSize": "14px", "color": "#6c757d", "marginTop": "20px"})
                ),
                width=12
            ),
        ], style={"marginTop": "40px"}),
    ], fluid=True)
])


# Function to handle NaN values for status codes and safely convert to int
def safe_int(value):
    """
    Converts a value to integer if it's not NaN. Otherwise, returns a default value (e.g., 0).
    """
    if pd.isna(value):
        return 0  # or you can return None or another default value
    try:
        return int(value)
    except ValueError:
        return 0  # Default value in case of invalid data


# Callback function to update the report based on selected execution and row clicks
# noinspection t
@app.callback(
    [
        Output("execution-filter", "options"),
        Output("total-tests", "children"),
        Output("passed-tests", "children"),
        Output("failed-tests", "children"),
        Output("skipped-tests", "children"),
        Output("avg-duration", "children"),
        Output("status-distribution-graph", "figure"),
        Output("duration-histogram", "figure"),
        Output("status-distribution-graph", "style"),
        Output("duration-histogram", "style"),
        Output("test-results-table", "data"),
        Output("test-modal", "is_open"),
        Output("test-details", "children")
    ],
    [
        Input("execution-filter", "value"),
        Input("test-results-table", "selected_rows"),
        Input("close-modal", "n_clicks"),
    ],
    [State("test-results-table", "data"), State("test-modal", "is_open")]
)
def update_report(execution_id, selected_rows, close_modal_clicks, table_data, is_open):
    """
    This function updates the entire report including the test statistics,
    graphs, and details of the selected test.

    Args:
    - execution_id (int or None): ID of the selected execution.
    - selected_rows (list): List of selected row indices in the test table.
    - close_modal_clicks (int): The number of clicks on the close button of the modal.
    - table_data (list): Data for the test results table.
    - is_open (bool): Whether the test details modal is open.

    Returns:
    - List of updated outputs for the Dash components.
    """
    # Fetch available executions and populate dropdown options
    executions = fetch_executions()
    execution_options = [{'label': exec['ExecutionName'], 'value': exec['ExecutionId']} for _, exec in
                         executions.iloc[::-1].iterrows()]

    # If an execution is selected, fetch relevant test data
    if execution_id:
        df_results = fetch_test_data(execution_id)
        total_tests = len(df_results)
        passed_tests = len(df_results[df_results['Status'] == 'PASSED'])
        failed_tests = len(df_results[df_results['Status'] == 'FAILED'])
        skipped_tests = len(df_results[df_results['Status'] == 'SKIPPED'])
        avg_duration = df_results['Duration'].mean() if not df_results['Duration'].isnull().all() else 0
        avg_duration_str = format_duration(avg_duration)

        # Create status distribution graph
        status_counts = df_results['Status'].value_counts()
        status_fig = {
            'data': [{
                'x': status_counts.index,
                'y': status_counts.values,
                'type': 'bar',
                'name': 'Estado de las pruebas',
                'marker': {
                    'color': ['green' if status == 'PASSED' else 'red' if status == 'FAILED' else 'yellow' for status in
                              status_counts.index]
                }
            }],
            'layout': {
                'title': '📊 Distribución de Estados de las Pruebas',
                'plot_bgcolor': '#f7f7f7',
                'paper_bgcolor': '#fff',
                'font': {'color': '#333'},
                'barmode': 'stack',
            }
        }

        # Create duration histogram
        duration_fig = px.histogram(df_results, x='Duration', title="⏱️ Histograma de Duración de Pruebas", nbins=20)
        duration_fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)

        # Format duration for the table, leaving blank for skipped tests
        df_results['Duration'] = df_results.apply(
            lambda row: format_duration(row['Duration']) if row['Status'] != "SKIPPED" else "",
            axis=1
        )

        # Prepare table data
        table_data = df_results[['TestId', 'TestCase', 'Status', 'Duration']].to_dict('records')

        # Handle test details for a selected row
        if selected_rows:
            selected_row_data = df_results.iloc[selected_rows[0]]
            error_message = selected_row_data['Error']
            formatted_error = None
            if error_message:
                try:
                    if "Expected response:" in error_message and "Got:" in error_message:
                        plain_text, responses = error_message.split("Got:", 1)
                        expected_text, got_text = plain_text.split("Expected response:", 1)

                        expected_json = json.dumps(eval(expected_text.strip()),
                                                   indent=2) if expected_text.strip() else "{}"
                        got_json = json.dumps(eval(responses.strip()), indent=2)

                        formatted_error = html.Div([
                            html.Details([
                                html.Summary("View Expected Response"),
                                html.Pre(expected_json, style={
                                    "whiteSpace": "pre-wrap",
                                    "wordBreak": "break-word",
                                    "backgroundColor": "#e9ecef",
                                    "padding": "10px",
                                    "borderRadius": "5px"
                                })
                            ]),
                            html.Details([
                                html.Summary("View Actual Response (Got)"),
                                html.Pre(got_json, style={
                                    "whiteSpace": "pre-wrap",
                                    "wordBreak": "break-word",
                                    "backgroundColor": "#e9ecef",
                                    "padding": "10px",
                                    "borderRadius": "5px"
                                })
                            ])
                        ])
                    else:
                        formatted_error = html.Pre(error_message, style={
                            "whiteSpace": "pre-wrap",
                            "wordBreak": "break-word",
                            "backgroundColor": "#f8f9fa",
                            "padding": "10px",
                            "borderRadius": "5px"
                        })
                except Exception as e:
                    formatted_error = html.Pre(error_message, style={
                        "whiteSpace": "pre-wrap",
                        "wordBreak": "break-word",
                        "backgroundColor": "#f8f9fa",
                        "padding": "10px",
                        "borderRadius": "5px"
                    })

            # Prepare the modal with the test details
            test_details = html.Div([
                html.P(f"Test ID: {selected_row_data['TestId']}"),
                html.P(f"Test Case: {selected_row_data['TestCase']}"),
                html.P(f"Status: {selected_row_data['Status']}"),
                html.P(f"Method: {selected_row_data['Method']}"),
                html.P(f"URL: {selected_row_data['URL']}"),
                html.P(f"Endpoint: {selected_row_data['Endpoint']}"),

                # Display Expected Status Code only if it doesn't match Actual Status Code
                html.P(f"Expected Status Code: {safe_int(selected_row_data['ExpectedStatusCode'])}" if safe_int(
                    selected_row_data['ExpectedStatusCode']) != safe_int(selected_row_data['ActualStatusCode']) else "",
                       style={"color": "red" if safe_int(selected_row_data['ExpectedStatusCode']) != safe_int(
                           selected_row_data['ActualStatusCode']) else ""}),

                # Change 'Actual Status Code' to 'Status Code' and rename it
                html.P(f"Status Code: {safe_int(selected_row_data['ActualStatusCode'])}" if selected_row_data[
                                                                                                'Status'] != "SKIPPED" else ""),

                # Display Duration and Response Size if not Skipped
                html.P(
                    f"Duration: {selected_row_data['Duration']}" if selected_row_data['Status'] != "SKIPPED" else ""),
                html.P(f"Response Size: {selected_row_data['ResponseSize']} bytes" if selected_row_data[
                                                                                          'Status'] != "SKIPPED" else ""),

                # Display error message if there's an error and the test is not skipped
                *([html.Div([html.P("Error:"), formatted_error])] if selected_row_data[
                                                                         'Status'] != "SKIPPED" and formatted_error else []),
            ])

            # If modal is not open, return updated data
            if not is_open:
                return execution_options, total_tests, passed_tests, failed_tests, skipped_tests, avg_duration_str, status_fig, duration_fig, {
                    'display': 'block'}, {'display': 'block'}, table_data, True, test_details

        # Return updated data when no row is selected
        return execution_options, total_tests, passed_tests, failed_tests, skipped_tests, avg_duration_str, status_fig, duration_fig, {
            'display': 'block'}, {'display': 'block'}, table_data, False, None

    # Default return if no execution is selected
    return execution_options, 0, 0, 0, 0, 0, {}, {}, {'display': 'none'}, {'display': 'none'}, [], False, None


# Run the server to start the app
if __name__ == "__main__":
    app.run_server(debug=True)
