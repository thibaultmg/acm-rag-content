from lightspeed_rag_content.metadata_processor import MetadataProcessor
from lightspeed_rag_content.document_processor import DocumentProcessor
from lightspeed_rag_content import utils

class CustomMetadataProcessor(MetadataProcessor):

    def __init__(self, url):
        self.url = url

    def url_function(self, file_path: str) -> str:
        # Return a URL for the file, so it can be referenced when used
        # in an answer
        return self.url

if __name__ == "__main__":
    parser = utils.get_common_arg_parser()
    parser.add_argument('--url', type=str, required=True, help='Base URL for the documentation.')
    args = parser.parse_args()

    # Instantiate custom Metadata Processor
    metadata_processor = CustomMetadataProcessor(args.url)

    # Instantiate Document Processor
    document_processor = DocumentProcessor(
        chunk_size=args.chunk,
        chunk_overlap=args.overlap,
        model_name=args.model_name,
        embeddings_model_dir=args.model_dir,
        num_workers=args.workers,
        vector_store_type=args.vector_store_type,
        doc_type="markdown",
    )

    # Load and embed the documents, this method can be called multiple times
    # for different sets of documents
    document_processor.process(args.folder, metadata=metadata_processor)

    # Save the new vector database to the output directory
    document_processor.save(args.index, args.output)
