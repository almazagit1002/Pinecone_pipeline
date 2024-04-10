from vector_db_pipeline.config.configuration import ConfigurationManager
from vector_db_pipeline.components.data_validation import DataValidation
from vector_db_pipeline import logger


STAGE_NAME = "Data Validation stage"


class DataValidationPipeline:
    def __init__(self):
        pass

    def main(self):
        """
        Executes the data validation pipeline.

        Instantiates the ConfigurationManager to retrieve data validation configuration.
        Initializes DataValidation with the retrieved configuration.
        Executes data validation checks.
        """
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()
        data_validation.validate_unique_index()


if __name__ =='__main__':
    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = DataValidationPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

    except Exception as e:
        logger.exception(e)
        raise(e)