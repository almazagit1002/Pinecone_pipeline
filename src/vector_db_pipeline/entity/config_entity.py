from dataclasses import dataclass
from pathlib import Path
from typing_extensions import TypedDict


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    local_data_file: Path
    load_dir: Path
    text_spliter_config : dict
    namespace_idx:str

    
@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    read_data_dir: Path
    STATUS_FILE: str
    SCHEMA: dict

@dataclass(frozen=True)
class DataUploadConfig:
    root_dir: Path
    read_data_dir: Path
    STATUS_FILE: str
    index_info: dict
    batch_size: int

@dataclass(frozen=True)
class CodeStructureConfig:
    root_dir: Path
    load_struct_dir: Path
    load_ignored_dir: Path
    gitignore_path: Path
    code_dir: Path
    sructure_file: Path
    models: dict
    structure_prompt: str

@dataclass(frozen=True)
class ConfigFileChanges:
    dir_to_monitor: Path
    state_file: Path
    updated_files: Path
    monitor_files: Path

@dataclass(frozen=True)
class EditSummaryConfig:
    read_json_summary: Path
    load_edited_summary: Path

@dataclass(frozen=True)
class GraphState(TypedDict):
    initial_file : str
    draft_json_summary : dict
    json_feedback : dict
    final_json_summary : dict
    num_steps : int

@dataclass(frozen=True)
class JsonSummaryConfig:
    root_dir: Path
    read_schema:Path
    load_json_summary: Path
    prompt_generate_json_summary:dict
    models: dict