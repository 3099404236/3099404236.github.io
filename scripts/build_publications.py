#!/usr/bin/env python3
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "publications.json"
PUB_DIR = ROOT / "publications"


def esc(value):
    return html.escape(str(value), quote=True)


def site_url(path):
    return "https://3099404236.github.io/" + path.replace("\\", "/").lstrip("/")


def render_links(item):
    links = []
    if item.get("pdf"):
        links.append(f'<a href="{esc(item["pdf"])}">PDF</a>')
    if item.get("github"):
        links.append(f'<a href="{esc(item["github"])}">GitHub</a>')
    if item.get("doi"):
        links.append(f'<a href="{esc(item["doi"])}">DOI</a>')
    if item.get("discussion"):
        links.append(f'<a href="{esc(item["discussion"])}">Discussion</a>')
    return '<div class="links">' + "\n".join(links) + "</div>"


def page_shell(title, body, extra_head=""):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="../assets/style.css">
{extra_head}</head>
<body>
  <main class="page">
{body}
  </main>
</body>
</html>
"""


def root_page_shell(title, body):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <main class="page">
{body}
  </main>
</body>
</html>
"""


def highwire_meta(item):
    lines = [
        f'  <meta name="citation_title" content="{esc(item["title"])}">',
        *(f'  <meta name="citation_author" content="{esc(author)}">' for author in item.get("authors", [])),
        f'  <meta name="citation_publication_date" content="{esc(item.get("date", "").replace("-", "/"))}">',
    ]
    if item.get("pdf"):
        lines.append(f'  <meta name="citation_pdf_url" content="{esc(site_url(item["pdf"]))}">')
    if item.get("abstract"):
        lines.append(f'  <meta name="citation_abstract" content="{esc(item["abstract"])}">')
    return "\n".join(lines) + "\n"


def build():
    PUB_DIR.mkdir(exist_ok=True)
    items = json.loads(DATA.read_text(encoding="utf-8"))

    entries = []
    for item in items:
        slug = item["slug"]
        detail_path = f"publications/{slug}.html"
        authors = ", ".join(item.get("authors", []))
        entries.append(
            f"""    <article class="pub">
      <h2><a href="{esc(detail_path)}">{esc(item["title"])}</a></h2>
      <div class="meta">{esc(authors)} · {esc(item.get("date", ""))}</div>
      <p>{esc(item.get("abstract", ""))}</p>
      {render_links(item)}
    </article>"""
        )

        detail_body = f"""    <p><a href="../publications.html">Back to research notes</a></p>
    <article>
      <h1>{esc(item["title"])}</h1>
      <div class="meta">{esc(authors)} · {esc(item.get("date", ""))}</div>
      <h2>Abstract</h2>
      <p>{esc(item.get("abstract", ""))}</p>
      {render_links({"pdf": "../" + item.get("pdf", ""), "github": item.get("github", ""), "doi": item.get("doi", ""), "discussion": item.get("discussion", "")})}
    </article>"""
        (PUB_DIR / f"{slug}.html").write_text(
            page_shell(item["title"], detail_body, highwire_meta(item)),
            encoding="utf-8",
        )

    publications_body = """    <header class="site-header">
      <h1>Research Notes</h1>
      <p>Lightweight, citable research notes with code, data, and discussion links.</p>
    </header>
    <nav><a href="index.html">Home</a><a href="https://github.com/3099404236">GitHub</a></nav>
""" + "\n".join(entries)
    (ROOT / "publications.html").write_text(root_page_shell("Research Notes", publications_body), encoding="utf-8")


if __name__ == "__main__":
    build()

