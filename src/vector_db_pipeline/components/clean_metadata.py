from vector_db_pipeline.utils.common import load_json ,save_json
from pathlib import Path
from vector_db_pipeline.constants import *
from vector_db_pipeline import logger
from vector_db_pipeline.entity.config_entity import EditSummaryConfig


"""
A class to read, clean, and save edited JSON summaries.

Attributes:
    config (EditSummaryConfig): Configuration object containing paths for reading and saving JSON summaries.

Methods:
    clean_json_summary(): Reads a JSON summary file, filters out entries with empty values, and saves the edited summary.
"""

class EditSummary:
    def __init__(self, config: EditSummaryConfig):
        """
        Initialize the EditSummary class with a configuration object.

        Args:
            config (EditSummaryConfig): Configuration object containing paths for reading and saving JSON summaries.
        """
        self.config = config

    def clean_json_summary(self):
        """
        Read a JSON summary file, filter out entries with empty values, and save the edited summary.

        This function performs the following steps:
        1. Load the JSON summary from the path specified in the configuration.
        2. Filter out entries in each file's summary that have empty values.
        3. Save the edited summary to the path specified in the configuration.

        The resulting edited summary contains only the non-empty entries from the original summary.
        """

        summary = load_json(Path(self.config.read_json_summary))
        
        # Create an edited summary by filtering out entries with empty values
        try:
            
            edited_summary = {file: {key: value for key, value in contents.items() if value}
                            for file, contents in summary.items()}
            logger.info(f"Empty values filtered out")
        except Exception as e:
            logger.error(f"Error filtering out entries with empty values: {e}")
      
        
   
        save_json(Path(self.config.load_edited_summary), edited_summary)



            
    