"""Check the rendered student book before uploading it to GitHub Pages."""

from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import sys
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        for key in ("href", "src"):
            if key in attributes and attributes[key]:
                self.links.append(attributes[key])


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "course/_book").resolve()
    errors = []
    forbidden = {"instructor", "_instructor", ".working", ".venv", ".git", ".env"}
    required = (
        "index.html", "setup.html", "glossary.html", "reading.html", "search.json",
        "lectures/01-ai-and-science.html", "lectures/02-learning-from-data.html",
        "lectures/03-mof-uptake.html", "activities/calibration.html",
        "downloads/introductory-setup.zip", "downloads/mof-practical.zip",
    )
    for name in required:
        if not (root / name).is_file():
            errors.append(f"Missing public resource: {name}")

    pages = {}
    private_roots = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        for index, part in enumerate(relative.parts):
            if part in forbidden:
                private_roots.add(str(Path(*relative.parts[:index + 1])))
                break
        if path.is_symlink():
            errors.append(f"Symlink in Pages artifact: {relative}")
        if path.suffix == ".html" and path.is_file():
            page = Page()
            page.feed(path.read_text(encoding="utf-8"))
            pages[path] = page

    errors.extend(f"Private path in student output: {name}" for name in sorted(private_roots))
    links = 0
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            links += 1
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(root):
                errors.append(f"Link leaves student output: {path.name}: {link}")
            elif not target.exists():
                errors.append(f"Missing local target: {path.name}: {link}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"Missing section anchor: {path.name}: {link}")

    search_path = root / "search.json"
    if search_path.is_file():
        search = search_path.read_text(encoding="utf-8")
        json.loads(search)
        for marker in ("authorial-direction", "source-map.html", "board-and-demo-plan"):
            if marker in search:
                errors.append(f"Instructor material in public search: {marker}")

    for archive in (root / "downloads").glob("*.zip"):
        with ZipFile(archive) as bundle:
            for member in bundle.namelist():
                path = PurePosixPath(member)
                if path.is_absolute() or ".." in path.parts or forbidden.intersection(path.parts):
                    errors.append(f"Unexpected download member: {archive.name}: {member}")

    if errors:
        message = "\n".join(errors[:25])
        if len(errors) > 25:
            message += f"\n... and {len(errors) - 25} further errors."
        raise SystemExit(message)
    print(f"Checked {len(pages)} HTML pages and {links} local links; student output is ready.")


if __name__ == "__main__":
    main()
