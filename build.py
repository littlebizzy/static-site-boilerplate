#!/usr/bin/env python3
"""Copy static site files into the Cloudflare deployment directory."""

from pathlib import Path
from shutil import copy2, copytree, rmtree


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "public"
STATIC_FILES = ("_headers", "_redirects", "robots.txt")
EXCLUDED_DIRS = {"assets", "docs", "public"}


def main():
    if OUTPUT.is_symlink():
        raise RuntimeError("Refusing to clean a symlinked public/ directory")
    if OUTPUT.exists():
        rmtree(OUTPUT)
    OUTPUT.mkdir()

    for name in STATIC_FILES:
        source = ROOT / name
        if source.is_file():
            copy2(source, OUTPUT / name)

    for source in ROOT.glob("*.html"):
        if source.is_file():
            copy2(source, OUTPUT / source.name)

    for directory in ROOT.iterdir():
        if not directory.is_dir() or directory.name in EXCLUDED_DIRS or directory.name.startswith("."):
            continue
        for source in directory.rglob("*.html"):
            destination = OUTPUT / source.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            copy2(source, destination)

    assets = ROOT / "assets"
    if assets.is_dir():
        copytree(assets, OUTPUT / "assets", dirs_exist_ok=True)

    print("Static files copied to public/")


if __name__ == "__main__":
    main()
