from vector_db_pipeline.constants import *
from vector_db_pipeline.utils.common import read_yaml, create_directories
from vector_db_pipeline.entity.config_entity import (DataIngestionConfig,
                                                     DataValidationConfig,
                                                     DataUploadConfig)


"""
Manages configuration settings for data ingestion, validation, and upload.

Attributes:
    config (dict): Dictionary containing data ingestion, validation, and upload configuration settings.
    schema (dict): Dictionary containing schema configuration settings.
    params (dict): Dictionary containing parameters required for configuration settings.

Methods:
    get_data_ingestion_config(): Retrieves data ingestion configuration settings.
    get_data_validation_config(): Retrieves data validation configuration settings.
    get_data_upload_config(): Retrieves data upload configuration settings.
"""
class ConfigurationManager:
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        schema_filepath=SCHEMA_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH):
        """
        Initializes ConfigurationManager with provided filepaths.

        Args:
            config_filepath (str): Filepath to configuration file. Defaults to CONFIG_FILE_PATH.
            schema_filepath (str): Filepath to schema file. Defaults to SCHEMA_FILE_PATH.
            params_filepath (str): Filepath to parameters file. Defaults to PARAMS_FILE_PATH.
        """
        self.config = read_yaml(config_filepath)
        self.schema = read_yaml(schema_filepath)
        self.params = read_yaml(params_filepath)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Retrieves data ingestion configuration settings.

        Returns:
            data_ingestion_config (DataIngestionConfig): Data ingestion configuration object.
        """
        config = self.config.data_ingestion
        text_spliter = self.params.TEXT_SPLITER

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            load_dir=config.load_dir,
            text_spliter_config=text_spliter
        )

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Retrieves data validation configuration settings.

        Returns:
            data_validation_config (DataValidationConfig): Data validation configuration object.
        """
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            read_data_dir=config.read_data_dir,
            STATUS_FILE=config.STATUS_FILE,
            SCHEMA=schema
        )

        return data_validation_config

    def get_data_upload_config(self) -> DataUploadConfig:
        """
        Retrieves data upload configuration settings.

        Returns:
            data_upload_config (DataUploadConfig): Data upload configuration object.
        """
        config = self.config.data_load
        index_info = self.params.INDEX_INFO
        batch_size = self.params.BATCH_SIZE

        create_directories([config.root_dir])

        data_upload_config = DataUploadConfig(
            root_dir=config.root_dir,
            read_data_dir=config.read_data_dir,
            STATUS_FILE=config.STATUS_FILE,
            index_info=index_info,
            batch_size=batch_size
        )

        return data_upload_config