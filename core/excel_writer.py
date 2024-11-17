from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Border, Side, Alignment
from datetime import datetime

def _copy_worksheet(wb, source_sheet_name, new_sheet_name):
    """
    Copies a worksheet from an existing sheet to a new sheet with a specified name.

    Args:
        wb (Workbook): The openpyxl Workbook object containing the sheet.
        source_sheet_name (str): The name of the sheet to copy.
        new_sheet_name (str): The name of the new sheet to create.

    Returns:
        Worksheet: The newly created sheet or None if the source sheet doesn't exist.
    """
    if source_sheet_name not in wb.sheetnames:
        print(f"No se encontró la hoja fuente: {source_sheet_name}")
        return None
    source_sheet = wb[source_sheet_name]
    new_sheet = wb.copy_worksheet(source_sheet)
    new_sheet.title = new_sheet_name
    return new_sheet


def _create_new_sheet_with_date(wb):
    """
    Creates a new sheet with the current date and time as the sheet name.
    This sheet will contain headers for test result data.

    Args:
        wb (Workbook): The openpyxl Workbook object where the new sheet will be created.

    Returns:
        Worksheet: The newly created sheet.
    """
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    sheet_name = f"TestCases_{current_date}"

    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    headers = [
        "TestId", "TestCase", "Status", "Error", "Method", "URL",
        "Endpoint", "ExpectedStatusCode", "ActualStatusCode",
        "Duration", "ResponseSize"
    ]
    ws.append(headers)

    return ws


def _format_error_message(error_message):
    """
    Formats the error message to improve readability, adding line breaks where appropriate.

    Args:
        error_message (str): The error message to format.

    Returns:
        str: The formatted error message with line breaks.
    """
    if error_message:
        formatted_message = error_message.replace("{", "\n{").replace("}", "}\n")
        return formatted_message.replace(",", "\n")
    return error_message


def _get_status_format(status, error_message):
    """
    Determines the formatting for a test case result based on its status.

    Args:
        status (str): The test status (e.g., "PASSED", "FAILED", "SKIPPED").
        error_message (str): The error message associated with the test, if any.

    Returns:
        tuple: A tuple containing:
            - status (str): The formatted status ("PASSED", "FAILED", or "SKIPPED").
            - color (str): The hex color code for the status cell.
            - error_message (str or None): The formatted error message (or None if no error).
    """
    if status == "SKIPPED":
        return ("SKIPPED", "FFFF00", None)
    elif status == "PASSED":
        return ("PASSED", "00FF00", None)
    else:
        return ("FAILED", "FF0000", _format_error_message(error_message))


class ExcelWriter:
    """
    A class for writing and formatting test results in an Excel file using the openpyxl library.

    This class is responsible for:
    - Updating the existing test result data in the "TestSuite" sheet.
    - Creating a new sheet with the current date to log additional test results.
    - Formatting the test result cells based on status and errors.

    Attributes:
        file_path (str): The path to the Excel file where test results will be written.
        thin_border (Border): The border style used to format cells in the spreadsheet.
    """

    def __init__(self, file_path):
        """
        Initializes the ExcelWriter with the file path of the Excel file to be updated.

        Args:
            file_path (str): The path to the Excel file.
        """
        self.file_path = file_path
        self.thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin")
        )

    def _apply_format_to_row(self, row, status, color, error_message):
        """
        Applies formatting to a row based on the test case result.

        Args:
            row (tuple): The row to format.
            status (str): The formatted status value ("PASSED", "FAILED", or "SKIPPED").
            color (str): The hex color code for the status cell.
            error_message (str or None): The formatted error message (or None if no error).
        """
        status_cell = row[13]  # The cell containing the status
        error_cell = row[14]   # The cell containing the error message

        # Set the status and its formatting
        status_cell.value = status
        status_cell.fill = PatternFill(start_color=color, fill_type="solid")
        status_cell.font = Font(color="000000")

        # Set the error message (with line breaks) and wrap text for better readability
        error_cell.value = error_message
        error_cell.alignment = Alignment(wrap_text=True)

        # Apply borders to all cells in the row
        for cell in row:
            cell.border = self.thin_border

    def _update_row(self, ws, result):
        """
        Updates the row in the worksheet with the given test result data.

        Args:
            ws (Worksheet): The worksheet to update.
            result (dict): A dictionary containing the test result data.
        """
        for row in ws.iter_rows(min_row=2, max_col=ws.max_column-1):
            if row[0].value == result["TestId"]:
                status, color, error_message = _get_status_format(result["Status"], result.get("Error"))
                self._apply_format_to_row(row, status, color, error_message)

    def update_results(self, results):
        """
        Updates the 'TestSuite' sheet and creates a new sheet with the test results.

        Args:
            results (list of dict): A list of dictionaries, each containing test case results.
        """
        try:
            if not results:
                print("No hay resultados para actualizar.")
                return

            wb = load_workbook(self.file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_sheet_name = f"TestSuite_{timestamp}"

            # Check if the 'TestSuite' sheet exists and update it
            if "TestSuite" in wb.sheetnames:
                main_sheet = wb["TestSuite"]
                for result in results:
                    self._update_row(main_sheet, result)
            else:
                print("No se encontró la hoja principal 'TestSuite'. No se realizaron actualizaciones.")
                return

            # Create a new sheet to log test results with the current timestamp
            new_sheet = _copy_worksheet(wb, "TestSuite", new_sheet_name)
            if new_sheet:
                for result in results:
                    self._update_row(new_sheet, result)

            wb.save(self.file_path)
            print(f"Resultados actualizados en 'TestSuite' y en la nueva hoja '{new_sheet_name}'.")
        except Exception as e:
            print(f"Error actualizando el archivo Excel: {e}")
