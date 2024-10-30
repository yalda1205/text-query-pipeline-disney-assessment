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

## Requirements

`requirements.txt` includes:
- `flask`
- `sentence-transformers`
- `faiss-cpu`
- `numpy`
- `pandas`

## Files

- **`data.csv`**: CSV file with unstructured data (e.g., `description` column). Place `data.csv` in the same directory as `data_pipeline.py`, or modify the file path in the code if located elsewhere.

## Running the Project

1. ### Run `data_pipeline.py`:

- This script will create `data_assessment.db` and `vector_index.faiss`, which the API will use.

```bash
python data_pipeline.py
```
2. ### Run `app.py`:
- After creating the database and FAISS index, start the Flask API.

```bash
python app.py
```

3. ### Test the API:
- The Flask API will start at `http://127.0.0.1:5000`
- Send a POST request to `http://127.0.0.1:5000/query` with a JSON payload:

```json
{
 "query": "your query text here"
}
```

