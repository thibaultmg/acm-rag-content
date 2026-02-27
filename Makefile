ACM_VERSION ?= 2.15
FETCHED_DOCS_DIR = tmp/rhacm-docs
PROCESSED_DOCS_DIR = docs/acm/$(ACM_VERSION)
PYTHON ?= python3

.PHONY: fetch-docs render-pandoc clean check-deps update-docs

check-deps:
	@which git > /dev/null || (echo "Error: git is not installed" && exit 1)
	@which $(PYTHON) > /dev/null || (echo "Error: $(PYTHON) is not installed" && exit 1)
	@which asciidoctor > /dev/null || (echo "Error: asciidoctor is not installed" && exit 1)
	@which pandoc > /dev/null || (echo "Error: pandoc is not installed" && exit 1)
	@echo "All dependencies check out."

fetch-docs: check-deps
	./scripts/fetch_acm_docs.sh $(ACM_VERSION) $(FETCHED_DOCS_DIR) $(PROCESSED_DOCS_DIR)

render-pandoc: check-deps
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

clean:
	rm -rf $(FETCHED_DOCS_DIR)

update-docs: fetch-docs render-pandoc clean