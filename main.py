from vector_db_pipeline import logger
from vector_db_pipeline.pipeline.DataIngestion import DataIngestionPipeline
from vector_db_pipeline.pipeline.DataValidation import DataValidationPipeline
from vector_db_pipeline.pipeline.DataUpload import DataUploadPipeline
from vector_db_pipeline.utils.common import read_yaml
from vector_db_pipeline.constants import *




STAGE_NAME = "Data Ingestion stage"
try:
    logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

except Exception as e:
    logger.error(e)
    raise(e)


STAGE_NAME = "Data Validation stage"

try:
    logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
    data_val = DataValidationPipeline()
    data_val.main()
    logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

except Exception as e:
    logger.error(e)
    raise(e)

STAGE_NAME = "Data Upload stage"

try: 
    params = read_yaml(PARAMS_FILE_PATH)
    delete_vector_database = params.DELETE_DATABSE.DELETE_DATABSE
    logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
    data_upload = DataUploadPipeline(should_restart_database=delete_vector_database)
    data_upload.main()
    logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

except Exception as e:
    logger.error(e)
    raise(e)