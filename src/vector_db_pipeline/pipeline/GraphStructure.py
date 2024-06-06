from langgraph.graph import StateGraph
import time
from vector_db_pipeline import logger
from vector_db_pipeline.config.configuration import ConfigurationManager
from vector_db_pipeline.components.generate_graph_db_structure import GraphStructure
from vector_db_pipeline.entity.config_entity import GraphSchemaState

STAGE_NAME = "Generate graph data base structure"

class GenetrateGraphStructurePipeline:
    """
    Pipeline class for generating graph structures.

    This class serves as the main entry point for initializing the graph structure
    generation process. It handles the configuration, sets up the necessary agents,
    and runs the workflow to generate and review the graph schema.

    Methods:
        __init__(): Initializes the GenetrateGraphStructurePipeline class.
        main(): Executes the main pipeline process for generating graph structures.
    """

    def __init__(self):
        """
        Initializes the GenetrateGraphStructurePipeline class.
        
        This constructor currently does not take any parameters and does not perform
        any initialization tasks.
        """
        pass

    def main(self):
        """
        Executes the main pipeline process for generating graph structures.
        
        This method performs the following steps:
        1. Initializes the configuration manager and retrieves the graph structure configuration.
        2. Creates an instance of the GraphStructure class with the retrieved configuration.
        3. Sets up the graph schema agents.
        4. Creates the agent workflow and runs it to generate and review the graph schema.
        """
       
        config = ConfigurationManager()
        graph_structure_config = config.get_graph_structure_config()
        graph_structure = GraphStructure(config=graph_structure_config)
        graph_structure.graph_schema_agents()
        app = graph_structure.create_graph_agents(StateGraph(GraphSchemaState))
        graph_structure.run_schema_agents(app)


if __name__ =='__main__':
    try:
        start = time.time()
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = GenetrateGraphStructurePipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed in  {(time.time() - start):.4f} seconds<<<<<<<<<<<<\n\nx===============x")



    except Exception as e:
        logger.exception(e)
        raise(e)