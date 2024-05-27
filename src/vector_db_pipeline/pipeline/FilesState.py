from vector_db_pipeline.config.configuration import ConfigurationManager
from vector_db_pipeline.components.changes_in_files import FilesState
from vector_db_pipeline import logger
from pathlib import Path

import time

STAGE_NAME = "File state monitor stage"

class FileStatePipeline:
    """
    A class to manage the pipeline for monitoring and recording the state of files in a directory.

    Methods:
        main(): Executes the main pipeline to monitor and record file state changes.
    """

    def __init__(self):
        """
        Initializes the FileStatePipeline class.
        """
        pass

    def main(self):
        """
        Executes the main pipeline to monitor and record file state changes.

        This method performs the following steps:
        1. Initializes the configuration manager and retrieves the file changes configuration.
        2. Creates a FilesState object with the retrieved configuration.
        3. Saves the current state of the directory if the state file does not exist.
        4. Monitors the directory for changes and updates the state file.

        Returns:
            None
        """
        config = ConfigurationManager()
        file_changes_config = config.get_file_changes_config()
        get_file_state = FilesState(file_changes_config)
        if not Path(file_changes_config.state_file).exists():
            get_file_state.save_directory_state()
        get_file_state.monitor_directory()

if __name__ =='__main__':
    try:
        start = time.time()
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = FileStatePipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed in  {(time.time() - start):.4f} seconds<<<<<<<<<<<<\n\nx===============x")



    except Exception as e:
        logger.exception(e)
        raise(e)