from vector_db_pipeline.constants import *
from vector_db_pipeline.utils.common import read_yaml, create_directories
from vector_db_pipeline.entity.config_entity import (DataIngestionConfig,
                                                     DataValidationConfig,
                                                     DataUploadConfig,
                                                     CodeStructureConfig,
                                                     JsonSummaryConfig,
                                                     EditSummaryConfig,
                                                     ConfigFileChanges)


"""
Manages configuration settings for data ingestion, validation, upload, code structure, and additional configurations.

Attributes:
    config (dict): Dictionary containing data ingestion, validation, upload, and code structure configuration settings.
    schema (dict): Dictionary containing schema configuration settings.
    params (dict): Dictionary containing parameters required for configuration settings.
    models (dict): Dictionary containing model configuration settings.
    prompt_template (dict): Dictionary containing prompt template configuration settings.

Methods:
    get_data_ingestion_config(): Retrieves data ingestion configuration settings.
    get_data_validation_config(): Retrieves data validation configuration settings.
    get_data_upload_config(): Retrieves data upload configuration settings.
    get_code_structure_config(): Retrieves code structure configuration settings.
    get_json_summary_config(): Retrieves JSON summary processing configuration settings.
    get_edit_summary_config(): Retrieves edited JSON summary configuration settings.
    get_file_changes_config(): Retrieves file changes monitoring configuration settings.
"""
class ConfigurationManager:
    def __init__( self,
        config_filepath = CONFIG_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        models_filepath = MODELS_FILE_PATH,
        prompt_template = PROMPT_FILE_PATH,
        files_to_ignore = IGNORE_FILE_PATH):
        """
        Initializes ConfigurationManager with provided filepaths.

        Args:
            config_filepath (str): Filepath to configuration file. Defaults to CONFIG_FILE_PATH.
            schema_filepath (str): Filepath to schema file. Defaults to SCHEMA_FILE_PATH.
            params_filepath (str): Filepath to parameters file. Defaults to PARAMS_FILE_PATH.
            models_filepath (str): Filepath to models file. Defaults to MODELS_FILE_PATH.
            prompt_template (str): Filepath to prompt template file. Defaults to PROMPT_FILE_PATH.
        """
        self.config = read_yaml(config_filepath)
        self.schema = read_yaml(schema_filepath)
        self.params = read_yaml(params_filepath)
        self.models = read_yaml(models_filepath)
        self.prompt_template = read_yaml(prompt_template)
        self.files_to_ignore = read_yaml(files_to_ignore)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Retrieves data ingestion configuration settings.

        Returns:
            data_ingestion_config (DataIngestionConfig): Data ingestion configuration object.
        """
        config = self.config.data_ingestion
        text_spliter = self.params.TEXT_SPLITER
        namespace = self.params.INDEX_INFO.NAMESPACE

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            load_dir=config.load_dir,
            text_spliter_config=text_spliter,
            namespace_idx = namespace
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
    
    def get_code_structure_config(self) -> CodeStructureConfig:
        """
        Generates a CodeStructureConfig object based on the provided configuration.

        Returns:
            CodeStructureConfig: The generated configuration object.
        """
        # Get the configuration from the main configuration object
        config = self.config.code_structure
        
        # Generate the file structure prompt template
        prompt_teplate = self.prompt_template.generate_file_structure
        
        # Create necessary directories
        create_directories([config.root_dir])
        
        # Create a CodeStructureConfig object with the specified parameters
        code_structure_config = CodeStructureConfig(
            root_dir=config.root_dir,
            load_struct_dir = config.load_struct_dir,
            load_ignored_dir = config.load_ignored_dir,
            gitignore_path = config.gitignore_path,
            code_dir = config.code_dir,
            sructure_file=config.sructure_file,
            save_files_to_read = config.save_files_to_read,
            models = self.models,
            structure_prompt = prompt_teplate.description,
            files_to_ignore = self.files_to_ignore.IGNORE_FILES
            
        ) 

        return code_structure_config
    def get_json_summary_config(self) -> JsonSummaryConfig:
        """
        Retrieves the configuration settings for JSON summary processing.

        This method reads the configuration settings from the class instance's config attribute,
        creates necessary directories, and initializes a JsonSummaryConfig object with the 
        retrieved settings.

        Returns:
            JsonSummaryConfig: An object containing configuration settings for JSON summary processing.
        """
        config = self.config.json_summary
        create_directories([config.root_dir])
        
        json_summary_config = JsonSummaryConfig(
            root_dir=config.root_dir,
            read_schema = config.read_schema,
            load_json_summary = config.load_json_summary,
            prompt_generate_json_summary = self.prompt_template.generate_json_summary,
            models = self.models,
            
        ) 

        return json_summary_config


    def get_edit_summary_config(self) -> EditSummaryConfig:
        """
        Create and return an EditSummaryConfig object based on the current configuration.

        This function retrieves the configuration related to the edited JSON summary, 
        creates an EditSummaryConfig object with the relevant settings, and returns it.

        Returns:
            EditSummaryConfig: The configuration object for editing the JSON summary.
        """
       
        config = self.config.edited_json_summary
        edit_summary_config = EditSummaryConfig(
            read_json_summary=config.read_json_summary,
            load_edited_summary = config.load_edited_summary
        
        ) 

        return edit_summary_config
    
    def get_file_changes_config(self) -> ConfigFileChanges:
        """
        Retrieves file changes monitoring configuration settings.

        Returns:
            file_changes_config (ConfigFileChanges): Configuration object for monitoring file changes.
        """
        config = self.config.file_changes
       
        create_directories([config.state_root])

        file_changes_config = ConfigFileChanges(
            dir_to_monitor = config.dir_to_monitor,
            state_file = config.state_file,
            updated_files = config.updated_files,
            monitor_files = config.monitor_files
        )

        return file_changes_config