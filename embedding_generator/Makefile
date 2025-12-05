IMAGE_NAME ?= localhost/my-rag-embedding-generator:latest
OUTPUT_DIR ?= ../vector_db/acm/2.15
DOCS_FOLDER ?= ../docs/acm/2.15
MODEL_DIR ?= ../embeddings_model/
MODEL_NAME ?= sentence-transformers/all-mpnet-base-v2
INDEX_NAME ?= acm_docs-2_15
URL ?= https://www.redhat.com
VECTOR_STORE_TYPE ?= faiss
WORKERS ?= 0

.PHONY: all build-image generate-local generate-container clean

all: generate-container

build-image:
	podman build -t $(IMAGE_NAME) .

generate-local: # Generate embeddings locally using the Python script
	@echo "Generating embeddings locally..."
	@mkdir -p $(OUTPUT_DIR)
	@mkdir -p $(MODEL_DIR)
	@if [ ! -f "$(MODEL_DIR)/config.json" ]; then \
		echo "Downloading embedding model..."; \
		python scripts/download_embeddings_model.py -l $(MODEL_DIR) -r $(MODEL_NAME); \
	else \
		echo "Embedding model already exists in $(MODEL_DIR), skipping download."; \
	fi
	KMP_DUPLICATE_LIB_OK=TRUE TOKENIZERS_PARALLELISM=false OMP_NUM_THREADS=1 python custom_processor.py \
		-o $(OUTPUT_DIR) \
		-f $(DOCS_FOLDER) \
		-md $(MODEL_DIR) \
		-mn $(MODEL_NAME) \
		-i $(INDEX_NAME) \
		--url $(URL) \
		--workers $(WORKERS) \
		--vector-store-type $(VECTOR_STORE_TYPE)
	@if [ -f "$(OUTPUT_DIR)/default__vector_store.json" ]; then \
		echo "Renaming default__vector_store.json to faiss_index.bin..."; \
		mv $(OUTPUT_DIR)/default__vector_store.json $(OUTPUT_DIR)/faiss_index.bin; \
	fi
generate-container: build-image # Generate embeddings using the container image
	@echo "Generating embeddings using the container image..."
	@mkdir -p $(OUTPUT_DIR)
	@mkdir -p $(MODEL_DIR)
	@if [ ! -f "$(MODEL_DIR)/config.json" ]; then \
		echo "Downloading embedding model..."; \
		python scripts/download_embeddings_model.py -l $(MODEL_DIR) -r $(MODEL_NAME); \
	else \
		echo "Embedding model already exists in $(MODEL_DIR), skipping download."; \
	fi
	podman run --rm \
		-v $(abspath $(DOCS_FOLDER)):/opt/app-root/src/custom_docs/0.1 \
		-v $(abspath $(OUTPUT_DIR)):/opt/app-root/src/vector_db/custom_docs/0.1 \
		-v $(abspath $(MODEL_DIR)):/opt/app-root/src/embeddings_model/ \
		$(IMAGE_NAME) \
		-f /opt/app-root/src/custom_docs/0.1 \
		-o /opt/app-root/src/vector_db/custom_docs/0.1 \
		-md /opt/app-root/src/embeddings_model/ \
		-mn $(MODEL_NAME) \
		-i $(INDEX_NAME) \
		--url $(URL) \
		--workers $(WORKERS) \
		--vector-store-type $(VECTOR_STORE_TYPE)

clean:
	@echo "Cleaning up generated files and image..."
	rm -rf $(OUTPUT_DIR)
	rm -rf $(MODEL_DIR)
	podman rmi $(IMAGE_NAME) || true
