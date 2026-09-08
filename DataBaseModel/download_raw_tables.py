from pathlib import Path
from DataBaseModel.constants import TABLE_FILENAMES, RAW_TABLES_DIR, REPO_ID
from huggingface_hub import hf_hub_download

def download_files(filenames: list[str], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename in filenames:
        cached_path: str = hf_hub_download(
            repo_id=REPO_ID,
            filename=filename,
            repo_type="dataset",
        )
        destination: Path = output_dir / filename
        destination.write_bytes(Path(cached_path).read_bytes())

if __name__ == "__main__":
    download_files(TABLE_FILENAMES, RAW_TABLES_DIR)
