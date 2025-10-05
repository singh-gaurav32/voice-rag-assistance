# app/services/rag_service.py

from threading import Lock
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import FAISS_INDEX_PATH, FAISS_METADATA_PATH
import asyncio
from app.services.logger_service import LoggerService
import os
import glob

logger = LoggerService() 

from enum import Enum

class EmbeddingModels(str, Enum):
    MINI_LM = "all-MiniLM-L6-v2"
    PARAPHRASE_MPNET = "paraphrase-mpnet-base-v2"



class RAGService:
    """
    Singleton service for Retrieval-Augmented Generation (RAG)
    using FAISS for vector search and SentenceTransformer for embeddings.
    Supports async embedding computation to avoid blocking FastAPI event loop.
    """

    _instance = None
    _lock = Lock()

    def __init__(self):
        """Initialize FAISS index, metadata, and embedding model."""
        import time
        start = time.time()
        self.model = SentenceTransformer(EmbeddingModels.MINI_LM, device="cpu")
        end = time.time()
        logger.log(f"[INFO] Loaded embedding model in {end-start:.3f} seconds")
        
        if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_METADATA_PATH):
            self.index = faiss.read_index(FAISS_INDEX_PATH)
            with open(FAISS_METADATA_PATH, "rb") as f:
                self.chunks = pickle.load(f)
            logger.log(f"[INFO] Loaded FAISS index with {len(self.chunks)} chunks")
        else:
            logger.log("[INFO] FAISS index not found. Ready for ingestion.")

    @classmethod
    def get_instance(cls):
        """Thread-safe singleton getter."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = RAGService()
        return cls._instance

    async def get_embedding_async(self, text: str) -> np.ndarray:
        """
        Compute embedding asynchronously using a thread executor.
        Prevents blocking FastAPI event loop.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.model.encode, text)

    async def retrieve_top_k_async(self, query: str, k: int = 3):
        """
        Retrieve top-k chunks asynchronously.
        Embedding computation is async; FAISS search is synchronous (fast in-memory).
        """
        query_emb = np.array(await self.get_embedding_async(query), dtype="float32").reshape(1, -1)
        D, I = self.index.search(query_emb, k)

        results = []
        for idx in I[0]:
            if idx < 0 or idx >= len(self.chunks):
                continue
            chunk = self.chunks[idx]
            results.append({
                "doc": chunk.get("doc"),
                "chunk_id": chunk.get("chunk_id", -1),
                "text": chunk.get("text", "")
            })
        return results
    
    def ingest_documents(
        self,
        data_dir: str,
        chunk_size: int = 100,
        overlap: int = 20,
        index_path: str = None,
        metadata_path: str = None,
    ):
        from app.config import FAISS_INDEX_PATH, FAISS_METADATA_PATH
        index_path = index_path or FAISS_INDEX_PATH
        metadata_path = metadata_path or FAISS_METADATA_PATH
        documents = []

        for file_path in glob.glob(os.path.join(data_dir, "*")):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                documents.append({"doc": os.path.basename(file_path), "text": text})
                logger.log(f"Loaded document: {os.path.basename(file_path)} ({len(text.split())} words)")

        self.chunks = []
        for doc in documents:
            text = doc["text"]
            start = 0
            chunk_id = 0
            while start < len(text):
                chunk_text = text[start : start + chunk_size]
                self.chunks.append({
                    "doc": doc["doc"],
                    "chunk_id": chunk_id,
                    "text": chunk_text
                })
                start += chunk_size - overlap
                chunk_id += 1
            logger.log(f"Processed document '{doc['doc']}' into {chunk_id} chunks.")

        logger.log(f"Ingested {len(documents)} documents, {len(self.chunks)} chunks created.")

        # Create embeddings
        embeddings = [self.model.encode(c["text"]) for c in self.chunks]
        embeddings = [e.astype("float32") for e in embeddings]

        import numpy as np
        embeddings_matrix = np.array(embeddings)

        # Create FAISS index
        dim = embeddings_matrix.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings_matrix)

        # Save index and metadata
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(self.index, index_path)
        with open(metadata_path, "wb") as f:
            pickle.dump(self.chunks, f)

        logger.log(f"FAISS index saved to {index_path}, metadata saved to {metadata_path}.")


    def append_documents_from_files(self, file_paths: list, chunk_size: int = 100, overlap: int = 20):
        """
        file_paths: list of file paths to text/markdown/json documents.
        Reads, chunks, generates embeddings, and adds to existing FAISS index.
        """
        import os, glob, numpy as np
        logger = LoggerService()

        new_docs = []
        for path in file_paths:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                new_docs.append({"doc": os.path.basename(path), "text": text})
            logger.log(f"Loaded document: {os.path.basename(path)} ({len(text.split())} words)")

        start_chunks = len(self.chunks)
        for doc in new_docs:
            text = doc["text"]
            start = 0
            chunk_id = 0
            while start < len(text):
                chunk_text = text[start : start + chunk_size]
                self.chunks.append({
                    "doc": doc["doc"],
                    "chunk_id": chunk_id,
                    "text": chunk_text
                })
                start += chunk_size - overlap
                chunk_id += 1
            logger.log(f"Appended document '{doc['doc']}' with {chunk_id} chunks.")

        new_embeddings = [self.model.encode(c["text"]).astype("float32") for c in self.chunks[start_chunks:]]
        new_matrix = np.array(new_embeddings)

        if self.index is None:
            import faiss
            dim = new_matrix.shape[1]
            self.index = faiss.IndexFlatL2(dim)

        self.index.add(new_matrix)
        logger.log(f"Added {len(new_matrix)} new chunks to FAISS index.")

