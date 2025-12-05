#!/bin/bash
set -eou pipefail

if [ -z "${1-}" ]; then
    echo "Error: ACM_VERSION argument is missing."
    echo "Usage: $0 <ACM_VERSION> <REPO_DIR>"
    exit 1
fi

if [ -z "${2-}" ]; then
    echo "Error: REPO_DIR argument is missing."
    echo "Usage: $0 <ACM_VERSION> <REPO_DIR>"
    exit 1
fi

ACM_VERSION=$1
REPO_DIR=$2

# Clean up on exit (handles both success and error)
# trap "rm -rf '${REPO_DIR}'" EXIT

# Ensure output directory is clean
rm -rf "docs/acm/${ACM_VERSION}"

echo "Cloning documentation for version ${ACM_VERSION}..."
# Clone specifically into the directory we expect (openshift-docs)
git clone --quiet --single-branch --branch "${ACM_VERSION}_prod" \
    https://github.com/stolostron/rhacm-docs.git "${REPO_DIR}"

# echo "Converting AsciiDoc to plaintext..."
# python3 scripts/asciidoctor-text/convert-it-all.py \
#     -i "${REPO_DIR}" \
#     -t "${REPO_DIR}/_topic_maps/_topic_map.yml" \
#     -d openshift-enterprise \
#     -o "ocp-product-docs-plaintext/${ACM_VERSION}" \
#     -a "scripts/asciidoctor-text/${ACM_VERSION}/attributes.yaml"

# if [ -f config/exclude.conf ]; then
#     echo "Removing excluded files..."
#     while IFS= read -r f; do
#         # Skip empty lines or comments if necessary
#         [[ -z "$f" || "$f" =~ ^# ]] && continue
#         rm -f "ocp-product-docs-plaintext/${ACM_VERSION}/$f"
#     done < config/exclude.conf
# else
#     echo "Warning: config/exclude.conf not found, skipping cleanup."
# fi

echo "Done."
