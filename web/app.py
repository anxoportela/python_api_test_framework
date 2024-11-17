import dash
import config
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import sqlite3
import json
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Inicialización de la aplicación Dash con un tema de Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX,
                                                "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap"])


def fetch_test_data(execution_id=None):
    """
    Obtiene los datos de las pruebas de la base de datos.
    Si se proporciona un `execution_id`, filtra los resultados por ese ID.
    """
    try:
        conn = sqlite3.connect(config.DB_PATH)
        query = "SELECT * FROM test_results"
        if execution_id:
            query += f" WHERE ExecutionId = {execution_id}"
        df = pd.read_sql(query, conn)  # Se convierte el resultado en un DataFrame de pandas
        conn.close()
        return df
    except Exception as e:
        print(f"Error al obtener los datos de las pruebas: {e}")
        return pd.DataFrame()  # Si ocurre un error, retorna un DataFrame vacío


def fetch_executions():
    """
    Obtiene una lista de las ejecuciones de pruebas desde la base de datos.
    """
    try:
        conn = sqlite3.connect(config.DB_PATH)
        query = "SELECT DISTINCT ExecutionId, ExecutionName FROM test_executions"
        df = pd.read_sql(query, conn)  # Se convierte el resultado en un DataFrame de pandas
        conn.close()
        return df
    except Exception as e:
        print(f"Error al obtener las ejecuciones: {e}")
        return pd.DataFrame()  # Si ocurre un error, retorna un DataFrame vacío


def get_execution_name(execution_id):
    """
    Obtiene el nombre de la ejecución dada su ID.
    """
    try:
        conn = sqlite3.connect(config.DB_PATH)
        query = f"SELECT ExecutionName FROM test_executions WHERE ExecutionId = {execution_id}"
        df = pd.read_sql(query, conn)  # Se convierte el resultado en un DataFrame de pandas
        conn.close()
        if not df.empty:
            return df['ExecutionName'].iloc[0]
        return None  # Si no se encuentra el nombre, retorna None
    except Exception as e:
        print(f"Error al obtener el nombre de la ejecución: {e}")
        return None  # Si ocurre un error, retorna None


def format_duration(duration):
    """
    Formatea la duración de la prueba en segundos y milisegundos.
    """
    if duration > 0:
        seconds = int(duration)
        milliseconds = int((duration - seconds) * 1000)
        return f"{seconds} sec {milliseconds} ms"
    else:
        return "0 sec 0 ms"  # Si la duración es 0 o menor, retorna 0 segundos y 0 milisegundos


# Layout principal de la aplicación, que contiene todos los componentes visuales
app.layout = html.Div([
    dbc.Container([
        # Fila para el encabezado principal
        dbc.Row([
            dbc.Col(
                html.H1("🔍 Reporte de Ejecuciones de Pruebas API 🚀",
                        style={"textAlign": "center", "marginTop": "40px", "color": "#2c3e50",
                               "fontFamily": "Arial, sans-serif"}),
                width=12
            ),
        ], style={"marginBottom": "40px"}),

        # Fila para seleccionar la ejecución de prueba
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
                    options=[],  # Las opciones se actualizarán dinámicamente
                    value=None,
                    clearable=False,
                    placeholder="Seleccione una ejecución",
                    style={"borderRadius": "0px", "backgroundColor": "#ecf0f1", "fontSize": "16px"}
                ), width=3, style={"margin": "0 auto"}
            ),
        ], style={"marginBottom": "40px"}),

        # Fila para mostrar las métricas de pruebas (total, pasadas, fallidas, saltadas, duración promedio)
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

        # Fila para los gráficos (Distribución de estados de las pruebas y Histograma de duración)
        dbc.Row([
            dbc.Col(dcc.Graph(id='status-distribution-graph', config={'displayModeBar': False}), width=6),
            dbc.Col(dcc.Graph(id='duration-histogram', config={'displayModeBar': False}), width=6),
        ]),

        # Fila para la tabla de resultados de las pruebas
        dbc.Row([
            dbc.Col(dash_table.DataTable(
                id='test-results-table',
                page_size=10,
                style_cell={'textAlign': 'left', 'fontFamily': 'Arial, sans-serif'},
                columns=[
                    {'name': '🆔 Test ID', 'id': 'TestId'},
                    {'name': '📝 Test Case', 'id': 'TestCase'},
                    {'name': '✅⏭️❌ Status', 'id': 'Status'},
                    {'name': '⏱️ Duration', 'id': 'Duration'}
                ],
                style_header={'fontWeight': 'bold', 'textTransform': 'none', 'fontFamily': 'Roboto, sans-serif'},
                row_selectable='single',  # Permite seleccionar filas de la tabla
                selected_rows=[],
                style_table={'overflowX': 'auto', 'borderRadius': '0px'},
                style_cell_conditional=[
                    {'if': {'column_id': 'TestId'}, 'width': '10%'},
                    {'if': {'column_id': 'TestCase'}, 'width': '50%'},
                    {'if': {'column_id': 'Status'}, 'width': '20%'},
                    {'if': {'column_id': 'Duration'}, 'width': '20%'}
                ],
                style_data_conditional=[
                    # Condicionales para cambiar el color de las celdas según el estado de la prueba
                    {'if': {'column_id': 'Status', 'filter_query': '{Status} = "PASSED"'},
                     'backgroundColor': 'green', 'color': 'white'},
                    {'if': {'column_id': 'Status', 'filter_query': '{Status} = "FAILED"'},
                     'backgroundColor': 'red', 'color': 'white'},
                    {'if': {'column_id': 'Status', 'filter_query': '{Status} = "SKIPPED"'},
                     'backgroundColor': 'yellow', 'color': 'black'}
                ]
            ), width=8, style={'margin': '0 auto'}),
        ], style={"marginBottom": "40px"}),

        # Modal para mostrar detalles de una prueba seleccionada
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
            style={'position': 'fixed', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)'}
        ),

        # Fila para el pie de página
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


def safe_int(value):
    """
    Convierte el valor dado en un entero seguro, retornando 0 si el valor es NaN o no puede convertirse.
    """
    if pd.isna(value):
        return 0
    try:
        return int(value)
    except ValueError:
        return 0  # Si ocurre un error al convertir, retorna 0


# noinspection t
@app.callback(
    [
        Output("execution-filter", "options"),  # Actualiza las opciones del dropdown de ejecuciones
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
        Input("execution-filter", "value"),  # Cuando el usuario selecciona una ejecución
        Input("test-results-table", "selected_rows"),  # Cuando el usuario selecciona una fila de la tabla
        Input("close-modal", "n_clicks"),  # Cuando el usuario hace clic en el botón "Cerrar" del modal
    ],
    [State("test-results-table", "data"), State("test-modal", "is_open")]
)


def update_report(execution_id, selected_rows, close_modal_clicks, table_data, is_open):
    """
    Esta función maneja la lógica de actualización del reporte cada vez que el usuario interactúa
    con los filtros, las filas seleccionadas de la tabla o el botón para cerrar el modal.
    """
    # Obtener las ejecuciones y actualizar las opciones del filtro
    executions = fetch_executions()
    execution_options = [{'label': exec['ExecutionName'], 'value': exec['ExecutionId']} for _, exec in
                         executions.iloc[::-1].iterrows()]

    if execution_id:
        # Si se selecciona una ejecución, obtener los resultados correspondientes
        df_results = fetch_test_data(execution_id)
        total_tests = len(df_results)  # Número total de pruebas
        passed_tests = len(df_results[df_results['Status'] == 'PASSED'])  # Pruebas pasadas
        failed_tests = len(df_results[df_results['Status'] == 'FAILED'])  # Pruebas falladas
        skipped_tests = len(df_results[df_results['Status'] == 'SKIPPED'])  # Pruebas saltadas
        avg_duration = df_results['Duration'].mean() if not df_results[
            'Duration'].isnull().all() else 0  # Duración promedio
        avg_duration_str = format_duration(avg_duration)  # Formato legible de la duración promedio

        # Crear el gráfico de distribución de estados
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

        # Crear el histograma de duración de las pruebas
        duration_fig = px.histogram(df_results, x='Duration', title="⏱️ Histograma de Duración de Pruebas", nbins=20)
        duration_fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)

        # Formatear la duración de las pruebas en la tabla
        df_results['Duration'] = df_results.apply(
            lambda row: format_duration(row['Duration']) if row['Status'] != "SKIPPED" else "",
            axis=1
        )

        # Preparar los datos para la tabla de resultados
        table_data = df_results[['TestId', 'TestCase', 'Status', 'Duration']].to_dict('records')

        # Si hay una fila seleccionada, mostrar los detalles en el modal
        if selected_rows:
            selected_row_data = df_results.iloc[selected_rows[0]]
            error_message = selected_row_data['Error']
            formatted_error = None
            if error_message:
                try:
                    if "Expected response:" in error_message and "Got:" in error_message:
                        plain_text, responses = error_message.split("Got:", 1)
                        expected_text, got_text = plain_text.split("Expected response:", 1)

                        # Formatear los errores para que sean más legibles
                        expected_json = json.dumps(eval(expected_text.strip()),
                                                   indent=2) if expected_text.strip() else "{}"
                        got_json = json.dumps(eval(responses.strip()), indent=2)

                        formatted_error = html.Div([
                            html.Details([
                                html.Summary("Ver respuesta esperada"),
                                html.Pre(expected_json, style={
                                    "whiteSpace": "pre-wrap",
                                    "wordBreak": "break-word",
                                    "backgroundColor": "#e9ecef",
                                    "padding": "10px",
                                    "borderRadius": "5px"
                                })
                            ]),
                            html.Details([
                                html.Summary("Ver respuesta obtenida (Got)"),
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

            test_details = html.Div([
                html.P(f"Test ID: {selected_row_data['TestId']}"),
                html.P(f"Test Case: {selected_row_data['TestCase']}"),
                html.P(f"Status: {selected_row_data['Status']}"),
                html.P(f"Method: {selected_row_data['Method']}"),
                html.P(f"URL: {selected_row_data['URL']}"),
                html.P(f"Endpoint: {selected_row_data['Endpoint']}"),

                html.P(
                    f"Expected Status Code: {safe_int(selected_row_data['ExpectedStatusCode'])}"
                    if selected_row_data['Status'] == "SKIPPED"
                    else (
                        f"Expected Status Code: {safe_int(selected_row_data['ExpectedStatusCode'])}"
                        if safe_int(selected_row_data['ExpectedStatusCode']) != safe_int(
                            selected_row_data['ActualStatusCode'])
                        else ""
                    ),
                    style={
                        "color": "red" if selected_row_data['Status'] != "SKIPPED" and safe_int(
                            selected_row_data['ExpectedStatusCode']) != safe_int(
                            selected_row_data['ActualStatusCode']) else ""
                    }
                ),

                html.P(f"Status Code: {safe_int(selected_row_data['ActualStatusCode'])}" if selected_row_data[
                                                                                                'Status'] != "SKIPPED" else ""),

                html.P(
                    f"Duration: {selected_row_data['Duration']}" if selected_row_data['Status'] != "SKIPPED" else ""),
                html.P(f"Response Size: {selected_row_data['ResponseSize']} bytes" if selected_row_data[
                                                                                          'Status'] != "SKIPPED" else ""),

                *([html.Div([html.P("Error:"), formatted_error])] if selected_row_data[
                                                                         'Status'] != "SKIPPED" and formatted_error else []),
            ])

            # Si el modal no está abierto, mostrar los detalles y abrir el modal
            if not is_open:
                return execution_options, total_tests, passed_tests, failed_tests, skipped_tests, avg_duration_str, status_fig, duration_fig, {
                    'display': 'block'}, {'display': 'block'}, table_data, True, test_details

        # Si no se ha seleccionado ninguna fila, devolver los valores estándar
        return execution_options, total_tests, passed_tests, failed_tests, skipped_tests, avg_duration_str, status_fig, duration_fig, {
            'display': 'block'}, {'display': 'block'}, table_data, False, None

    return execution_options, 0, 0, 0, 0, 0, {}, {}, {'display': 'none'}, {'display': 'none'}, [], False, None


# Arrancar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
