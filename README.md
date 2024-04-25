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

## Generate requiremnets

```bash
pip freeze > requirements.txt
```
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
* GROQ_API_KEY=....


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

* Getting App File Structure Stage:
    * Use Case: This stage involves generating the file structure of the application using language models (like llama3-70b-8192 or mixtral-8x7b-32768), while monitoring token usage, error rates, costs, latency, and other metrics using Langsmith.
    * Implementation: To achieve this, the GenerateAppStructurePipeline class is utilized. This class efficiently generates the file structure of the application in a human-friendly and easily readable format. The output is saved in the structure.txt file.

## Example
Use data from 'Data' directory

## Docker

### Build Docker Image

Use the following command to build the Docker image for the Pinecone Pipeline:
```bash
docker build -t piencone_pipeline_image .
```
This command will build the Docker image using the provided Dockerfile (Dockerfile) in the current directory (.). The -t flag is used to tag the image with the name pinecone_pipeline_image for easy reference.

### Run Docker Container
This command starts a new Docker container named blog_upload from the pinecone_pipeline_image Docker image. The --name flag is used to specify a custom name for the container. The container will execute the command specified in the Dockerfile (CMD ["python3", "main.py"]), which in this case runs the main.py script of the Pinecone Pipeline.

Once the Docker image is built, you can run a Docker container from it using the following command:
```bash
docker run --name blog_upload piencone_pipeline_image
```
Feel free to adjust the container name or image tag as needed. Ensure that you have Docker installed and properly configured on your system before running these commands.

## Possible bug

### Updating Methods and Functions

If you add new methods or functions to any of the files, it's possible that the system may not detect these changes. In such cases, it's recommended to erase your virtual environment (venv), recreate it, and reinstall the requirements. This ensures that any new changes are properly reflected in the environment.

### Managing Database IDs

Pinecone does not provide direct visibility into all the IDs stored in the database. This limitation can make it challenging to add new vectors while continuing with the last ID. However, there's a workaround available. You can modify the namespace parameter in the params.yaml file to a different value. This effectively changes the namespace of the vectors, allowing you to add new vectors without conflicting with existing ones.

