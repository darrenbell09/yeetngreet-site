"""MkDocs hooks: ship marketing styles.css + logo into the docs site build."""

from __future__ import annotations

from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files


def _repo_root(config: MkDocsConfig) -> Path:
    return Path(config.config_file_path).resolve().parent


def on_files(files: Files, config: MkDocsConfig) -> Files:
    """Expose root marketing assets so docs can load the same styles.css / logo.png."""
    root = _repo_root(config)
    for name in ("styles.css", "logo.png"):
        src = root / name
        if not src.is_file():
            continue
        # Drop any prior entry (rebuild / serve) then add from repo root.
        existing = files.get_file_from_path(name)
        if existing is not None:
            files.remove(existing)
        files.append(
            File(
                path=name,
                src_dir=str(root),
                dest_dir=config.site_dir,
                use_directory_urls=config.use_directory_urls,
            )
        )
    return files
