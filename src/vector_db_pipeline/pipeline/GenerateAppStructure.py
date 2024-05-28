from vector_db_pipeline.config.configuration import ConfigurationManager
from vector_db_pipeline.components.generate_app_structure import CodeStructure
from vector_db_pipeline.utils.common import list_files, save_set
from vector_db_pipeline import logger
from pathlib import Path


STAGE_NAME = "Getting App File Structure stage"

"""
Generates the application structure pipeline.

Methods:
    main(): Main method to execute the pipeline.
"""
class GenerateAppStructurePipeline:
    def __init__(self):
        """
        Initializes the GenerateAppStructurePipeline.
        """
        pass

    def main(self):
        """
        Executes the main pipeline to generate the application structure.

        Returns:
            None
        """
        # Initialize ConfigurationManager
        config = ConfigurationManager()
        code_structure_config = config.get_code_structure_config()
        
        # Get code structure configuration
        code_structure_config = config.get_code_structure_config()
        
        # Initialize CodeStructure with code structure configuration
        get_code_structure = CodeStructure(config=code_structure_config)
        
        # Retrieve ignored subdirectories from .gitignore
        all_ignored_files = get_code_structure.get_ignored_dirs()

        directory_structure = get_code_structure.build_directory_structure()
        

        get_code_structure.get_formated_strcuture(directory_structure)
        

        files_in_app = list_files('.',all_ignored_files)
        save_set(Path(code_structure_config.save_files_to_read),set(files_in_app))


if __name__ =='__main__':
    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = GenerateAppStructurePipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

    except Exception as e:
        logger.exception(e)
        raise(e)