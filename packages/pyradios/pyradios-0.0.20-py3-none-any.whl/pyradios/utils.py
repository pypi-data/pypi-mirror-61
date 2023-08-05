from pathlib import Path

from pyradios.config import app_dirs


def create_app_dirs(filename, path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p / filename


def setup_log_file(filename, **kwargs):
    return create_app_dirs(filename, app_dirs.user_log_dir)


def setup_cache_file(filename, **kwargs):
    return create_app_dirs(filename, app_dirs.user_cache_dir)
