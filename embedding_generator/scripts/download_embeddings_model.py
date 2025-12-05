import argparse
from pathlib import Path
from sentence_transformers import SentenceTransformer

def download_model(model_name: str, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading model {model_name} using SentenceTransformer to {output_dir}...")
    model = SentenceTransformer(model_name)
    model.save(str(output_dir))
    print(f"Successfully downloaded {model_name} to {output_dir}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download embedding model from HuggingFace.')
    parser.add_argument('-l', '--local_dir', type=Path, required=True, help='Local directory to save the model.')
    parser.add_argument('-r', '--repo_id', type=str, required=True, help='HuggingFace repository ID (e.g., sentence-transformers/all-mpnet-base-v2).')
    args = parser.parse_args()

    download_model(args.repo_id, args.local_dir)
