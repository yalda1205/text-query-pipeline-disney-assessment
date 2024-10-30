# Data Pipeline and API for Text Querying and Retrieval with Embedding-based Similarity

## Overview

This project implements a data pipeline and an API that:
1. **Ingests** and preprocesses data from a CSV file.
2. **Stores** the data in an SQLite database with optimized indexing.
3. **Embeds** text data using Sentence-BERT for similarity search.
4. **Indexes** these embeddings with FAISS for efficient retrieval.
5. **Provides** a Flask API for querying similar records based on text input.

The solution is designed to handle large datasets through batch processing, with logging for monitoring and easy scalability.

## Contents

- `data_pipeline.py`: Main script for data ingestion, preprocessing, and FAISS indexing.
- `app.py`: Flask API to handle queries based on text prompts and retrieve similar records.
- `README.md`: Documentation and setup instructions.
- `requirements.txt`: List of dependencies for easy setup.

## Getting Started

### Prerequisites

- Python 3.x
- Required packages (install using):
  ```bash
  pip install -r requirements.txt

requirements.txt includes:
flask
sentence-transformers
faiss-cpu
numpy
pandas
