#!/usr/bin/env python3
"""Copy or assemble static pages into the Cloudflare deployment directory."""

from datetime import date
from html import escape as escape_html
from html.parser import HTMLParser
from json import loads
from pathlib import Path
from posixpath import normpath
from re import compile, escape, finditer, search
from shutil import copy2, copytree, rmtree
from subprocess import run
from urllib.parse import quote, unquote, urlsplit


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "public"
STATIC_FILES = ("_headers", "_redirects", "robots.txt")
UNPUBLISHED_FOLDERS = {"drafts", "templates"}
EXCLUDED_DIRS = {"assets", "docs", "public"} | UNPUBLISHED_FOLDERS
ROOT_ASSET_EXTENSIONS = {".ico", ".svg", ".png", ".jpg", ".jpeg", ".gif", ".webmanifest", ".xml", ".txt", ".pdf", ".css", ".js"}


def load_site():
    site = loads((ROOT / "site.json").read_text(encoding="utf-8"))
    if not isinstance(site, dict) or any(not isinstance(site.get(key), str) for key in ("name", "url", "description")):
        raise ValueError("site.json requires string name, url, and description fields")
    if not site["name"].strip() or not site["description"].strip():
        raise ValueError("site.json name and description cannot be empty")
    site["url"] = site["url"].strip()
    if site["url"]:
        url = urlsplit(site["url"])
        if url.scheme != "https" or not url.netloc or url.path not in ("", "/") or url.query or url.fragment:
            raise ValueError("site.json url must be an HTTPS site root, such as https://example.com/")
    return site


def expand_site(value, site, html=False):
    for key in ("name", "description"):
        replacement = site[key]
        if html:
            replacement = escape_html(replacement, quote=True)
        value = value.replace("{{ site_" + key + " }}", replacement)
    return value


def unpublished_filename(name):
    return name.startswith(("_", "."))


def unpublished_path(path):
    return any(unpublished_filename(part) for part in path.parts)


def ignored_asset_files(_directory, names):
    return [name for name in names if unpublished_filename(name)]


def html_sources():
    sources = [path for path in ROOT.glob("*.html") if path.is_file() and not unpublished_filename(path.name)]
    for directory in ROOT.iterdir():
        if not directory.is_dir() or directory.name in EXCLUDED_DIRS or unpublished_filename(directory.name):
            continue
        sources.extend(
            path for path in directory.rglob("*.html")
            if path.is_file()
            and not unpublished_path(path.relative_to(ROOT))
            and UNPUBLISHED_FOLDERS.isdisjoint(path.relative_to(ROOT).parts[:-1])
        )
    return sorted(sources)


def route_for(source):
    relative = source.relative_to(ROOT)
    if relative.name == "index.html":
        return relative.parent.as_posix()
    return relative.with_suffix("").as_posix()


def published_url(source, site):
    route = route_for(source)
    path = "/" if route == "." else "/" + route + ("/" if source.name == "index.html" else "")
    return site["url"].rstrip("/") + quote(path, safe="/")


def check_conflicts(sources):
    routes = {}
    for source in sources:
        routes.setdefault(route_for(source), []).append(source.relative_to(ROOT))

    conflicts = {route: paths for route, paths in routes.items() if len(paths) > 1}
    if conflicts:
        details = "\n".join(
            f"/{route}: " + ", ".join(str(path) for path in paths)
            for route, paths in sorted(conflicts.items())
        )
        raise RuntimeError("Conflicting HTML routes:\n" + details)


def render_page(source, site):
    """Assemble front-matter HTML fragments; leave complete HTML files unchanged."""
    content = source.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return None

    boundary = content.find("\n---\n", 4)
    if boundary == -1:
        raise ValueError(f"{source.relative_to(ROOT)}: missing closing front-matter --- line")

    metadata = {}
    allowed = {"title", "description", "lang", "robots", "canonical", "image", "lastmod"}
    for number, line in enumerate(content[4:boundary].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if not separator or key not in allowed or not value:
            raise ValueError(f"{source.relative_to(ROOT)}:{number}: expected a supported key: value field")
        if key in metadata:
            raise ValueError(f"{source.relative_to(ROOT)}:{number}: duplicate {key} field")
        metadata[key] = expand_site(value, site)

    if not metadata.get("title") or not metadata.get("lang"):
        raise ValueError(f"{source.relative_to(ROOT)}: fragment pages require title and lang fields")
    if "lastmod" in metadata:
        try:
            if date.fromisoformat(metadata["lastmod"]).isoformat() != metadata["lastmod"]:
                raise ValueError()
        except ValueError:
            raise ValueError(f"{source.relative_to(ROOT)}: lastmod must be a valid YYYY-MM-DD date") from None
    body = expand_site(content[boundary + len("\n---\n"):].strip(), site, html=True)
    if not body:
        raise ValueError(f"{source.relative_to(ROOT)}: fragment page has no HTML content")

    if "canonical" not in metadata and site["url"] and source.relative_to(ROOT) != Path("404.html"):
        metadata["canonical"] = published_url(source, site)

    tags = []
    for field in ("description", "robots"):
        if field in metadata:
            tags.append(f'  <meta name="{field}" content="{escape_html(metadata[field], quote=True)}">')
    if "canonical" in metadata:
        tags.append(f'  <link rel="canonical" href="{escape_html(metadata["canonical"], quote=True)}">')

    tags.append('  <meta property="og:type" content="website">')
    tags.append(f'  <meta property="og:title" content="{escape_html(metadata["title"], quote=True)}">')
    if "description" in metadata:
        tags.append(f'  <meta property="og:description" content="{escape_html(metadata["description"], quote=True)}">')
    if "canonical" in metadata:
        tags.append(f'  <meta property="og:url" content="{escape_html(metadata["canonical"], quote=True)}">')
    if "image" in metadata:
        tags.append(f'  <meta property="og:image" content="{escape_html(metadata["image"], quote=True)}">')

    templates = ROOT / "templates"
    head = (templates / "head.html").read_text(encoding="utf-8")
    for name, value in {
        "title": escape_html(metadata["title"], quote=True),
        "metadata": "\n".join(tags),
    }.items():
        token = "{{ " + name + " }}"
        if head.count(token) != 1:
            raise ValueError(f"templates/head.html must contain exactly one {token}")
        head = head.replace(token, value)

    rendered = (templates / "base.html").read_text(encoding="utf-8")
    sections = {
        "lang": escape_html(metadata["lang"], quote=True),
        "head": head.strip(),
        "header": expand_site((templates / "header.html").read_text(encoding="utf-8").strip(), site, html=True),
        "content": body,
        "footer": expand_site((templates / "footer.html").read_text(encoding="utf-8").strip(), site, html=True),
    }
    # Accept the earlier base template while its empty body-attributes token is removed.
    rendered = rendered.replace("{{ body_attributes }}", "")
    for name, value in sections.items():
        token = "{{ " + name + " }}"
        if rendered.count(token) != 1:
            raise ValueError(f"templates/base.html must contain exactly one {token}")
        rendered = rendered.replace(token, value)
    return rendered, metadata.get("lastmod")


def srcset_urls(value):
    """Read srcset URL tokens without splitting commas inside URLs."""
    index = 0
    while index < len(value):
        while index < len(value) and (value[index].isspace() or value[index] == ","):
            index += 1
        start = index
        while index < len(value) and not value[index].isspace():
            index += 1
        url = value[start:index].rstrip(",")
        if url:
            yield url
        if index > start and value[index - 1] == ",":
            continue
        # Skip descriptors until the next candidate separator.
        while index < len(value) and value[index] != ",":
            index += 1
        index += 1


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.assets = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append((self.getpos()[0], href))
        attributes = dict(attrs)
        if tag.lower() in {"img", "source"} and attributes.get("srcset"):
            for url in srcset_urls(attributes["srcset"]):
                self.assets.append((self.getpos()[0], url))
        if tag.lower() in {"img", "script", "source", "video", "audio"} and attributes.get("src"):
            self.assets.append((self.getpos()[0], attributes["src"]))
        if tag.lower() == "link" and attributes.get("href") and any(
            item in attributes.get("rel", "").lower().split() for item in ("stylesheet", "icon", "preload", "modulepreload", "manifest")
        ):
            self.assets.append((self.getpos()[0], attributes["href"]))


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


def check_asset(target, source, line, href, errors):
    """Check a deployed /assets/ path; return whether it is an asset reference."""
    relative = target.lstrip("/")
    if relative.startswith("assets/"):
        assets_root = ROOT / "assets"
        file = assets_root / relative[len("assets/"):]
        exists = file.is_file() and not unpublished_path(file.relative_to(assets_root)) and file.resolve().is_relative_to(assets_root.resolve())
    elif "/" not in relative and Path(relative).suffix.lower() in ROOT_ASSET_EXTENSIONS:
        file = ROOT / relative
        exists = file.is_file() and not unpublished_filename(file.name)
    else:
        return False
    if not exists:
        errors.append(f"{source.relative_to(ROOT)}:{line}: {href} (missing local asset)")
    return True


def check_css_assets(errors):
    """Check simple CSS url() references relative to each stylesheet."""
    assets = ROOT / "assets"
    if not assets.is_dir():
        return
    for source in sorted(assets.rglob("*.css")):
        if unpublished_path(source.relative_to(assets)):
            continue
        css = source.read_text(encoding="utf-8")
        # Consume comments and quoted strings before matching real url() tokens.
        tokens = r"""(?P<comment>/\*[\s\S]*?\*/)|(?P<url>url\(\s*(?:"([^"]*)"|'([^']*)'|([^\s)]*))\s*\))|(?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')"""
        for match in finditer(tokens, css, flags=2):
            if match.group("url") is None:
                continue
            href = next((part for part in match.groups()[2:5] if part is not None), "").strip()
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            if "\\" in path or "\x00" in path:
                continue
            base = "/" + source.relative_to(ROOT).parent.as_posix() + "/"
            target = normpath(path if path.startswith("/") else base + path)
            line = css.count("\n", 0, match.start()) + 1
            check_asset(target, source, line, href, errors)


def check_internal_links(sources, rendered_pages):
    routes = {route_for(source) for source in sources}
    redirects = redirect_sources()
    errors = []
    for source in sources:
        parser = LinkParser()
        html = rendered_pages[source] if source in rendered_pages else source.read_text(encoding="utf-8")
        parser.feed(html)
        parent = source.relative_to(ROOT).parent
        # Flat page.html URLs omit the slash; index.html folders retain it.
        # Both resolve relative links from their containing URL directory.
        base = "/" if parent == Path(".") else "/" + parent.as_posix() + "/"
        for line, href in parser.assets:
            url = urlsplit(href.strip())
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            if "\\" in path or "\x00" in path:
                continue
            target = normpath(path if path.startswith("/") else base + path)
            check_asset(target, source, line, href, errors)
        for line, href in parser.links:
            url = urlsplit(href.strip())
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            if "\\" in path or "\x00" in path:
                continue
            target = normpath(path if path.startswith("/") else base + path)
            if check_asset(target, source, line, href, errors):
                continue
            if target == "/":
                route = "."
            else:
                route = target.lstrip("/").rstrip("/")
                if route == "index.html" or route.endswith("/index.html"):
                    route = route[:-11] or "."
                elif route.endswith(".html"):
                    route = route[:-5] or "."
                elif Path(route).suffix:
                    continue  # Non-HTML assets are outside this check.
            if route not in routes and not any(pattern.fullmatch(candidate) for pattern in redirects for candidate in (target, target + "/" if path.endswith("/") and target != "/" else target)):
                errors.append(f"{source.relative_to(ROOT)}:{line}: {href} (missing HTML page)")
    check_css_assets(errors)
    if errors:
        print(f"Warning: {len(errors)} unresolved local reference(s) (build continues):\n" + "\n".join(errors))


class SitemapParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.noindex = False
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag.lower() == "meta" and (attributes.get("name") or "").lower() in {"robots", "googlebot"}:
            directives = (attributes.get("content") or "").lower().split(",")
            if any(directive.strip() == "noindex" for directive in directives):
                self.noindex = True
        if tag.lower() == "link" and "canonical" in (attributes.get("rel") or "").lower().split():
            self.canonical = attributes.get("href")


def git_modification_dates(sources):
    """Use committed source dates, never checkout file times or build time."""
    try:
        shallow = run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, capture_output=True, text=True)
        if shallow.returncode != 0 or shallow.stdout.strip() == "true":
            return {}
        history = run(
            ["git", "log", "--format=SITEMAP_DATE:%cs", "--name-only", "--diff-filter=ACMR", "--", "."],
            cwd=ROOT, capture_output=True, text=True,
        )
    except OSError:
        return {}
    if history.returncode != 0:
        return {}

    wanted = {source.relative_to(ROOT).as_posix() for source in sources}
    dates = {}
    current_date = None
    for line in history.stdout.splitlines():
        if line.startswith("SITEMAP_DATE:"):
            current_date = line[len("SITEMAP_DATE:"):]
        elif line in wanted and line not in dates and current_date:
            dates[line] = current_date
            if len(dates) == len(wanted):
                break
    return dates


def write_sitemap(site, sources, rendered_pages, lastmod_overrides):
    if not site["url"]:
        return

    dates = git_modification_dates(sources)
    redirects = redirect_sources()
    entries = []
    missing_dates = 0
    for source in sources:
        if source.relative_to(ROOT) == Path("404.html"):
            continue
        url = published_url(source, site)
        if any(pattern.fullmatch(urlsplit(url).path) for pattern in redirects):
            continue
        parser = SitemapParser()
        parser.feed(rendered_pages.get(source) or source.read_text(encoding="utf-8"))
        if parser.noindex or (parser.canonical and parser.canonical != url):
            continue
        entry = f"  <url>\n    <loc>{escape_html(url, quote=True)}</loc>"
        lastmod = lastmod_overrides.get(source) or dates.get(source.relative_to(ROOT).as_posix())
        if lastmod:
            entry += f"\n    <lastmod>{lastmod}</lastmod>"
        else:
            missing_dates += 1
        entries.append(entry + "\n  </url>")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "\n".join(entries) + ("\n" if entries else "") + "</urlset>\n"
    (OUTPUT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"Generated sitemap.xml with {len(entries)} URL(s)")
    if missing_dates:
        print(f"Note: <lastmod> omitted for {missing_dates} URL(s) without a manual date or complete Git history")


def main():
    site = load_site()
    sources = html_sources()
    check_conflicts(sources)
    rendered_pages = {}
    lastmod_overrides = {}
    for source in sources:
        page = render_page(source, site)
        if page is not None:
            rendered, lastmod = page
            rendered_pages[source] = rendered
            if lastmod:
                lastmod_overrides[source] = lastmod
    check_internal_links(sources, rendered_pages)

    if OUTPUT.is_symlink():
        raise RuntimeError("Refusing to clean a symlinked public/ directory")
    if OUTPUT.exists():
        rmtree(OUTPUT)
    OUTPUT.mkdir()

    for name in STATIC_FILES:
        source = ROOT / name
        if source.is_file():
            copy2(source, OUTPUT / name)

    for source in ROOT.iterdir():
        if (
            source.is_file()
            and source.name not in STATIC_FILES
            and source.suffix.lower() in ROOT_ASSET_EXTENSIONS
            and not unpublished_filename(source.name)
        ):
            copy2(source, OUTPUT / source.name)

    for source in sources:
        destination = OUTPUT / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source in rendered_pages:
            destination.write_text(rendered_pages[source], encoding="utf-8")
        else:
            copy2(source, destination)

    assets = ROOT / "assets"
    if assets.is_dir():
        copytree(assets, OUTPUT / "assets", ignore=ignored_asset_files, dirs_exist_ok=True)

    write_sitemap(site, sources, rendered_pages, lastmod_overrides)

    print("Static files copied to public/")


if __name__ == "__main__":
    main()
