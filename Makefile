ACM_VERSION ?= 2.15
DOCS_DIR = acm-docs
OUTPUT_DIR = experimental-output

.PHONY: fetch-docs render-pandoc render-ruby clean

fetch-docs:
	./scripts/get_ocp_plaintext_docs.sh $(ACM_VERSION) $(DOCS_DIR)

render-pandoc:
	@echo "Rendering with Pandoc..."
	@mkdir -p $(OUTPUT_DIR)/pandoc
	@find $(DOCS_DIR) -name "main.adoc" -type f | while read file; do \
		echo "Processing $$file"; \
		REL_PATH=$${file#$(DOCS_DIR)/}; \
		OUT_DIR="$(OUTPUT_DIR)/pandoc/$$(dirname $$REL_PATH)"; \
		mkdir -p "$$OUT_DIR"; \
		TMP_XML=$$(mktemp); \
		asciidoctor -b docbook -a allow-uri-read -a images! -o "$$TMP_XML" "$$file"; \
		xmlstarlet ed -L -N p="http://docbook.org/ns/docbook" -d "//p:imageobject" "$$TMP_XML"; \
		pandoc -f docbook -t markdown_strict "$$TMP_XML" -o "$$OUT_DIR/main.md"; \
		rm "$$TMP_XML"; \
	done

render-ruby:
	@echo "Rendering with Ruby script..."
	@mkdir -p $(OUTPUT_DIR)/ruby
	@find $(DOCS_DIR) -name "main.adoc" -type f | while read file; do \
		echo "Processing $$file"; \
		REL_PATH=$${file#$(DOCS_DIR)/}; \
		OUT_DIR="$(OUTPUT_DIR)/ruby/$$(dirname $$REL_PATH)"; \
		mkdir -p "$$OUT_DIR"; \
		asciidoctor -r ./scripts/asciidoctor-text/text-converter.rb -b text -o "$$OUT_DIR/main.txt" "$$file"; \
	done

clean:
	rm -rf $(OUTPUT_DIR)
