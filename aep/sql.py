from pathlib import Path


def load_sql(path: str | Path) -> str:
    return Path(path).read_text(encoding='utf-8')


def load_sql_relative(base_file: str | Path, relative_sql_path: str | Path) -> str:
    return (Path(base_file).resolve().parent / relative_sql_path).read_text(encoding='utf-8')
