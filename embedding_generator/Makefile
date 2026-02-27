IMAGE_NAME ?= localhost/my-rag-embedding-generator:latest
PRODUCT ?= acm
VERSION ?= 2.15
OUTPUT_DIR ?= ../vector_db/$(PRODUCT)/$(VERSION)
DOCS_FOLDER ?= ../docs/$(PRODUCT)/$(VERSION)
MODEL_DIR ?= ../embeddings_model/
MODEL_NAME ?= sentence-transformers/all-mpnet-base-v2
# Sanitize version for index name (replace . with _)
SANITIZED_VERSION = $(subst .,_,$(VERSION))
INDEX_NAME ?= $(PRODUCT)_docs-$(SANITIZED_VERSION)

VECTOR_STORE_TYPE ?= faiss
WORKERS ?= 0
UNREACHABLE_ACTION ?= warn
LOG_LEVEL ?= WARNING

.PHONY: all build-image generate-local generate-container clean

all: generate-container

build-image:
	podman build -t $(IMAGE_NAME) .

$(MODEL_DIR)/config.json:
	@echo "Downloading embedding model..."
	@mkdir -p $(MODEL_DIR)
	@python scripts/download_embeddings_model.py -l $(MODEL_DIR) -r $(MODEL_NAME)

generate-local: $(MODEL_DIR)/config.json # Generate embeddings locally using the Python script
	@echo "Generating embeddings locally..."
	@mkdir -p $(OUTPUT_DIR)
	KMP_DUPLICATE_LIB_OK=TRUE TOKENIZERS_PARALLELISM=false OMP_NUM_THREADS=1 python custom_processor.py \
		-o $(OUTPUT_DIR) \
		-f $(DOCS_FOLDER) \
		-md $(MODEL_DIR) \
		-mn $(MODEL_NAME) \
		-i $(INDEX_NAME) \
		--product $(PRODUCT) \
		--version $(VERSION) \
		--workers $(WORKERS) \
		--vector-store-type $(VECTOR_STORE_TYPE) \
		--unreachable-action $(UNREACHABLE_ACTION) \
		--log-level $(LOG_LEVEL)
	@if [ -f "$(OUTPUT_DIR)/default__vector_store.json" ]; then \
		echo "Renaming default__vector_store.json to faiss_index.bin..."; \
		mv $(OUTPUT_DIR)/default__vector_store.json $(OUTPUT_DIR)/faiss_index.bin; \
	fi

generate-container: build-image $(MODEL_DIR)/config.json # Generate embeddings using the container image
	@echo "Generating embeddings using the container image..."
	@mkdir -p $(OUTPUT_DIR)
	podman run --rm \
		-v $(abspath config.yaml):/opt/app-root/src/config.yaml:ro \
		-v $(abspath $(DOCS_FOLDER)):/data/input:ro \
		-v $(abspath $(OUTPUT_DIR)):/data/output \
		-v $(abspath $(MODEL_DIR)):/data/model:ro \
		$(IMAGE_NAME) \
		-o /data/output \
		-f /data/input \
		-md /data/model \
		-mn $(MODEL_NAME) \
		-i $(INDEX_NAME) \
		--product $(PRODUCT) \
		--version $(VERSION) \
		--workers $(WORKERS) \
		--vector-store-type $(VECTOR_STORE_TYPE) \
		--unreachable-action $(UNREACHABLE_ACTION) \
		--log-level $(LOG_LEVEL)

clean:
	@echo "Cleaning up generated files and image..."
	rm -rf $(OUTPUT_DIR)
	rm -rf $(MODEL_DIR)
	podman rmi $(IMAGE_NAME) || true

