import argparse
import os
import sys
from pathlib import Path

import faiss
from llama_index.core import Settings, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.llms import MockLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the local RAG vector database.")
    parser.add_argument("-q", "--query", type=str, required=True, help="The query text.")
    parser.add_argument(
        "-p",
        "--product",
        type=str,
        default="acm",
        help="Product name (e.g., acm, thanos). Default: acm",
    )
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="2.15",
        help="Documentation version (e.g., 2.15, latest). Default: 2.15",
    )
    args = parser.parse_args()

    # Define paths (relative to scripts/ directory)
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    base_output_dir = (PROJECT_ROOT / "vector_db").resolve()
    OUTPUT_DIR = (base_output_dir / args.product / args.version).resolve()

    # Check for path traversal vulnerabilities
    if not OUTPUT_DIR.is_relative_to(base_output_dir):
        print(
            f"Error: Invalid product or version path (path traversal detected): {OUTPUT_DIR}",
            file=sys.stderr,
        )
        return 1

    MODEL_DIR = PROJECT_ROOT / "embeddings_model"

    sanitized_version = args.version.replace(".", "_")
    INDEX_NAME = f"{args.product}_docs-{sanitized_version}"
    FAISS_INDEX_PATH = OUTPUT_DIR / "faiss_index.bin"

    if not OUTPUT_DIR.exists():
        print(f"Error: Vector DB directory not found at {OUTPUT_DIR}", file=sys.stderr)
        return 1

    if not MODEL_DIR.exists():
        print(f"Error: Model directory not found at {MODEL_DIR}", file=sys.stderr)
        return 1

    # Set the HuggingFace model environment variables
    os.environ["HF_HOME"] = str(MODEL_DIR)
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    # Configure the embedding model for LlamaIndex
    Settings.embed_model = HuggingFaceEmbedding(model_name=str(MODEL_DIR))
    Settings.llm = MockLLM()

    print(f"Loading FAISS index from {FAISS_INDEX_PATH}...")
    try:
        faiss_index = faiss.read_index(str(FAISS_INDEX_PATH))
        print("FAISS index loaded successfully.")
    except (RuntimeError, ValueError, OSError) as e:
        print(f"Failed to load FAISS index: {e}", file=sys.stderr)
        return 1

    print("Initializing FaissVectorStore...")
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    print(f"Loading storage context from {OUTPUT_DIR}...")
    # Rebuild storage context, but ignore the missing vector_store.json
    # We initialize it with our custom vector_store
    storage_context = StorageContext.from_defaults(persist_dir=str(OUTPUT_DIR), vector_store=vector_store)

    print("Loading index from storage...")
    try:
        index = load_index_from_storage(storage_context, index_id=INDEX_NAME)
        print("Index loaded successfully.")
    except ValueError as e:
        print(f"load_index_from_storage failed: {e}")
        print("Attempting to reconstruct VectorStoreIndex directly...")
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store, storage_context=storage_context)
        print("Reconstructed VectorStoreIndex.")

    # Create a query engine
    query_engine = index.as_query_engine()

    query_text = args.query
    print(f"\nQuerying: '{query_text}'")
    response = query_engine.query(query_text)
    print(f"Response: {response}")

    # You can also get more detailed information, like the source nodes
    print("\nSource Nodes:")
    for node in response.source_nodes:
        print(f"  Score: {node.score}")
        print(f"  Text: {node.text[:200]}...")  # Print first 200 characters of the text
        print(f"  Metadata: {node.metadata}")
        print("-" * 20)

    return 0


if __name__ == "__main__":
    sys.exit(main())
