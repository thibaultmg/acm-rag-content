#!/bin/bash
set -eou pipefail

if [ -z "${1-}" ]; then
    echo "Error: ACM_VERSION argument is missing."
    echo "Usage: $0 <ACM_VERSION> <REPO_DIR> [OUTPUT_DIR]"
    exit 1
fi

if [ -z "${2-}" ]; then
    echo "Error: REPO_DIR argument is missing."
    echo "Usage: $0 <ACM_VERSION> <REPO_DIR> [OUTPUT_DIR]"
    exit 1
fi

ACM_VERSION=$1
REPO_DIR=$2
OUTPUT_DIR=${3:-"docs/acm/${ACM_VERSION}"}

# Ensure parent directory of REPO_DIR exists
mkdir -p "$(dirname "${REPO_DIR}")"

# Safety guardrail to prevent catastrophic deletion
if [[ "${OUTPUT_DIR}" != docs/* && "${OUTPUT_DIR}" != tmp/* && "${OUTPUT_DIR}" != */docs/* && "${OUTPUT_DIR}" != */tmp/* ]]; then
    echo "Error: OUTPUT_DIR (${OUTPUT_DIR}) seems unsafe to delete. It must be inside a docs or tmp directory."
    exit 1
fi

# Ensure output directory is clean
rm -rf "${OUTPUT_DIR}"

echo "Cloning documentation for version ${ACM_VERSION}..."
# Clone specifically into the directory we expect (openshift-docs)
git clone --quiet --single-branch --branch "${ACM_VERSION}_prod" \
    https://github.com/stolostron/rhacm-docs.git "${REPO_DIR}"

echo "Done."
