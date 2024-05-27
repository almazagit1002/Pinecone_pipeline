from vector_db_pipeline.constants import * 
from vector_db_pipeline.utils.common import read_yaml, create_directories, load_json, load_set, list_files
from vector_db_pipeline import logger
import os
import json
from hashlib import md5
from pathlib import Path
from vector_db_pipeline.entity.config_entity import ConfigFileChanges

"""
A class to monitor and manage the state of files in a directory.

Attributes:
    config (ConfigFileChanges): Configuration object containing paths and file monitoring settings.
    dir_to_monitor (str): Directory path to monitor for file changes.
    state_file (str): File path to save the state of monitored files.
    app_files (set): Set of files to monitor in the specified directory.

Methods:
    get_file_md5(file_path): Computes the MD5 hash of a file.
    save_directory_state(): Saves the current state of the monitored directory to a file.
    load_directory_state(state_file): Loads the state of the monitored directory from a file.
    compare_states(old_state, new_state): Compares old and new directory states and classifies changes.
    monitor_directory(): Monitors the directory and reports changes.
"""


class FilesState:
    def __init__(self, config:ConfigFileChanges):
        self.config = config
        self.dir_to_monitor = config.dir_to_monitor
        self.state_file = config.state_file
        self.app_files = load_set(Path(self.config.monitor_files))


    @staticmethod
    def get_file_md5(file_path):
        """
        Compute the MD5 hash of the file.

        Args:
            file_path (str): Path of the file to compute the MD5 hash for.

        Returns:
            str: MD5 hash of the file.
        """
        hasher = md5()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()


    def save_directory_state(self):
        """
        Save the current state of the directory to a file.

        This method computes the MD5 hashes of the monitored files and saves the current state
        to the specified state file in JSON format.
        """
        current_state = {}
       
        for file in self.app_files:
            current_state[file] = self.get_file_md5(file)
        with open(self.state_file, 'w') as f:
            json.dump(current_state, f, indent=4)

    @staticmethod
    def load_directory_state(state_file):
        """
        Load the directory state from a file.

        Args:
            state_file (str): Path of the file to load the directory state from.

        Returns:
            dict: Dictionary representing the state of the directory.
        """
        if not os.path.exists(state_file):
            return {}
        with open(state_file, 'r') as f:
            return json.load(f)


    def compare_states(self,old_state, new_state):
        """
        Compare the old and new directory states and classify changes.

        This method identifies added, deleted, and changed files between the old and new states
        and saves these changes to the specified updated files path in JSON format.

        Args:
            old_state (dict): The old state of the directory.
            new_state (dict): The new state of the directory.
        """
        old_files = set(old_state.keys())
        new_files = set(new_state.keys())

        added_files = new_files - old_files
        deleted_files = old_files - new_files
        common_files = old_files & new_files

        changed_files = {
            file for file in common_files if old_state[file] != new_state[file]
        }
        

        changes = {
            'added_files': list(added_files),
            'deleted_files': list(deleted_files),
            'changed_files': list(changed_files),
        }

        with open(self.config.updated_files, 'w') as f:
            json.dump(changes, f, indent=4)

       

    def monitor_directory(self):
        """
        Monitor the directory and report changes.

        This method loads the old state of the directory, computes the new state,
        compares the two states to identify changes, and saves the updated state.
        """
        old_state = self.load_directory_state(self.state_file)
        new_state = {}
 
        for file in self.app_files:
            new_state[file] = self.get_file_md5(file)
    
 

        self.compare_states(old_state, new_state)
        self.save_directory_state()



