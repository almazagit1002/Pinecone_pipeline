from vector_db_pipeline import logger
from vector_db_pipeline.pipeline.GenerateAppStructure import GenerateAppStructurePipeline
from vector_db_pipeline.pipeline.JsonSummary import GenerateJsonSummaryPipeline
from vector_db_pipeline.pipeline.EditSummary import CleanJsonSummaryPipeline
from vector_db_pipeline.pipeline.FilesState import FileStatePipeline


import time

MAIN_STAGE = "Main exhalation"
main_start = time.time()
logger.info(f">>>>>>> Stage {MAIN_STAGE} started <<<<<<<<<<<<")

STAGE_NAME = "Getting App File Structure"

try:
    start = time.time()
    logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<<<")
    obj = GenerateAppStructurePipeline()
    obj.main()
    logger.info(f">>>>>>> Stage {STAGE_NAME} completed in  {(time.time() - start):.4f} seconds <<<<<<<<<<<<\n\nx===============x")

except Exception as e:
    logger.exception(e)
    raise(e)


STAGE_NAME = "Generate files summary"

try:
    start = time.time()
    logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<<<")
    obj = GenerateJsonSummaryPipeline()
    obj.main()
    logger.info(f">>>>>>> Stage {STAGE_NAME} completed in  {(time.time() - start):.4f} seconds <<<<<<<<<<<<\n\nx===============x")



except Exception as e:
    logger.exception(e)
    raise(e)

STAGE_NAME = "Clean summary"

try:
    start = time.time()
    logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<<<")
    obj = CleanJsonSummaryPipeline()
    obj.main()
    logger.info(f">>>>>>> Stage {STAGE_NAME} completed in  {(time.time() - start):.4f} seconds <<<<<<<<<<<<\n\nx===============x")



except Exception as e:
    logger.exception(e)
    raise(e)

STAGE_NAME = "File state monitor"

try:
    start = time.time()
    logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<<<")
    obj = FileStatePipeline()
    obj.main()
    logger.info(f">>>>>>> Stage {STAGE_NAME} completed in  {(time.time() - start):.4f} seconds <<<<<<<<<<<<\n\nx===============x")



except Exception as e:
    logger.exception(e)
    raise(e)


logger.info(f">>>>>>> Stage {MAIN_STAGE} completed in  {(time.time() - main_start):.4f} seconds <<<<<<<<<<<<\n\nx===============x")