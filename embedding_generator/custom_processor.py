import functools
import json
import logging
import os
import re
import sys

import yaml
from lightspeed_rag_content import utils
from lightspeed_rag_content.document_processor import DocumentProcessor
from lightspeed_rag_content.metadata_processor import MetadataProcessor
from llama_index.core import Settings
from llama_index.core.node_parser import MarkdownNodeParser

NON_WORD_SPACE_DASH_PATTERN = re.compile(r"[^\w\s-]")
DASH_SPACE_PATTERN = re.compile(r"[-\s]+")


def slugify(text: str) -> str:
    """
    Create a URL slug from the header text.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower().strip()
    text = NON_WORD_SPACE_DASH_PATTERN.sub("", text)
    text = DASH_SPACE_PATTERN.sub("-", text)
    return text


@functools.lru_cache(maxsize=1024)
def _load_header_map(dir_path: str) -> dict:
    map_file = os.path.join(dir_path, "header_map.json")
    try:
        with open(map_file) as f:
            data = json.load(f)
            # Validate schema and normalize data
            normalized_map = {}
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, list) and len(v) > 0:
                        normalized_map[str(k)] = str(v[0])
                    elif isinstance(v, str):
                        normalized_map[str(k)] = v
            return normalized_map
    except FileNotFoundError:
        pass
    except json.JSONDecodeError as e:
        logging.error("Failed to decode header map %s: %s", map_file, e)
        raise ValueError(f"Invalid JSON in {map_file}") from e
    return {}


def get_anchor_id(file_path: str, header_text: str) -> str:
    """
    Try to find the custom ID from header_map.json in the file's directory.
    Fallback to slugify if not found.
    """
    if not isinstance(file_path, str) or not file_path:
        return slugify(header_text)

    dir_path = os.path.dirname(os.path.abspath(file_path))
    header_map = _load_header_map(dir_path)

    custom_id = header_map.get(header_text)
    if custom_id:
        return custom_id.lstrip("_")

    return slugify(header_text)


class AnchorLinkNodeParser(MarkdownNodeParser):
    _chunk_size: int = 1024
    _chunk_overlap: int = 0

    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value):
        self._chunk_size = value

    @property
    def chunk_overlap(self):
        return self._chunk_overlap

    @chunk_overlap.setter
    def chunk_overlap(self, value):
        self._chunk_overlap = value

    def get_nodes_from_documents(self, documents, **kwargs):
        nodes = super().get_nodes_from_documents(documents, **kwargs)

        # Post-process nodes to add anchor links using public node attributes
        count = 0
        for node in nodes:
            base_url = node.metadata.get("docs_url")
            file_path = node.metadata.get("file_path")

            if isinstance(base_url, str) and base_url and isinstance(file_path, str) and file_path:
                leaf_header = ""

                # Try to extract the header from the node's text
                if hasattr(node, "text") and node.text:
                    first_line = node.text.lstrip().split("\n", 1)[0]
                    match = re.match(r"^(#+)\s+(.*)", first_line)
                    if match:
                        leaf_header = match.group(2).strip()

                # Fallback to header_path if no header in text
                if not leaf_header:
                    header_path = node.metadata.get("header_path")
                    if isinstance(header_path, str) and header_path:
                        headers = [h for h in header_path.split("/") if h]
                        if headers:
                            leaf_header = headers[-1]

                if leaf_header:
                    # Get anchor (custom ID or slug)
                    anchor = get_anchor_id(file_path, leaf_header)

                    # Construct deep link
                    deep_link = f"{base_url}#{anchor}"

                    # Construct full title path
                    header_path_str = node.metadata.get("header_path", "")
                    headers = [h for h in header_path_str.split("/") if h] if isinstance(header_path_str, str) else []

                    if headers and leaf_header != headers[-1]:
                        full_title = " - ".join(headers + [leaf_header])
                    elif headers:
                        full_title = " - ".join(headers)
                    else:
                        full_title = leaf_header

                    # Defensive copy before mutation
                    node.metadata = node.metadata.copy()

                    # Update metadata
                    node.metadata["docs_url"] = deep_link
                    node.metadata["url"] = deep_link
                    node.metadata["title"] = full_title
                    count += 1

        logging.debug("Updated URLs for %d nodes with anchor links.", count)
        return nodes


class CustomMetadataProcessor(MetadataProcessor):
    def __init__(self, root_dir, default_url, rename_map=None):
        self.root_dir = os.path.abspath(root_dir)
        self.default_url = default_url
        self.rename_map = rename_map or {}
        if not self.default_url.endswith("/"):
            self.default_url += "/"

    def populate(self, file_path: str):
        metadata = super().populate(file_path)
        metadata = metadata.copy()
        metadata["file_path"] = file_path
        return metadata

    def url_function(self, file_path: str) -> str:
        import pathlib

        abs_path = os.path.abspath(file_path)

        # Calculate relative path from the processed root
        try:
            rel_path = pathlib.Path(abs_path).relative_to(self.root_dir).as_posix()
            if rel_path == ".":
                rel_path = ""
        except ValueError:
            return self.default_url

        # Apply rename map to path segments
        if self.rename_map:
            parts = rel_path.split("/")
            parts = [self.rename_map.get(p, p) for p in parts]
            rel_path = "/".join(parts)

        # Remove the file extension
        url_suffix = os.path.splitext(rel_path)[0]

        # Rename 'main' to 'index' for standard Red Hat docs structure
        if url_suffix.endswith("/main") or url_suffix == "main":
            url_suffix = url_suffix[:-4] + "index"

        return self.default_url + url_suffix


def run() -> int:
    parser = utils.get_common_arg_parser()
    parser.add_argument("--product", type=str, required=True, help="Product name (key in config.yaml).")
    parser.add_argument("--version", type=str, required=True, help="Product version.")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to configuration file.")

    log_level_str = os.environ.get("LOG_LEVEL", "WARNING").upper()
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=log_level_str,
        help="Set the logging level.",
    )
    parser.add_argument(
        "--unreachable-action",
        type=str,
        choices=["warn", "fail", "drop"],
        default="warn",
        help="Action to take when a URL is unreachable (warn, fail, drop).",
    )
    args = parser.parse_args()

    # Configure logging based on parsed arguments
    log_level = getattr(logging, args.log_level.upper(), logging.WARNING)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr,
    )

    # Load config
    try:
        with open(args.config) as f:
            config = yaml.safe_load(f) or {}
    except (yaml.YAMLError, OSError):
        logging.exception("Failed to load config file: %s", args.config)
        return 1

    # Resolve URL from config
    products_config = config.get("products") or {}
    product_config = products_config.get(args.product)
    if not product_config:
        logging.warning("Product '%s' not found in config. Using default.", args.product)
        product_config = products_config.get("default") or {}

    url_template = product_config.get("url_template", "")
    rename_map = product_config.get("rename_map", {})

    if not url_template:
        logging.error("No url_template found for product '%s' or default.", args.product)
        return 1

    resolved_url = url_template.format(version=args.version, product=args.product)
    logging.info("Resolved base URL: %s", resolved_url)

    # Instantiate custom Metadata Processor with the root folder
    metadata_processor = CustomMetadataProcessor(args.folder, resolved_url, rename_map)

    # Inject our custom node parser
    custom_parser = AnchorLinkNodeParser()
    Settings.node_parser = custom_parser
    Settings.text_splitter = custom_parser

    # Instantiate Document Processor
    document_processor = DocumentProcessor(
        chunk_size=args.chunk,
        chunk_overlap=args.overlap,
        model_name=args.model_name,
        embeddings_model_dir=args.model_dir,
        num_workers=args.workers,
        vector_store_type=args.vector_store_type,
        doc_type="text",  # Bypasses MarkdownNodeParser default assignment to respect our wrapper
    )

    # Load and embed the documents
    document_processor.process(
        args.folder,
        metadata=metadata_processor,
        unreachable_action=args.unreachable_action,
    )

    # Save the new vector database to the output directory
    document_processor.save(args.index, args.output)

    return 0


if __name__ == "__main__":
    sys.exit(run())
