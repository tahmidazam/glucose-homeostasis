from pathlib import Path


def verify_cache_directory():
    cache_directory = Path("df-cache/")

    if not cache_directory.is_dir():
        cache_directory.mkdir()
