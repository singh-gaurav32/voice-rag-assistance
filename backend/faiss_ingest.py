# faiss_ingest.py

import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# -------------------------------
# Config
# -------------------------------
DATA_DIR = "./data/docs"
FAISS_INDEX_PATH = "./data/faiss_index.idx"
METADATA_PATH = "./data/faiss_metadata.pkl"
CHUNK_SIZE = 200  # words per chunk

# -------------------------------
# Load docs and chunk
# -------------------------------
chunks = []

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".md") or filename.endswith(".txt"):
        path = os.path.join(DATA_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        words = text.split()
        for i in range(0, len(words), CHUNK_SIZE):
            chunk_text = " ".join(words[i:i+CHUNK_SIZE])
            chunks.append({
                "doc": filename,
                "chunk_id": i // CHUNK_SIZE,
                "text": chunk_text
            })

print(f"[INFO] Total chunks created: {len(chunks)}")

# -------------------------------
# Generate embeddings
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return model.encode(text)

# -------------------------------
# Create FAISS index
# -------------------------------
dim = len(get_embedding("test text"))
index = faiss.IndexFlatL2(dim)

for chunk in chunks:
    emb = np.array(get_embedding(chunk["text"]), dtype="float32")
    index.add(emb.reshape(1, -1))

print(f"[INFO] FAISS index contains {index.ntotal} vectors")

# -------------------------------
# Save FAISS index & metadata
# -------------------------------
faiss.write_index(index, FAISS_INDEX_PATH)
with open(METADATA_PATH, "wb") as f:
    pickle.dump(chunks, f)

print(f"[INFO] FAISS index saved to {FAISS_INDEX_PATH}")
print(f"[INFO] Metadata saved to {METADATA_PATH}")
