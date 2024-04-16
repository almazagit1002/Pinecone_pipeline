FROM python:3.8-slim-buster

RUN apt update -y
WORKDIR /pinecone_pipeline

COPY . /pinecone_pipeline
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]