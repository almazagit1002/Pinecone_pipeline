from vector_db_pipeline.entity.config_entity import DataUploadConfig
from vector_db_pipeline import logger
from pinecone import Pinecone, PodSpec
import math
import time
import os
from dotenv import load_dotenv
import pandas as pd

"""
Handles data upload to Pinecone indexes.

Attributes:
    config (DataUploadConfig): Configuration object containing settings for data upload.
    params (dict): Dictionary containing parameters required for data upload.

Methods:
    del_index(): Deletes the specified index if it exists.
    recreate_index(): Recreates the index with specified dimensions, metric, and environment.
    pinecon_vector(): Converts data from CSV to a list of JSON objects.
    batch_upload(pinecone_vector): Uploads vectors to a Pinecone index in batches.
"""
class DataUpload:
    def __init__(self, config: DataUploadConfig):
        """
        Initializes DataUpload class with provided configuration and parameters.

        Args:
            config (DataUploadConfig): Configuration object containing settings for data upload.
            params_filepath (str): Filepath to parameters file. Defaults to PARAMS_FILE_PATH.
        """


        self.config = config

        #initialize db
        load_dotenv()
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pc = Pinecone(api_key=pinecone_api_key)
        self.index_info = self.config.index_info
        self.index_name = self.index_info.INDEX_NAME
        
        
     
    def del_index(self):
        """
        Deletes the specified index if it exists.
        """
        if self.index_name in [index_info["name"] for index_info in self.pc.list_indexes()]:
            self.pc.delete_index(self.index_name)
            logger.info(f"Index '{self.index_name}' deleted ")

    def recreate_index(self):
        """
        Recreates the index with specified dimensions, metric, and environment.
        """

        dim = self.index_info.DIMENSIONS
        met = self.index_info.METRIC
        env = self.index_info.ENVIROMENT
        existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]
        
        # Check if index already exists
        if self.index_name not in existing_indexes:
            # Create index if it doesn't exist
            self.pc.create_index(
                name=self.index_name,
                dimension=dim,
                metric=met,
                spec=PodSpec(
                    environment=env
                )
            )
            # Wait for index to be initialized
            while not self.pc.describe_index(self.index_name).status['ready']:
                time.sleep(1)
        index = self.pc.Index(self.index_name)
        logger.info("Index created")
        logger.info(index.describe_index_stats())

    def pinecon_vector(self): 
        """
        Converts data from CSV to a list of JSON objects.

        Returns:
            pinecone_vect (list): List of JSON objects representing each row of the dataframe.
        """
        data_read_path = self.config.read_data_dir
        df = pd.read_csv(data_read_path)
        pinecone_vect = []
        
        for i, row in df.iterrows():
            id = row['id']
            values = row['values'][1:-1].split(',')
            vector_floats = [float(element) for element in values]  #FIX THIS #############################################################
            text = row['text']
            host = row['host']
            page_title = row['page_title']
            url = row['url']
            # Create a dictionary for the metadata containing 'text', 'host', 'page_title', and 'url'
            metadata = {'text': text, 'host': host, 'page_title': page_title, 'url': url}
            # Create a dictionary for the JSON object containing 'id', 'values', and 'metadata'
            emb_vect = {'id': id, 'values': vector_floats, 'metadata': metadata}
            
            pinecone_vect.append(emb_vect)
        logger.info(f"Data ready for upload")
        with open(self.config.STATUS_FILE, 'a') as f:
            f.write(f"Data size: {len(pinecone_vect)}\n")
        # Return the list of JSON objects
        return pinecone_vect

    def batch_upload(self, pinecone_vector):
        """
        Uploads vectors to a Pinecone index in batches.

        Args:
            pinecone_vector (list): List of JSON objects representing vectors to be uploaded.
        """
        # Determine the batch size and total number of data points
        batch_size = self.config.batch_size.BATCH_SIZE 
        
        index = self.pc.Index(self.index_name)
        data_size = len(pinecone_vector)
        
        
        # Calculate the number of batches required
        batch_num = math.ceil(data_size / batch_size)
        logger.info(f"Uploading: {data_size} vectors, in {batch_num} batches")
        
        # Iterate over each batch
        for i in range(batch_num):
 
            try:
                # Calculate the start and end indices for the current batch
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, len(pinecone_vector))
            
                batch_vectors = pinecone_vector[start_idx:end_idx]
                
                # Upload the vectors to the Pinecone index
                index.upsert(vectors=batch_vectors)
                logger.info(f"Batch {i+1} uploaded")
            except Exception as e:
                logger.info(f"Error encountered: {e}")
        
        time.sleep(30)
        logger.info(index.describe_index_stats())
        with open(self.config.STATUS_FILE, 'a') as f:
            f.write(f"Data upload completed\n")
