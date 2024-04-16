from dataclasses import dataclass
from pathlib import Path


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
