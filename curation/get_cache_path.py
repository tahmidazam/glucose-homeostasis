from pathlib import Path


def get_cache_path(filename: str) -> Path:
    path = Path(f"./../df_cache/{filename}")

    return path
