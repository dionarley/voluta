"""Sincroniza os assets da raiz com o diretório de documentação."""

from __future__ import annotations

import filecmp
import shutil
from pathlib import Path


def _copy_if_changed(source: Path, destination: Path) -> None:
    if destination.exists() and filecmp.cmp(source, destination, shallow=False):
        return
    shutil.copy2(source, destination)


def on_pre_build(config) -> None:
    """Copia ``assets/`` para ``docs/assets`` antes do build do MkDocs."""
    root = Path(config["config_file_path"]).resolve().parent
    source = root / "assets"
    destination = Path(config["docs_dir"]).resolve() / "assets"

    if not source.is_dir():
        return

    destination.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        if item.is_file() and item.suffix.lower() != ".md":
            _copy_if_changed(item, destination / item.name)
