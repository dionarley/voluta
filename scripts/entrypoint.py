"""Ponto de entrada usado pelo PyInstaller para gerar os binários."""

from __future__ import annotations

from voluta.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
