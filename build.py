#!/usr/bin/env python3
"""Copy static site files into the Cloudflare deployment directory."""

from pathlib import Path
from shutil import copy2, copytree, rmtree


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "public"
STATIC_FILES = ("_headers", "_redirects", "robots.txt")
EXCLUDED_DIRS = {"assets", "docs", "public"}


def html_sources():
    sources = [path for path in ROOT.glob("*.html") if path.is_file()]
    for directory in ROOT.iterdir():
        if not directory.is_dir() or directory.name in EXCLUDED_DIRS or directory.name.startswith("."):
            continue
        sources.extend(path for path in directory.rglob("*.html") if path.is_file())
    return sorted(sources)


def check_conflicts(sources):
    routes = {}
    for source in sources:
        relative = source.relative_to(ROOT)
        if relative.name == "index.html":
            route = relative.parent.as_posix()
        else:
            route = relative.with_suffix("").as_posix()
        routes.setdefault(route, []).append(relative)

    conflicts = {route: paths for route, paths in routes.items() if len(paths) > 1}
    if conflicts:
        details = "\n".join(
            f"/{route}/: " + ", ".join(str(path) for path in paths)
            for route, paths in sorted(conflicts.items())
        )
        raise RuntimeError("Conflicting HTML routes:\n" + details)


def main():
    sources = html_sources()
    check_conflicts(sources)

    if OUTPUT.is_symlink():
        raise RuntimeError("Refusing to clean a symlinked public/ directory")
    if OUTPUT.exists():
        rmtree(OUTPUT)
    OUTPUT.mkdir()

    for name in STATIC_FILES:
        source = ROOT / name
        if source.is_file():
            copy2(source, OUTPUT / name)

    for source in sources:
        destination = OUTPUT / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, destination)

    assets = ROOT / "assets"
    if assets.is_dir():
        copytree(assets, OUTPUT / "assets", dirs_exist_ok=True)

    print("Static files copied to public/")


if __name__ == "__main__":
    main()
