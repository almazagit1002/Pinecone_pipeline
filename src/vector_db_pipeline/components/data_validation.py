from vector_db_pipeline.entity.config_entity import DataValidationConfig
from vector_db_pipeline import logger
import pandas as pd


"""
Validates data integrity and structure based on specified schema and configuration settings.

Attributes:
    config (DataValidationConfig): Configuration object containing data validation settings.

Methods:
    validate_all_columns() -> bool: Validates presence of all columns specified in the schema.
    validate_unique_index() -> bool: Validates uniqueness of the 'id' column as the index.
"""
class DataValidation:
    def __init__(self, config: DataValidationConfig):
        """
        Initializes DataValidation with the provided data validation configuration.

        Args:
            config (DataValidationConfig): Configuration object containing data validation settings.
        """
        self.config = config
        self.data = pd.read_json(self.config.read_data_dir, orient='records')

    def validate_all_columns(self) -> bool:
        """
        Validates presence of all columns specified in the schema.

        Returns:
            bool: True if all columns are present, False otherwise.
        """
        try:
            all_cols = list(self.data.columns)
            all_schema = self.config.SCHEMA
            all_schema['id'] = 'str'
            all_schema['values'] = 'list'

            validation_status = all(col in all_schema.keys() for col in all_cols)

            with open(self.config.STATUS_FILE, 'a') as f:
                f.write(f"All columns present in data: {validation_status}\n")

            logger.info(f"All columns present in data: {validation_status}")
            return validation_status
        
        except Exception as e:
            logger.error(f"Error occurred during column validation: {str(e)}")
            raise e
        
    def validate_unique_index(self) -> bool:
        """
        Validates uniqueness of the 'id' column as the index.

        Returns:
            bool: True if 'id' column is unique, False otherwise.
        """
        try:
            unique_id = len(self.data.id.unique()) == len(self.data)

            with open(self.config.STATUS_FILE, 'a') as f:
                f.write(f"Unique ids: {unique_id}\n")

            logger.info(f"Unique ids: {unique_id}")
            return unique_id
        
        except Exception as e:
            logger.error(f"Error occurred during unique index validation: {str(e)}")
            raise e
        
    def validate_column_types(self):
        """
        Get the types of values in each column of the DataFrame.

       
        Returns:
            dict: A dictionary where keys are column names and values are lists containing the types of values present in each column.
        """
        
        try:
            column_types = {}
            how_many_types = {}
            
            # Iterate over each column in the DataFrame
            for column in self.data.columns:
                # Create a set of unique types for values in the column
                types = set(type(value) for value in self.data[column])
                # Convert the set to a list for easier handling
                types_list = list(types)

                column_types[column] = types_list
                how_many_types[column] = len(types_list)
            
            

            # Check if elements in 'values' column are of type float
            vector_elemts_type = list(set(type(elem) for elem in self.data['values'][0]))
            if len(vector_elemts_type) != 1 or vector_elemts_type[0] != float:
                raise TypeError("Vector values are not of type float")

            # Check if all columns have a single type
            unique_types = all(value == 1 for value in how_many_types.values())

            # Check if 'id' column is of type string and 'values' column is of type list
            id_type = column_types['id'][0] == str
            vector_type = column_types['values'][0] == list

            if not id_type:
                raise TypeError("ID column is not of type string")
            elif not vector_type:
                raise TypeError("Values column is not of type list")
            elif not unique_types:
                raise TypeError("Several types present in data")

            # Log success message
            with open(self.config.STATUS_FILE, 'a') as f:
                f.write("Data types are correct\n")

            return logger.info("Data types are valid")
        except Exception as e:
            raise e

