#!/usr/bin/env python3
"""Copy static site files into the Cloudflare deployment directory."""

from html.parser import HTMLParser
from pathlib import Path
from posixpath import normpath
from re import compile, escape
from shutil import copy2, copytree, rmtree
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "public"
STATIC_FILES = ("_headers", "_redirects", "robots.txt")
EXCLUDED_DIRS = {"assets", "docs", "drafts", "public"}


def html_sources():
    sources = [path for path in ROOT.glob("*.html") if path.is_file()]
    for directory in ROOT.iterdir():
        if not directory.is_dir() or directory.name in EXCLUDED_DIRS or directory.name.startswith("."):
            continue
        sources.extend(path for path in directory.rglob("*.html") if path.is_file())
    return sorted(sources)


def route_for(source):
    relative = source.relative_to(ROOT)
    if relative.name == "index.html":
        return relative.parent.as_posix()
    return relative.with_suffix("").as_posix()


def check_conflicts(sources):
    routes = {}
    for source in sources:
        routes.setdefault(route_for(source), []).append(source.relative_to(ROOT))

    conflicts = {route: paths for route, paths in routes.items() if len(paths) > 1}
    if conflicts:
        details = "\n".join(
            f"/{route}/: " + ", ".join(str(path) for path in paths)
            for route, paths in sorted(conflicts.items())
        )
        raise RuntimeError("Conflicting HTML routes:\n" + details)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append((self.getpos()[0], href))


def redirect_sources():
    """Read active local redirect patterns; ignore comments and external sources."""
    redirects = ROOT / "_redirects"
    patterns = []
    if redirects.is_file():
        for line in redirects.read_text(encoding="utf-8").splitlines():
            fields = line.split()
            if len(fields) < 3 or fields[0].startswith("#"):
                continue
            source, _, status = fields[:3]
            if not source.startswith("/") or status not in {"301", "302", "303", "307", "308"}:
                continue
            if source.endswith("/*"):
                patterns.append(compile("^" + escape(source[:-1]) + ".*$"))
            elif "*" not in source and ":" not in source:
                patterns.append(compile("^" + escape(source) + "$"))
    return patterns


def check_internal_links(sources):
    routes = {route_for(source) for source in sources}
    redirects = redirect_sources()
    errors = []
    for source in sources:
        parser = LinkParser()
        parser.feed(source.read_text(encoding="utf-8"))
        source_route = route_for(source)
        base = "/" + source_route.strip("/") + "/" if source.name == "index.html" else "/" + source.relative_to(ROOT).parent.as_posix().strip("/") + "/"
        for line, href in parser.links:
            url = urlsplit(href.strip())
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            if "\\" in path or "\x00" in path:
                continue
            target = normpath(path if path.startswith("/") else base + path)
            if target == "/":
                route = "."
            else:
                route = target.lstrip("/").rstrip("/")
                if route.endswith("/index.html"):
                    route = route[:-11] or "."
                elif route.endswith(".html"):
                    route = route[:-5] or "."
                elif Path(route).suffix:
                    continue  # Non-HTML assets are outside this check.
            if route not in routes and not any(pattern.fullmatch(target) for pattern in redirects):
                errors.append(f"{source.relative_to(ROOT)}:{line}: {href} (missing HTML page)")
    if errors:
        raise RuntimeError("Broken internal page links:\n" + "\n".join(errors))


def main():
    sources = html_sources()
    check_conflicts(sources)
    check_internal_links(sources)

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
