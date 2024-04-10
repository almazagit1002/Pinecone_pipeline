# Pinecone_pipeline

## Workflows

1. Update config.yaml
2. Update schema.yaml
3. Update params.yaml
4. Update the entity in src\mlProject\entity\config_entity.py
5. Update the configuration manager in src\mlProject\config\configuration.py
6. Update the components in src\mlProject\components
7. Update the pipeline in src\mlProject\pipeline
8. Update the main.py
9. Update the app.py

## Prerequisites
Before running the FastAPI API and client examples, make sure you have the following installed:

Python (version >= 3.6)
Installation
Clone the Repository:

```bash
git clone https://github.com/almazagit1002/Pinecone_pipeline.git
```
Navigate to the Project Directory:

```bash
cd Pinecone_pipeline
```
## Set Up Python Virtual Environment (Optional but Recommended):

```bash
python3 -m venv venv
.\venv\Scripts\activate
```

## Set up enviroments variables
create an .env file and add the following api keys:

* OPENAI_API_KEY=..... 
* PINECONE_API_KEY=....


Alternatively go to enviroment variables in your loca machine click in create new and insert your API keys. 

## Install Dependencies:

```bash
pip install -r requirements.txt
```

## Sytem Summary
The system automates the process of ingesting raw data, validating its integrity, and uploading it to pinecone, making it suitable for data preprocessing and analysis tasks in various domains such as natural language processing, data mining, and machine learning.

## Uscases
* Data Ingestion Stage:
    * Use Case: Ingesting raw data from various sources (e.g., JSON files) into the system for further processing.
    * Implementation: The DataIngestionPipeline class handles data ingestion tasks by retrieving configuration, parsing JSON files, processing text data, and     saving processed data into CSV files.

* Data Validation Stage:
    * Use Case: Ensuring the quality and integrity of the ingested data before further processing or analysis.
    * Implementation: The DataValidationPipeline class performs data validation checks such as column presence and uniqueness to validate the structure and integrity of the data.

* Data Upload Stage:
    * Use Case: Uploading processed data to a database or indexing system for storage and retrieval.
    * Implementation: The DataUploadPipeline class handles data upload tasks by generating Pinecone vectors from processed data and uploading them to the Pinecone index in batches. It also provides an option to restart the database if needed.

## Example
Use data from 'Data' directory
