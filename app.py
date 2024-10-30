from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import sqlite3
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load FAISS index and Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("vector_index.faiss")  # Ensure this file is created by data_pipeline.py
conn = sqlite3.connect('data_assessment.db', check_same_thread=False)  # Ensure this DB is created by data_pipeline.py

@app.route('/query', methods=['POST'])
def query():
    """API endpoint for retrieving similar records based on a text query."""
    data = request.json
    query_text = data.get('query', '')

    # Generate embedding for query and retrieve similar records
    query_embedding = model.encode([query_text]).astype('float32')
    distances, indices = index.search(query_embedding, k=5)

    # Retrieve corresponding records from SQLite
    record_ids = indices[0]
    retrieved_records = []
    for record_id in record_ids:
        query_sql = f"SELECT * FROM disney_data_cleaned WHERE rowid = {record_id + 1};"
        record = conn.execute(query_sql).fetchone()
        if record:
            retrieved_records.append({
                "Incident_date": record[1],
                "Ride_name": record[2],
                "Theme_Park": record[3],
                "Description": record[6]
            })

    # Create a summary of descriptions for Retriever-Augmented Generation (RAG)
    summary = " ".join([rec["Description"] for rec in retrieved_records])

    # Return query result and summary
    return jsonify({
        "query": query_text,
        "retrieved_records": retrieved_records,
        "summary": summary
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=False)
