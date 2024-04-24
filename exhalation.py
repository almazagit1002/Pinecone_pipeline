from vector_db_pipeline import logger
from vector_db_pipeline.pipeline.GenerateAppStructure import GenerateAppStructurePipeline

STAGE_NAME = "Getting App File Structure stage"

try:
    logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
    obj = GenerateAppStructurePipeline()
    obj.main()
    logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

except Exception as e:
    logger.exception(e)
    raise(e)