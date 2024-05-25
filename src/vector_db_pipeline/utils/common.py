import os
from box.exceptions import BoxValueError
import yaml
from vector_db_pipeline import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any, List



@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    

    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Create a list of directories if they do not exist.

    Args:
        path_to_directories (list): List of paths of directories.
        verbose (bool, optional): Whether to log messages. Defaults to True.
    """
    for path in path_to_directories:
        if not os.path.exists(path):  # Check if directory already exists
            os.makedirs(path, exist_ok=True)
            if verbose:
                logger.info(f"Created directory at: {path}")
        elif verbose:
            logger.info(f"Directory already exists: {path}")



@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")




@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data



@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


@ensure_annotations
def get_json(json_files: List) -> List:
    """
    Load data from JSON files and return as a ConfigBox object.

    Args:
        json_files (List[str]): List of paths to JSON files.

    Returns:
        ConfigBox: Data as class attributes instead of dict.
    """
    # Initialize an empty list to store data from JSON files
    all_data = []

    # Iterate through each JSON file
    for json_file in json_files:
        # Open the JSON file
        with open(json_file, 'r', encoding='utf-8') as file:
            # Load the JSON data
            data = json.load(file)
        # Append the loaded data to the list
        all_data.append(data)
    
    # Flatten the list of lists into a single list
    flattened_list = [item for sublist in all_data for item in sublist]
    
    # Log a message indicating successful loading of JSON files
    logger.info(f"JSON files loaded successfully from: {json_files}")
    
    # Return the data as a ConfigBox object
    return flattened_list

@ensure_annotations
def list_files_in_directory(path: Path) -> List:
    """
    List files in a directory and its subdirectories.

    Args:
        path (Path): Path to the directory.

    Returns:
        List[str]: List of file paths.
    """
    scraped_files = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            scraped_files.append(file_path)
    logger.info(f"Files list successfully loaded from: {path}")
    return scraped_files


def get_column_types(df) -> dict:
    """
    Get the types of values in each column of the DataFrame.

    Args:
        df (DataFrame): The input DataFrame.

    Returns:
        dict: A dictionary where keys are column names and values are lists containing the types of values present in each column.
    """

    column_types = {}
    for column in df.columns:
        # Create a set of unique types for values in the column
        types = set(type(value) for value in df[column])
        # Convert the set to a list for easier handling
        types_list = list(types)
        
        column_types[column] = types_list

    return column_types
@ensure_annotations
def set_to_txt(file_path: Path,set_obj:set):
    with open(file_path, "w") as file:
        # Convert the set elements to strings and write them to the file
        for element in set_obj:
            file.write(str(element) + "\n")
    logger.info(f"Files successfully saved in: {file_path}")


@ensure_annotations
def read_txt(file_path: Path):
    with open(file_path, 'r') as file:
              content = file.read()
    return content
@ensure_annotations
def remove_extension(file_name: Path):
    base_name, extension = os.path.splitext(file_name)
    return base_name

@ensure_annotations
def write_to_txt(file_path: Path, content):
    with open(file_path, 'w') as f:
        f.write(content)

@ensure_annotations
def read_txt_to_list(file_path: Path):
    file_list = []
    with open(file_path, 'r') as file:
        for line in file:
            file_list.append(Path(line.strip()))
    return file_list

@ensure_annotations
def save_set(file_path: Path, file:set):
    with open(file_path, 'w') as f:
        json.dump(list(file), f)
    logger.info(f"Files successfully saved in: {file_path}")


@ensure_annotations
def load_set(file_path: Path):
    with open(file_path, 'r') as file:
        _list = json.load(file)
    

    # Convert the list back to a set
    loaded_set = set(_list)
    logger.info(f"Files successfully loaded from: {file_path}")
    return loaded_set
                

def list_files(directory, exclusions):
    def should_exclude(path, exclusions):
        # Check if the path matches any of the exclusion patterns
        for exclusion in exclusions:
            if exclusion in path:
                return True
            if path.endswith(exclusion):
                return True
        return False

    result = []
    for root, dirs, files in os.walk(directory):
        # Exclude directories from the list
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), exclusions)]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_exclude(file_path, exclusions):
                result.append(file_path)
    return result