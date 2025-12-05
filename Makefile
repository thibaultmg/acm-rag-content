ACM_VERSION ?= 2.15
DOCS_DIR = acm-docs
OUTPUT_DIR = experimental-output

.PHONY: fetch-docs render-pandoc clean check-deps

check-deps:
	@which git > /dev/null || (echo "Error: git is not installed" && exit 1)
	@which python3 > /dev/null || (echo "Error: python3 is not installed" && exit 1)
	@which asciidoctor > /dev/null || (echo "Error: asciidoctor is not installed" && exit 1)
	@which pandoc > /dev/null || (echo "Error: pandoc is not installed" && exit 1)
	@echo "All dependencies check out."

fetch-docs: check-deps
	./scripts/get_ocp_plaintext_docs.sh $(ACM_VERSION) $(DOCS_DIR)

render-pandoc: check-deps
	@echo "Rendering with Pandoc..."
	@mkdir -p $(OUTPUT_DIR)/pandoc
	@find $(DOCS_DIR) -name "main.adoc" -type f | grep -v "$(DOCS_DIR)/apis/main.adoc" | while read file; do \
		echo "Processing $$file"; \
		REL_PATH=$${file#$(DOCS_DIR)/}; \
		OUT_DIR="$(OUTPUT_DIR)/pandoc/$$(dirname $$REL_PATH)"; \
		mkdir -p "$$OUT_DIR"; \
		TMP_XML=$$(mktemp); \
		asciidoctor -b docbook -a allow-uri-read -a images! -o "$$TMP_XML" "$$file"; \
		python3 scripts/clean_docbook.py "$$TMP_XML"; \
		pandoc -f docbook -t gfm "$$TMP_XML" -o "$$OUT_DIR/main.md"; \
		rm "$$TMP_XML"; \
	done

clean:
	rm -rf $(OUTPUT_DIR)