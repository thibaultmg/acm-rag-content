import os
import argparse
import faiss
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex
from llama_index.core.llms import MockLLM
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Query the local RAG vector database.")
    parser.add_argument("-q", "--query", type=str, required=True, help="The query text.")
    args = parser.parse_args()

    # Define paths (relative to scripts/ directory)
    # Assuming the script is run from the root of the repo or from scripts/, 
    # but using relative paths might be brittle if CWD changes.
    # Let's resolve relative to the script's location.
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent
    
    OUTPUT_DIR = PROJECT_ROOT / "vector_db/acm/2.15"
    MODEL_DIR = PROJECT_ROOT / "embeddings_model"
    INDEX_NAME = "acm_docs-2_15" 
    FAISS_INDEX_PATH = OUTPUT_DIR / "faiss_index.bin"

    if not OUTPUT_DIR.exists():
        print(f"Error: Vector DB directory not found at {OUTPUT_DIR}")
        exit(1)
        
    if not MODEL_DIR.exists():
         print(f"Error: Model directory not found at {MODEL_DIR}")
         exit(1)

    # Set the HuggingFace model environment variables
    os.environ["HF_HOME"] = str(MODEL_DIR)
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    # Configure the embedding model for LlamaIndex
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=str(MODEL_DIR)
    )
    Settings.llm = MockLLM()

    print(f"Loading FAISS index from {FAISS_INDEX_PATH}...")
    try:
        faiss_index = faiss.read_index(str(FAISS_INDEX_PATH))
        print("FAISS index loaded successfully.")
    except Exception as e:
        print(f"Failed to load FAISS index: {e}")
        exit(1)

    print("Initializing FaissVectorStore...")
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    print(f"Loading storage context from {OUTPUT_DIR}...")
    # Rebuild storage context, but ignore the missing vector_store.json
    # We initialize it with our custom vector_store
    storage_context = StorageContext.from_defaults(
        persist_dir=str(OUTPUT_DIR),
        vector_store=vector_store
    )

    print("Loading index from storage...")
    try:
        index = load_index_from_storage(storage_context, index_id=INDEX_NAME)
        print("Index loaded successfully.")
    except Exception as e:
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
        print(f"  Text: {node.text[:200]}...") # Print first 200 characters of the text
        print(f"  Metadata: {node.metadata}")
        print("-" * 20)

if __name__ == "__main__":
    main()
