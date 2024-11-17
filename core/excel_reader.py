import pandas as pd
import json
from core.test_data_model import APIData


def _convert_to_dict(value):
    """
    Converts a string value to a dictionary if it is in valid JSON format.

    Args:
        value (str): The string to be converted to a dictionary.

    Returns:
        dict: The converted dictionary, or an empty dictionary if the conversion fails.
    """
    if isinstance(value, str) and value:  # Ensure value is a non-empty string
        try:
            # Try to parse the string as JSON; return an empty dict if it's invalid JSON
            if value != '{}':
                return json.loads(value)
            else:
                return {}
        except json.JSONDecodeError:
            print(f"Error al convertir la cadena a diccionario: {value}")  # Log error if JSON parsing fails
            return {}
    return {}  # Return an empty dict if the value is not a string


def _validate(record):
    """
    Validates a record by attempting to instantiate it as an APIData object.

    Args:
        record (dict): A dictionary containing test data for validation.

    Returns:
        bool: True if the record is valid according to the APIData model, False otherwise.
    """
    try:
        # Attempt to create an APIData object from the record
        APIData(**record)
        return True
    except Exception as e:
        print(f"Validation error: {e}")  # Log validation errors
        return False


class ExcelReader:
    """
    A class to read and process test data from an Excel file.

    Attributes:
        file_path (str): The path to the Excel file containing the test data.
    """
    def __init__(self, file_path):
        """
        Initializes the ExcelReader with the file path.

        Args:
            file_path (str): The path to the Excel file.
        """
        self.file_path = file_path

    def load_data(self):
        """
        Loads test data from the specified Excel file, processes it, and validates the records.

        Returns:
            list: A list of validated APIData objects extracted from the Excel file.
                  Returns an empty list if there is an error reading the file or if validation fails.
        """
        try:
            # Read the Excel file, specifically the "TestSuite" sheet
            df = pd.read_excel(self.file_path, sheet_name="TestSuite")

            # Fill missing values with empty strings
            df = df.fillna('')

            # Ensure 'TestId' is a string, and convert other fields to dictionaries using the conversion function
            df['TestId'] = df['TestId'].apply(str)
            df['Headers'] = df['Headers'].apply(_convert_to_dict)
            df['Body'] = df['Body'].apply(_convert_to_dict)
            df['ExpectedResponse'] = df['ExpectedResponse'].apply(_convert_to_dict)

            # Convert DataFrame to a list of dictionaries (one per record)
            records = df.to_dict(orient="records")

            # Validate each record and return only the valid ones as APIData objects
            validated_data = [APIData(**record) for record in records if _validate(record)]
            return validated_data  # Return the list of validated test data objects

        except Exception as e:
            print(f"Error reading the Excel file: {e}")  # Log any error that occurs while reading the file
            return []  # Return an empty list if an error occurs
