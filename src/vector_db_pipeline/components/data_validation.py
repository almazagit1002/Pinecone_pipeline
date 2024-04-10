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

    def validate_all_columns(self) -> bool:
        """
        Validates presence of all columns specified in the schema.

        Returns:
            bool: True if all columns are present, False otherwise.
        """
        try:
            data = pd.read_csv(self.config.read_data_dir)
            all_cols = list(data.columns)
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
            data = pd.read_csv(self.config.read_data_dir)
            unique_id = len(data.id.unique()) == len(data)

            with open(self.config.STATUS_FILE, 'a') as f:
                f.write(f"Unique ids: {unique_id}\n")

            logger.info(f"Unique ids: {unique_id}")
            return unique_id
        
        except Exception as e:
            logger.error(f"Error occurred during unique index validation: {str(e)}")
            raise e
