import pandas as pd
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from pathlib import Path
from typing import List
from vector_db_pipeline.entity.config_entity import DataIngestionConfig
from vector_db_pipeline import logger





"""
Processes text data by splitting it into chunks and embedding each chunk.

Attributes:
    config (DataIngestionConfig): Configuration object containing text splitting settings.

Methods:
    get_text_chunks(text: str) -> List[str]: Splits input text into chunks based on configuration settings.
    split_text(data: List[dict]) -> List[dict]: Splits text data in each dictionary entry into chunks and embeds each chunk.
    load_data_csv(splited_text_data: List[dict]): Saves the processed data into a CSV file.
"""
class TextProcessor:
    def __init__(self, config: DataIngestionConfig):
        """
        Initializes TextProcessor with the provided data ingestion configuration.

        Args:
            config (DataIngestionConfig): Configuration object containing text splitting settings.
        """
        self.config = config
        
    def get_text_chunks(self, text: str) -> List[str]:
        """
        Splits input text into chunks based on configuration settings.

        Args:
            text (str): Input text to be split into chunks.

        Returns:
            chunks (List[str]): List of text chunks.
        """
        text_splitter_config = self.config.text_spliter_config
        text_splitter = CharacterTextSplitter(
            separator=text_splitter_config.SEPARATOR.encode().decode('unicode_escape'),
            chunk_size=text_splitter_config.CHUNK_SIZE,
            chunk_overlap=text_splitter_config.CHUNK_OVERLAP,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks

    def split_text(self, data: List[dict]) -> List[dict]:
        """
        Splits text data in each dictionary entry into chunks and embeds each chunk.

        Args:
            data (List[dict]): List of dictionaries containing text data.

        Returns:
            splited_text_data (List[dict]): List of dictionaries containing split and embedded text data.
        """
        embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")
        splited_text_data = []
        idx = 0
        for d in data:
            # Start schema extraction
            text = d.get('text')
            if text:
                timestamp = d.pop('date_scraped_timestamp')
                host = d.pop('host')
                url = d.pop('url')
                page_title = d.pop('page_title')
                # End schema extraction
                
                text_chunks = self.get_text_chunks(text)
                
                embeded_text = embed_model.embed_documents(text_chunks)
                for i, text_chunk in enumerate(text_chunks):
                    emb_vect = {'id': str(timestamp)+'-'+str(idx), 'values': embeded_text[i], 
                                'text': text_chunk, 'host': str(host), 'page_title': str(page_title),
                                'url': str(url)}
                    idx += 1
                    splited_text_data.append(emb_vect)
        logger.info(f"Text processed and chunked. Total chunks: {len(splited_text_data)}")
        return splited_text_data
    
    def load_data_csv(self, splited_text_data: List[dict]):
        """
        Saves the processed data into a CSV file.

        Args:
            splited_text_data (List[dict]): List of dictionaries containing processed text data.
        """
        csv_file_path = Path(self.config.load_dir)
        df = pd.DataFrame(splited_text_data)
        df.to_csv(csv_file_path, index=False)

        logger.info(f"Data processed and saved into CSV file in {csv_file_path}")
