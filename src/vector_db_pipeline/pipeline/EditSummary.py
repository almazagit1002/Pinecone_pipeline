from vector_db_pipeline.config.configuration import ConfigurationManager
from vector_db_pipeline.components.clean_metadata import EditSummary
from vector_db_pipeline import logger

import time

STAGE_NAME = "Clean summary stage"

class CleanJsonSummaryPipeline:
    """
    A class to manage the pipeline for cleaning JSON summaries.

    Methods:
        main(): Executes the main pipeline to clean the JSON summary.
    """
    
    def __init__(self):
        """
        Initializes the CleanJsonSummaryPipeline class.
        """
        pass

    def main(self):
        """
        Executes the main pipeline to clean the JSON summary.

        This method performs the following steps:
        1. Initializes the configuration manager and retrieves the edit summary configuration.
        2. Creates an EditSummary object with the retrieved configuration.
        3. Cleans the JSON summary by removing entries with empty values.

        Returns:
            None
        """
        config = ConfigurationManager()
        edit_summary_config = config.get_edit_summary_config()
        edit_summary = EditSummary(edit_summary_config)
        edit_summary.clean_json_summary()


if __name__ =='__main__':
    try:
        start = time.time()
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = CleanJsonSummaryPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed in  {(time.time() - start):.4f} seconds<<<<<<<<<<<<\n\nx===============x")



    except Exception as e:
        logger.exception(e)
        raise(e)