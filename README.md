# ACM RAG Content

This repository contains reference content used by OLS (OpenShift Lightspeed) and tooling to produce vector embeddings from that content. It allows generating a vector database that can be used for Retrieval-Augmented Generation (RAG).

## Overview

The project provides:
1.  **Documentation:** A collection of documentation files (e.g., in `docs/acm/2.15`).
2.  **Embedding Generation:** Tools to chunk this documentation and generate vector embeddings using a HuggingFace model (`sentence-transformers/all-mpnet-base-v2`).
3.  **Vector Database:** Scripts to create a FAISS-based vector index from the embeddings.

## Prerequisites

-   Python 3.12
-   `uv`
-   `make`
-   `podman` (for containerized generation)

## Setup

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    uv sync
    ```

## Usage

### Generating Embeddings (Local)

To generate the vector database locally on your machine, run the generation command from the root of the repository:

```bash
make generate-embeddings-local
```

This will:
-   Download the embedding model (if not present) to `embeddings_model/`.
-   Process the documents in `docs/acm/2.15`.
-   Generate the vector database in `vector_db/acm/2.15`.
-   Automatically rename the output file to `faiss_index.bin` for compatibility.

### Generating Embeddings (Container)

To generate the vector database using a container (requires Podman), run the following from the root of the repository:

```bash
make generate-embeddings-container
```

### Querying the Vector Database

A helper script is provided to query the generated local vector database.

```bash
uv run scripts/query_local.py --query "Your question here"
```

**Example:**

```bash
uv run scripts/query_local.py --query "What is ACM Observability?"
```

This will load the FAISS index and metadata from `vector_db/acm/2.15` and return the most relevant document chunks.

### Combining Multiple Products/Versions in a Single DB

To create a single vector database from documentation spanning multiple products or versions, you can use symbolic links to create a unified view of your documentation. This approach leverages the recursive processing of the `embedding_generator`.

1.  **Create a combined documentation directory:**
    ```bash
    mkdir -p docs/combined_docs
    ```

2.  **Create symbolic links to your product/version directories:**
    ```bash
    ln -s $(pwd)/docs/acm/2.15 docs/combined_docs/acm_2.15
    ln -s $(pwd)/docs/thanos/latest docs/combined_docs/thanos_latest # Example for Thanos
    # Add more symlinks as needed
    ```

3.  **Generate the embeddings, pointing to the combined directory:**
    Override the `DOCS_FOLDER` variable:
    ```bash
    make generate-embeddings-local DOCS_FOLDER=docs/combined_docs PRODUCT=combined VERSION=v1
    ```
    *Note: The `PRODUCT` and `VERSION` parameters here (`combined` and `v1`) will determine the output directory (`vector_db/combined/v1`) and the `INDEX_NAME` for the combined database.*

    The `embedding_generator/custom_processor.py` has been updated to dynamically assign appropriate URLs to the chunks based on whether `acm` or `thanos` is in their file path, ensuring correct source attribution for mixed content.

4.  **Query the combined database:**
    ```bash
    uv run scripts/query_local.py --product combined --version v1 --query "How do I manage multi-cluster applications with ACM?"
    ```

## Directory Structure

-   `docs/`: Source documentation files.
-   `embeddings_model/`: Local cache for the HuggingFace embedding model (should be ignored by git).
-   `vector_db/`: Output directory for the generated vector database (should be ignored by git).
-   `embedding_generator/`: Contains logic for the generation process.
-   `scripts/`: Helper scripts (e.g., for querying).

## Troubleshooting

-   **Segmentation Faults (macOS):** The `Makefile` includes specific environment variables (`TOKENIZERS_PARALLELISM=false`, `OMP_NUM_THREADS=1`) to prevent common concurrency issues with `faiss` and `torch` on macOS.
-   **UnicodeDecodeError:** If you see this when querying, ensure `vector_db/acm/2.15/default__vector_store.json` has been renamed to `faiss_index.bin`. The `make generate-embeddings-local` command does this automatically.
