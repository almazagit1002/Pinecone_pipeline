from vector_db_pipeline.config.configuration import ConfigurationManager
from vector_db_pipeline.components.data_ingestion import TextProcessor
from vector_db_pipeline.utils.common import list_files_in_directory, get_json
from vector_db_pipeline import logger
from pathlib import Path


STAGE_NAME = "Data Ingestion stage"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        """
        Executes the data ingestion pipeline.

        Retrieves data ingestion configuration from ConfigurationManager.
        Retrieves JSON files from the local data directory specified in the configuration.
        Parses JSON files to extract data.
        Initializes TextProcessor with data ingestion configuration.
        Splits text data into chunks and embeds them.
        Saves the processed data into a CSV file.
        """
        # Retrieve data ingestion configuration
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        
        # Get JSON files from local data directory
        json_files = list_files_in_directory(Path(data_ingestion_config.local_data_file))
        
        # Parse JSON files to extract data
        data = get_json(json_files)
        
        # Initialize TextProcessor with data ingestion configuration
        text_processor = TextProcessor(config=data_ingestion_config)
        
        # Split text data into chunks and embed them
        splited_text_data = text_processor.split_text(data)
        
        # Save the processed data into a CSV file
        text_processor.load_data_csv(splited_text_data)



if __name__ =='__main__':
    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

    except Exception as e:
        logger.exception(e)
        raise(e)