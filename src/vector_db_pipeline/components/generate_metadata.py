from vector_db_pipeline.entity.config_entity import JsonSummaryConfig
from vector_db_pipeline.utils.common import load_json ,save_json, read_file_with_encodings
from pathlib import Path
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from vector_db_pipeline.constants import *
from vector_db_pipeline import logger
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langgraph.graph import END
import os


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Generate_summaries_research_with_agents"

load_dotenv()


"""
A class to generate and manage JSON summaries using various agents and models.

Attributes:
    config (JsonSummaryConfig): Configuration settings for JSON summary processing.

Methods:
    configure_model_system(): Configures the model system with the appropriate agents and prompts.
    generate_json_summary_agent(state): Generates a JSON summary draft from the initial file.
    json_format_route_agent(state): Determines if the JSON draft has the correct format.
    feedback_json(state): Provides feedback for correcting the JSON draft if the format is incorrect.
    no_rewrite(state): Finalizes the JSON draft as the final JSON summary if no corrections are needed.
    edit_file_agent(state): Produces the final JSON summary using the draft and feedback.
    state_printer(state): Prints the current state of the processing.
    create_graph_agents(workflow): Creates and configures the agent workflow graph.
    run_graph_agents(app, file_paths): Runs the agent workflow on a list of file paths to generate JSON summaries.
"""

class JsonSummary:
    """
    A class to generate and manage JSON summaries using various agents and models.

    Attributes:
        config (JsonSummaryConfig): Configuration settings for JSON summary processing.
    """
    def __init__(self, config:JsonSummaryConfig):
        """
        Initializes the JsonSummary class with the provided configuration.

        Args:
            config (JsonSummaryConfig): Configuration settings for JSON summary processing.
        """
        self.config = config

   
    
    def configure_model_system(self):
        """
        Configures the model system with the appropriate agents and prompts.

        This method sets up the models, templates, and agents required for generating,
        validating, and editing JSON summaries.
        """
        model =self.config.models.Llama3
        logger.info(f"Working with model: {model}")
        llm = ChatGroq(temperature=0, model_name=model)
        
        #Agents

        # summary generator agent 
        json_creator_promt = PromptTemplate(
            template= self.config.prompt_generate_json_summary.agent_summary_json_creator,
            input_variables=["content"])
        
        self.json_summary_generator = json_creator_promt | llm | JsonOutputParser()
        
        # analyse summary and decides if it has correct format
        data_type_json_route_prompt = PromptTemplate(
            template= self.config.prompt_generate_json_summary.agent_edit_json_route,
            input_variables=["file"])
        
        self.data_type_json_route_generator = data_type_json_route_prompt | llm | StrOutputParser()

        # if json format is not correct this agent provides feedback for the final editor to aply corrections
        json_feedbak_prompt =  PromptTemplate(
            template= self.config.prompt_generate_json_summary.agent_feedbak_json,
            input_variables=["file"])
        
        self.json_feedbak_generator = json_feedbak_prompt | llm | JsonOutputParser()


        # Final agent produce the final json object using the draft from self.json_summary_generator
        # and the feedback from json_feedbak_generator
        json_editor_prompt =  PromptTemplate(
            template= self.config.prompt_generate_json_summary.agent_rewrite_json,
            input_variables=["file", "feedback"])
        self.json_editor_generator = json_editor_prompt | llm | JsonOutputParser()
        
        
    
    
    def generate_json_summary_agent(self,state):
        """
        Generates a JSON summary draft from the initial file.

        Args:
            state (dict): The current state of the processing, including the initial file and step count.

        Returns:
            dict: Updated state with the draft JSON summary and incremented step count.
        """
        logger.info(f"Creating JSON summary draft")
        initial_file= state['initial_file']
        num_steps = int(state['num_steps'])
        num_steps += 1

        try:
            draft_json_summary = self.json_summary_generator.invoke({"content": initial_file})
        except Exception as e:
            logger.error(f"Error in json summary generator agent: {e}")
        return {"draft_json_summary": draft_json_summary, "num_steps":num_steps}
    
    def json_format_route_agent(self, state):
        """
        Determines if the JSON draft has the correct format.

        Args:
            state (dict): The current state of the processing, including the draft JSON summary and step count.

        Returns:
            str: 'edit_file' if the data type is incorrect, otherwise 'no_edit'.
        """
        logger.info(f"Checking JSON draft data type")
        draft_json_summary = state.get('draft_json_summary')
    
        if draft_json_summary is None:
            logger.error("No draft JSON summary provided.")
            return None

        try:
            summary_type = self.data_type_json_route_generator.invoke({"file": draft_json_summary})
        except Exception as e:
            logger.error(f"Error determining JSON draft data type: {e}")
            return None

        if summary_type == 'text':
            return 'edit_file'
        else:
            return 'no_edit'
        
    def feedback_json(self,state):
        """
        Provides feedback for correcting the JSON draft if the format is incorrect.

        Args:
            state (dict): The current state of the processing, including the draft JSON summary and step count.

        Returns:
            dict: Updated state with the feedback for the JSON draft and incremented step count.
        """

        logger.info(f"JSON draft incorrect.... Producing feedback ")
        draft_json_summary= state['draft_json_summary']
        num_steps = int(state['num_steps'])
        num_steps += 1
        try:
            json_feedback = self.json_feedbak_generator.invoke({"draft_json": draft_json_summary})
        except Exception as e:
            logger.error(f"Error producing fedback: {e}")
      
        return {"json_feedback": json_feedback, "num_steps":num_steps}

    
    def no_rewrite(self,state):
        """
        Finalizes the JSON draft as the final JSON summary if no corrections are needed.

        Args:
            state (dict): The current state of the processing, including the draft JSON summary and step count.

        Returns:
            dict: Updated state with the final JSON summary and incremented step count.
        """

        logger.info("JSON summary draft correct and assigned to final_json_summary")
        ## Get the state
        draft_json_summary = state["draft_json_summary"]
        num_steps = state['num_steps']
        num_steps += 1

        return {"final_json_summary": draft_json_summary, "num_steps":num_steps}
    
    

    def edit_file_agent(self,state):
        """
        Produces the final JSON summary using the draft and feedback.

        Args:
            state (dict): The current state of the processing, including the draft JSON summary, feedback, and step count.

        Returns:
            dict: Updated state with the final JSON summary and incremented step count.
        """
        
        logger.info(f"Acting on feedback and producing final JSON summary")
        draft_json_summary= state['draft_json_summary']
        json_feedback = state['json_feedback']
        num_steps = int(state['num_steps'])
        num_steps += 1
        
        try:
            final_json_summary = self.json_editor_generator.invoke({"file": draft_json_summary, "feedback":json_feedback })
        except Exception as e:
            logger.error(f"Error acting on fedback to generate final json file: {e}")


        return {"final_json_summary": final_json_summary, "num_steps":num_steps}
       
    def state_printer(self,state):
        """
        Prints the current state of the processing.

        Args:
            state (dict): The current state of the processing.
        """
        if state['num_steps'] > 2 :
            logger.info("---STATE PRINTER---")
            logger.info(f"Draft Json Summary Type: {type(state['draft_json_summary'])} \n")
            logger.info(f"Feedback: {state['json_feedback']} \n")
            logger.info(f"Final Json Summary Type: {type(state['final_json_summary'])} \n" )
            logger.info(f"Num Steps: {state['num_steps']} \n")
        else:
            logger.info("---STATE PRINTER---")
            logger.info(f"Draft Json Summary: {type(state['draft_json_summary'])} \n")
            logger.info(f"Final Json Summary: {type(state['final_json_summary'])} \n")
            logger.info(f"Num Steps: {state['num_steps']} \n")
    
    
    
    def create_graph_agents(self, workflow):
        """
        Creates and configures the agent workflow graph.

        Args:
            workflow (Workflow): The workflow object to which nodes and edges will be added.

        Returns:
            CompiledWorkflow: The compiled workflow ready for execution.
        """


        #nodes
        workflow.add_node("generate_json_summary_agent", self.generate_json_summary_agent) 
        workflow.add_node("feedback_json", self.feedback_json)
        workflow.add_node("edit_file_agent", self.edit_file_agent)
        workflow.add_node("no_rewrite", self.no_rewrite)
        workflow.add_node("state_printer", self.state_printer)

        #edges
        workflow.set_entry_point("generate_json_summary_agent")
        workflow.add_conditional_edges(
            "generate_json_summary_agent",
            self.json_format_route_agent,
            {
                "edit_file": "feedback_json",
                "no_edit": "no_rewrite",
            },
        )
        workflow.add_edge("feedback_json", "edit_file_agent")
        workflow.add_edge("no_rewrite", "state_printer")
        workflow.add_edge("edit_file_agent", "state_printer")
        workflow.add_edge("state_printer", END)

        #compile
        try:
            app = workflow.compile()
            logger.info("Agent graph created")
        except Exception as e:
            logger.error(f"Agent graph error: {e}")
             
        return  app
    
    def run_graph_agents(self, app,file_paths):
        """
        Runs the agent workflow on a list of file paths to generate JSON summaries.

        Args:
            app (CompiledWorkflow): The compiled workflow to be executed.
            file_paths (list[Path]): List of file paths to process.

        Returns:
            None
        """
        load_json_file = self.config.load_json_summary
        logger.info(f"Initializing agent summary orquestration")
        batch_size = 5


        batches = [file_paths[i:i + batch_size] for i in range(0, len(file_paths), batch_size)]
        
        for idx, files_batch in enumerate(batches, 1):

            if os.path.exists(Path(load_json_file)):
                json_summaries = load_json(Path(load_json_file))
                logger.info(f"Json summaries readed")
            else:
                json_summaries = {}
                logger.info(f"new Json summaries")
            
            
            logger.info(f"------------------------------Batch: {idx}------------------------------")
            
            for file_path in files_batch:
                logger.info(f"Starting summary of {file_path}")
                file_content = read_file_with_encodings(file_path)

                if len(file_content)>0:
                    filename = os.path.basename(file_path)
                    json_summaries[filename] = {}
                    json_summaries[filename]['FILE_PATH'] = str(file_path)
                    
                    inputs = {"initial_file": file_content,"num_steps":0}
                    try:
                        output = app.invoke(inputs)
                        json_summaries[filename].update(output['final_json_summary'])
                        logger.info(f"{filename} summary success")
                
                    except:
                        logger.error(f"Error in agent graph: {e}")
                   
                else:
                    logger.info(f"{filename} empty.")

            try:
                save_json(Path(load_json_file), json_summaries)
                logger.info(f"JSON summaries loaded to {load_json_file}")
            except Exception as e:
                logger.error(f"Error saving JSON summaries: {e}")
                return batches[idx:]
        
        return logger.info(f"All batches proccessed")



    