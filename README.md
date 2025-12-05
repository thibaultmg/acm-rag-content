# ACM RAG Content

This repository contains reference content used by OLS (OpenShift Lightspeed) and tooling to produce vector embeddings from that content. It allows generating a vector database that can be used for Retrieval-Augmented Generation (RAG).

## Overview

The project provides:
1.  **Documentation:** A collection of documentation files (e.g., in `docs/acm/2.15`).
2.  **Embedding Generation:** Tools to chunk this documentation and generate vector embeddings using a HuggingFace model (`sentence-transformers/all-mpnet-base-v2`).
3.  **Vector Database:** Scripts to create a FAISS-based vector index from the embeddings.

## Prerequisites

-   Python 3.12+
-   `make`
-   `podman` (for containerized generation)

## Setup

1.  Clone the repository.
2.  Install dependencies (if running locally):
    ```bash
    pip install -r requirements.txt
    ```
    (Note: The project is set up to use `uv` for dependency management if available, but requirements are provided).

## Usage

### Generating Embeddings (Local)

To generate the vector database locally on your machine:

1.  Navigate to the `embedding_generator` directory:
    ```bash
    cd embedding_generator
    ```

2.  Run the generation command:
    ```bash
    make generate-local
    ```

    This will:
    -   Download the embedding model (if not present) to `embeddings_model/`.
    -   Process the documents in `docs/acm/2.15`.
    -   Generate the vector database in `vector_db/acm/2.15`.
    -   Automatically rename the output file to `faiss_index.bin` for compatibility.

### Generating Embeddings (Container)

To generate the vector database using a container (requires Podman):

```bash
cd embedding_generator
make generate-container
```

### Querying the Vector Database

A helper script is provided to query the generated local vector database.

```bash
python scripts/query_local.py --query "Your question here"
```

**Example:**

```bash
python scripts/query_local.py --query "What is OpenShift Container Platform?"
```

This will load the FAISS index and metadata from `vector_db/acm/2.15` and return the most relevant document chunks.

## Directory Structure

-   `docs/`: Source documentation files.
-   `embeddings_model/`: Local cache for the HuggingFace embedding model (should be ignored by git).
-   `vector_db/`: Output directory for the generated vector database (should be ignored by git).
-   `embedding_generator/`: Contains scripts and Makefile for the generation process.
-   `scripts/`: Helper scripts (e.g., for querying).

## Troubleshooting

-   **Segmentation Faults (macOS):** The `Makefile` includes specific environment variables (`TOKENIZERS_PARALLELISM=false`, `OMP_NUM_THREADS=1`) to prevent common concurrency issues with `faiss` and `torch` on macOS.
-   **UnicodeDecodeError:** If you see this when querying, ensure `vector_db/acm/2.15/default__vector_store.json` has been renamed to `faiss_index.bin`. The `make generate-local` command does this automatically.
