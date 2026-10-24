#!/usr/bin/env python3
"""Copy static site files into the Cloudflare deployment directory."""

from pathlib import Path
from shutil import copy2, copytree


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "public"
STATIC_FILES = ("_headers", "_redirects", "robots.txt")


def main():
    OUTPUT.mkdir(exist_ok=True)

    for name in STATIC_FILES:
        source = ROOT / name
        if source.is_file():
            copy2(source, OUTPUT / name)

    for source in ROOT.glob("*.html"):
        if source.is_file():
            copy2(source, OUTPUT / source.name)

    assets = ROOT / "assets"
    if assets.is_dir():
        copytree(assets, OUTPUT / "assets", dirs_exist_ok=True)

    print("Static files copied to public/")


if __name__ == "__main__":
    main()
