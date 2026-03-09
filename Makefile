PRODUCT ?= acm
VERSION ?= 2.15
FETCHED_DOCS_DIR = tmp/rhacm-docs
PROCESSED_DOCS_DIR = docs/$(PRODUCT)/$(VERSION)
PYTHON ?= uv run python

IMAGE_NAME ?= localhost/my-rag-embedding-generator:latest
OUTPUT_DIR ?= vector_db/$(PRODUCT)/$(VERSION)
DOCS_FOLDER ?= docs/$(PRODUCT)/$(VERSION)
MODEL_DIR ?= embeddings_model/
MODEL_NAME ?= sentence-transformers/all-mpnet-base-v2
# Sanitize version for index name (replace . with _)
SANITIZED_VERSION = $(subst .,_,$(VERSION))
INDEX_NAME ?= $(PRODUCT)_docs-$(SANITIZED_VERSION)

VECTOR_STORE_TYPE ?= faiss
WORKERS ?= 0
UNREACHABLE_ACTION ?= warn
LOG_LEVEL ?= WARNING

.PHONY: fetch-docs render-docs clean check-deps update-docs test lint all build-image generate-embeddings-local generate-embeddings-container

all: generate-embeddings-container

# Verify that all required system dependencies are installed
check-deps:
	@which git > /dev/null || (echo "Error: git is not installed" && exit 1)
	@which uv > /dev/null || (echo "Error: uv is not installed" && exit 1)
	@which asciidoctor > /dev/null || (echo "Error: asciidoctor is not installed" && exit 1)
	@which pandoc > /dev/null || (echo "Error: pandoc is not installed" && exit 1)
	@echo "All dependencies check out."

# Download the ACM documentation from the rhacm-docs repository
fetch-docs: check-deps
	./scripts/fetch_acm_docs.sh $(VERSION) $(FETCHED_DOCS_DIR) $(PROCESSED_DOCS_DIR)

# Convert the fetched AsciiDoc files to Markdown using Pandoc
render-docs: check-deps
	@echo "Rendering with Pandoc..."
	@mkdir -p $(PROCESSED_DOCS_DIR)
	@find $(FETCHED_DOCS_DIR) -name "main.adoc" -type f | grep -v "$(FETCHED_DOCS_DIR)/apis/main.adoc" | while read file; do \
		echo "Processing $$file"; \
		REL_PATH=$${file#$(FETCHED_DOCS_DIR)/}; \
		OUT_DIR="$(PROCESSED_DOCS_DIR)/$$(dirname $$REL_PATH)"; \
		mkdir -p "$$OUT_DIR"; \
		TMP_XML=$$(mktemp); \
		asciidoctor -b docbook -a allow-uri-read -a images! -o "$$TMP_XML" "$$file"; \
		$(PYTHON) scripts/clean_acm_docs.py "$$TMP_XML"; \
		$(PYTHON) scripts/extract_ids.py "$$TMP_XML" "$$OUT_DIR/header_map.json"; \
		pandoc -f docbook -t gfm "$$TMP_XML" -o "$$OUT_DIR/main.md"; \
		rm "$$TMP_XML"; \
	done

# Fetch, render, and clean up temporary documentation files
update-docs: fetch-docs render-docs
	rm -rf $(FETCHED_DOCS_DIR)

# Build the Podman container image used for generating embeddings
build-image:
	podman build -t $(IMAGE_NAME) -f Dockerfile .

# Download the HuggingFace embedding model to the local cache
$(MODEL_DIR)/config.json:
	@echo "Downloading embedding model..."
	@mkdir -p $(MODEL_DIR)
	@$(PYTHON) embedding_generator/scripts/download_embeddings_model.py -l $(MODEL_DIR) -r $(MODEL_NAME)

# Generate vector embeddings locally using the Python virtual environment
generate-embeddings-local: $(MODEL_DIR)/config.json
	@echo "Generating embeddings locally..."
	@mkdir -p $(OUTPUT_DIR)
	# Restricting underlying library threads to 1 and disabling tokenizer parallelism 
	# is required to prevent segmentation faults (Error 139) on macOS when using 
	# multiprocessing with PyTorch.
	KMP_DUPLICATE_LIB_OK=TRUE TOKENIZERS_PARALLELISM=false OMP_NUM_THREADS=1 $(PYTHON) embedding_generator/custom_processor.py \
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
		--log-level $(LOG_LEVEL) \
		--config embedding_generator/config.yaml
	@if [ -f "$(OUTPUT_DIR)/default__vector_store.json" ]; then \
		echo "Renaming default__vector_store.json to faiss_index.bin..."; \
		mv $(OUTPUT_DIR)/default__vector_store.json $(OUTPUT_DIR)/faiss_index.bin; \
	fi

# Generate vector embeddings using the isolated Podman container
generate-embeddings-container: build-image $(MODEL_DIR)/config.json
	@echo "Generating embeddings using the container image..."
	@mkdir -p $(OUTPUT_DIR)
	podman run --rm \
		-v $(abspath $(DOCS_FOLDER)):/data/input:ro \
		-v $(abspath $(OUTPUT_DIR)):/data/output \
		-v $(abspath $(MODEL_DIR)):/data/model \
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

# Clean up all generated files, caches, and container images
clean:
	rm -rf $(FETCHED_DOCS_DIR)
	@echo "Cleaning up generated files and image..."
	rm -rf $(OUTPUT_DIR)
	rm -rf $(MODEL_DIR)
	podman rmi $(IMAGE_NAME) || true

# Run Python tests
test:
	PYTHONPATH=. uv run pytest

# Run Python code linters and formatters
lint:
	uv run ruff check .
	uv run ruff format --check .
