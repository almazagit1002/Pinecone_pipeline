from vector_db_pipeline.config.configuration import ConfigurationManager
from vector_db_pipeline.components.generate_metadata import JsonSummary
from vector_db_pipeline import logger
from vector_db_pipeline.utils.common import  load_set
from vector_db_pipeline.entity.config_entity import GraphState

from langgraph.graph import StateGraph
import time
from pathlib import Path

STAGE_NAME = "Generate files summary stage"


class GenerateJsonSummaryPipeline:
    """
    A class to manage the pipeline for generating JSON summaries.

    Methods:
        main(): Executes the main pipeline to generate the JSON summary.
    """
    def __init__(self):
        """
        Initializes the GenerateJsonSummaryPipeline class.
        """
        pass

    def main(self):
        """
        Executes the main pipeline to generate the JSON summary.

        This method performs the following steps:
        1. Initializes the configuration manager and retrieves the JSON summary configuration.
        2. Loads the set of files to be processed.
        3. Configures the model system for generating JSON summaries.
        4. Creates and runs the agent workflow for generating JSON summaries.

        Returns:
            None
        """
        json_summary_config = ConfigurationManager()
        config_json = json_summary_config.get_json_summary_config()
        files_in_app = list(load_set(Path(config_json.read_schema)))

        generate_json_summary = JsonSummary(config_json)

        generate_json_summary.configure_model_system()
        app = generate_json_summary.create_graph_agents(StateGraph(GraphState))
        generate_json_summary.run_graph_agents(app, files_in_app)


if __name__ =='__main__':
    try:
        start = time.time()
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = GenerateJsonSummaryPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed in  {(time.time() - start):.4f} seconds<<<<<<<<<<<<\n\nx===============x")



    except Exception as e:
        logger.exception(e)
        raise(e)