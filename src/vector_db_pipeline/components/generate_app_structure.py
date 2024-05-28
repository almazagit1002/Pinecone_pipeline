from vector_db_pipeline.entity.config_entity import CodeStructureConfig
from vector_db_pipeline.constants import *
from vector_db_pipeline.utils.common import  save_json, save_set
from vector_db_pipeline import logger
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
load_dotenv()

import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Code_structure_main"


"""
A class for managing code structure and formatting.

Attributes:
    config (CodeStructureConfig): Configuration object for the CodeStructure class.

Functions:
    get_ignored_subdirs_from_gitignore: Reads ignored directories and extensions from a .gitignore file.
    explore_directory: Explores directories and files, excluding ignored ones.
    build_directory_structure: Builds the directory structure recursively.
    get_formated_strcuture: Formats the directory structure using an AI model.
"""

class CodeStructure:
    def __init__(self, config:CodeStructureConfig):
        """
        Initializes the CodeStructure object with the given configuration.

        Args:
            config (CodeStructureConfig): Configuration object for the CodeStructure class.
        """        
        self.config = config        

    def get_ignored_dirs(self):
        """
        Reads ignored directories and extensions from a .gitignore file and from exhalation_ignnore file.

        Returns:
            None
        """
        ignore_subdirs_files = []
        ignore_subdirs_files_extentions = []
        gitignore_path = self.config.gitignore_path
        ignored_fles_path = self.config.load_ignored_dir
        files_to_ignore = self.config.files_to_ignore
        try:
            with open(gitignore_path, "r") as file:
                for i,line in enumerate(file):
                    # Skip comments and empty lines
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    else:
                        if line.startswith("*"):
                            if line.endswith("/"):
                                ignore_subdirs_files_extentions.append(line[1:-1])
                            else:
                                ignore_subdirs_files_extentions.append(line[1:])
                        else:
                            if line.endswith("/"):
                                ignore_subdirs_files.append(line[:-1])
                            elif line.endswith("*"):
                                ignore_subdirs_files.append(line[:-2])
                            
                            else:
                                ignore_subdirs_files.append(line)
            logger.info(f"Files to ignore obtained from: {gitignore_path} and exhalation_ignore")
        except FileNotFoundError:
            return logger.error(f"Warning: {gitignore_path} not found.")
        except Exception as e:
            return logger.error(f"Error while reading {gitignore_path}: {e}")

        self.ignored_subdirs = set(ignore_subdirs_files)
        #adding files to ignore from exhalation_ignore
        self.ignored_subdirs.update(files_to_ignore)
        self.ignored_extensions = set(ignore_subdirs_files_extentions)
        try:
            all_ignored_files = self.ignored_subdirs.union(self.ignored_extensions)
            logger.info(f"Set of files to ignore created")
            save_set(Path(ignored_fles_path),all_ignored_files)

           
            return all_ignored_files
      
        except Exception as e:
            return logger.error(f"Error while loading ignored files to {ignored_fles_path}: {e}")
        

        
    
    def explore_directory(self,directory):
        """
        Explores directories and files, excluding ignored ones.

        Args:
            directory (str): Path to the directory to explore.

        Returns:
            dict: A dictionary containing the list of directories and files.
        """
        directories = []
        files = []
        for item in os.listdir(directory):
            if item not in self.ignored_subdirs and not item.endswith(tuple(self.ignored_extensions)):
                item_path = os.path.join(directory, item)

                if os.path.isdir(item_path):
                    directories.append(item)
                else:
                    files.append(item)

        return {'Directories': directories, 'Files': files}

    def build_directory_structure(self):
        """
        Builds the directory structure recursively.

        Returns:
            dict: A dictionary representing the directory structure.
        """
        directory_structure = {}
        root_directory = self.config.code_dir
        dir_structure_file = self.config.load_struct_dir
        def explore_and_build(directory):
            dir_path = os.path.join(root_directory, directory)
            directory_structure[directory] = self.explore_directory(dir_path)
            
            for subdir in directory_structure[directory]['Directories']:
                explore_and_build(os.path.join(directory, subdir))
        
        explore_and_build(root_directory)
        
        
        save_json(Path(dir_structure_file), directory_structure)
        logger.info(f"Directory structure loaded to {dir_structure_file}")
        return  directory_structure

    def get_formated_strcuture(self, directory_structure):
        """
        Formats the directory structure using an AI model.

        Args:
            directory_structure (dict): The directory structure to format.

        Returns:
            None
        """
        try:
            formated_structure_file = self.config.sructure_file
            model = self.config.models.Llama3
            logger.info(f"Working with model: {model}")
            chat = ChatGroq(temperature=0, model_name=model)
            file_structure_prompt = self.config.structure_prompt
            prompt = ChatPromptTemplate.from_messages([("human", file_structure_prompt)])
            chain = prompt | chat
            fromated_structure = chain.invoke({"JSON_FILE": directory_structure})
            with open(formated_structure_file, "w") as f:
                f.write(fromated_structure.content)
            # return logger.info(f"Formated file structure loaded to : {formated_structure_file}")
        except Exception as e:
            return logger.error(f"Error while formating structure: {e}")

