import argparse
from app.services.rag_service import RAGService
from app.config import DATA_DIR_LOCAL

def main(data_dir: str):
    rag = RAGService.get_instance()
    rag.ingest_documents(data_dir)
    print("FAISS ingestion completed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents into FAISS index")
    parser.add_argument(
        "--data-dir",
        type=str,
        default=DATA_DIR_LOCAL,
        help=f"Path to document directory (default: {DATA_DIR_LOCAL})"
    )
    args = parser.parse_args()
    main(args.data_dir)
