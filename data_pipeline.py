import pandas as pd
import sqlite3
import logging
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Load and Preprocess Data, then Store in SQLite
def load_and_preprocess_data(csv_file_path='data.csv'):
    """Load, preprocess, and store data in SQLite."""
    try:
        # Load CSV file into a Pandas DataFrame
        data = pd.read_csv(csv_file_path)
        logging.info("Loaded CSV data with %d rows", len(data))

        # Connect to SQLite database and store the raw data in a table
        conn = sqlite3.connect('data_assessment.db')
        data.to_sql('disney_data', conn, if_exists='replace', index=False)
        
        # Create indexes on frequently queried columns
        conn.execute("CREATE INDEX IF NOT EXISTS idx_incident_date ON disney_data (Incident_date);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_theme_park ON disney_data (Theme_Park);")
        conn.commit()

        # Data cleaning
        data['Incident_date'] = pd.to_datetime(data['Incident_date'], errors='coerce')
        data['Theme_Park'] = data['Theme_Park'].str.strip().str.title()
        data['description'] = data['description'].str.strip().str.lower()
        data['description'].fillna("No description available", inplace=True)

        # Store cleaned data
        data.to_sql('disney_data_cleaned', conn, if_exists='replace', index=False)
        logging.info("Data cleaned and stored as disney_data_cleaned.")
        conn.close()

    except FileNotFoundError:
        logging.error("The CSV file was not found. Please ensure 'data.csv' is in the same directory or provide the correct path.")

# Step 2: Vectorization and FAISS Indexing
def create_faiss_index():
    """Generate embeddings and create FAISS index from SQLite data."""
    conn = sqlite3.connect('data_assessment.db')
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding_dim = 384
    index = faiss.IndexFlatL2(embedding_dim)

    batch_size = 100
    offset = 0

    while True:
        query = f"SELECT description FROM disney_data_cleaned LIMIT {batch_size} OFFSET {offset};"
        data = pd.read_sql_query(query, conn)

        if data.empty:
            break

        batch_descriptions = data['description'].tolist()
        batch_embeddings = model.encode(batch_descriptions, convert_to_tensor=False)
        batch_embeddings = np.array(batch_embeddings).astype('float32')
        index.add(batch_embeddings)
        logging.info("Processed and indexed batch at offset %d", offset)
        offset += batch_size

    faiss.write_index(index, 'vector_index.faiss')
    conn.close()

if __name__ == '__main__':
    load_and_preprocess_data()
    create_faiss_index()
    logging.info("Data pipeline completed successfully.")
