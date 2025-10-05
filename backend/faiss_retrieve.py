# faiss_retrieve.py

import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import time

# -------------------------------
# Config
# -------------------------------
FAISS_INDEX_PATH = "./data/faiss_index.idx"
METADATA_PATH = "./data/faiss_metadata.pkl"

# -------------------------------
# Load FAISS index and metadata
# -------------------------------
index = faiss.read_index(FAISS_INDEX_PATH)
with open(METADATA_PATH, "rb") as f:
    chunks = pickle.load(f)

# -------------------------------
# Embedding model
# -------------------------------
start_time = time.time()
model = SentenceTransformer("all-MiniLM-L6-v2") 
end_time = time.time()
print(f"[INFO] Loaded embedding model in {end_time - start_time:.3f} seconds")

def get_embedding(text):
    return model.encode(text)

# -------------------------------
# Retrieve top-k chunks
# -------------------------------
def retrieve_top_k(query, k=3):
    query_emb = np.array(get_embedding(query), dtype="float32").reshape(1, -1)
    D, I = index.search(query_emb, k)
    results = []
    for idx in I[0]:
        chunk = chunks[idx]
        results.append({
            "doc": chunk["doc"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"]
        })
    return results

# -------------------------------
# Test retrieval
# -------------------------------
if __name__ == "__main__":
    query = "How long does standard shipping take?"
    start_time = time.time()   
    top_chunks = retrieve_top_k(query, k=1)
    end_time = time.time() 
    elapsed = end_time - start_time
    print(f"[INFO] Retrieval took {elapsed:.3f} seconds\n")
    print(f"\n[INFO] Top chunks for query:\n {query}\n")
    for c in top_chunks:
        print(f"Doc: {c['doc']}, Chunk: {c['chunk_id']}, Length Text: {len(c['text'].split())} words.\n")
        print(c["text"])
        print("-" * 50)
