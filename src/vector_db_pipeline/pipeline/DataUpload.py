from vector_db_pipeline.config.configuration import ConfigurationManager
from vector_db_pipeline.components.data_load import DataUpload
from vector_db_pipeline import logger

STAGE_NAME = "Data Upload stage"

class DataUploadPipeline:
    def __init__(self, should_restart_database=False):
        """
        Initializes the DataUploadPipeline.

        Retrieves data upload configuration using ConfigurationManager.
        """
        self.config_manager = ConfigurationManager()
        self.data_upload_config = self.config_manager.get_data_upload_config()
        self.should_restart_database = should_restart_database

    def restart_database(self):
        """
        Restarts the database by deleting and recreating the index.

        Deletes the existing index and recreates it to start fresh.
        """
        data_upload = DataUpload(config=self.data_upload_config)
        data_upload.del_index()
        data_upload.recreate_index()

    def main(self):
        """
        Executes the data upload pipeline.

        Initializes DataUpload with data upload configuration.
        Generates Pinecone vectors from the input data.
        Uploads vectors to the Pinecone index in batches.
        """
        # Initialize DataUpload with data upload configuration
        data_upload = DataUpload(config=self.data_upload_config)
        
        # Restart the database if needed
        if self.should_restart_database:
            logger.info(f"Restarting database")
            self.restart_database()

        # Generate Pinecone vectors from the input data
        pinecone_vector = data_upload.pinecon_vector()
        
        # Upload vectors to the Pinecone index in batches
        data_upload.batch_upload(pinecone_vector)


if __name__ =='__main__':
    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = DataUploadPipeline(should_restart_database=True)
        obj.restart_database()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

    except Exception as e:
        logger.exception(e)
        raise(e)