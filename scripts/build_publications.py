#!/usr/bin/env python3
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "publications.json"
PUB_DIR = ROOT / "publications"

CATEGORIES = [
    (
        "research",
        "研究",
        "偏研究型的笔记、实验和问题探索，通常有 PDF 报告。",
    ),
    (
        "tools",
        "工具",
        "以代码为主的工具、流程、脚本、数据处理管线和可复用组件。",
    ),
    (
        "applications",
        "应用",
        "偏实际使用的 Demo、应用、仪表盘、产品原型和落地实验。",
    ),
]


def esc(value):
    return html.escape(str(value), quote=True)


def site_url(path):
    return "https://3099404236.github.io/" + path.replace("\\", "/").lstrip("/")


def first_present(*values):
    for value in values:
        if value:
            return value
    return ""


def latest_version(item):
    versions = item.get("versions") or []
    return versions[-1] if versions else {}


def normalize_item(item):
    """Accept the old flat publication schema and the newer project schema."""
    if "versions" not in item:
        item = dict(item)
        item["category"] = item.get("category", "research")
        item["kind"] = item.get("kind", "研究笔记")
        item["summary"] = item.get("summary", item.get("abstract", ""))
        item["versions"] = [
            {
                "label": item.get("version", "v0.1"),
                "date": item.get("date", ""),
                "note": item.get("abstract", ""),
                "pdf": item.get("pdf", ""),
                "slides": item.get("slides", ""),
                "demo": item.get("demo", ""),
                "release": item.get("release", ""),
                "doi": item.get("doi", ""),
            }
        ]
    return item


def render_links(links):
    rendered = []
    for label, href in links:
        if href:
            rendered.append(f'<a href="{esc(href)}">{esc(label)}</a>')
    if not rendered:
        return ""
    return '<div class="links">' + "\n".join(rendered) + "</div>"


def local_href(href, prefix=""):
    if not href:
        return ""
    if href.startswith(("http://", "https://", "mailto:", "#", "/", "../")):
        return href
    return prefix + href


def project_links(item):
    version = latest_version(item)
    return [
        ("PDF", version.get("pdf", "")),
        ("幻灯片", version.get("slides", "")),
        ("演示", first_present(version.get("demo"), item.get("demo"))),
        ("GitHub", item.get("github", "")),
        ("发布版本", version.get("release", "")),
        ("DOI", version.get("doi", "")),
        ("讨论", item.get("discussion", "")),
    ]


def version_links(version):
    return [
        ("PDF", version.get("pdf", "")),
        ("幻灯片", version.get("slides", "")),
        ("演示", version.get("demo", "")),
        ("发布版本", version.get("release", "")),
        ("DOI", version.get("doi", "")),
    ]


def page_shell(title, body, extra_head="", stylesheet="../assets/style.css"):
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{esc(stylesheet)}">
{extra_head}</head>
<body>
  <main class="page">
{body}
  </main>
</body>
</html>
"""


def root_page_shell(title, body):
    return page_shell(title, body, stylesheet="assets/style.css")


def highwire_meta(item):
    version = latest_version(item)
    pdf = version.get("pdf", "")
    if item.get("category") != "research" or not pdf:
        return ""

    abstract = first_present(item.get("abstract"), item.get("summary"))
    lines = [
        f'  <meta name="citation_title" content="{esc(item["title"])}">',
        *(f'  <meta name="citation_author" content="{esc(author)}">' for author in item.get("authors", [])),
        f'  <meta name="citation_publication_date" content="{esc(item.get("date", "").replace("-", "/"))}">',
        f'  <meta name="citation_pdf_url" content="{esc(site_url(pdf))}">',
    ]
    if abstract:
        lines.append(f'  <meta name="citation_abstract" content="{esc(abstract)}">')
    return "\n".join(lines) + "\n"


def render_version(version, prefix=""):
    note = version.get("note", "")
    links = [(label, local_href(href, prefix)) for label, href in version_links(version)]
    return f"""        <li>
          <div class="version-head">
            <strong>{esc(version.get("label", "版本"))}</strong>
            <span>{esc(version.get("date", ""))}</span>
          </div>
          {f'<p>{esc(note)}</p>' if note else ''}
          {render_links(links)}
        </li>"""


def render_project_summary(item):
    authors = ", ".join(item.get("authors", []))
    summary = item.get("summary") or item.get("abstract", "")
    versions = "\n".join(render_version(version) for version in item.get("versions", []))
    detail_path = f"publications/{item['slug']}.html"
    open_attr = " open" if item.get("category") == "research" else ""
    return f"""    <details class="project"{open_attr}>
      <summary>
        <span class="project-main">
          <span class="project-title">{esc(item["title"])}</span>
          <span class="meta">{esc(item.get("kind", ""))} · {esc(authors)} · {esc(item.get("date", ""))}</span>
        </span>
        <span class="project-toggle">详情</span>
      </summary>
      <div class="project-body">
        {f'<p>{esc(summary)}</p>' if summary else ''}
        {render_links([("项目页", detail_path), *project_links(item)])}
        <h3>版本记录</h3>
        <ol class="timeline">
{versions}
        </ol>
      </div>
    </details>"""


def render_detail_page(item):
    authors = ", ".join(item.get("authors", []))
    abstract = first_present(item.get("abstract"), item.get("summary"))
    versions = "\n".join(render_version(version, prefix="../") for version in item.get("versions", []))

    links = [("项目列表", "../publications.html")]
    latest_links = []
    for label, href in project_links(item):
        href = local_href(href, prefix="../")
        latest_links.append((label, href))

    detail_body = f"""    <nav>{render_links(links)}</nav>
    <article>
      <p class="eyebrow">{esc(item.get("kind", ""))}</p>
      <h1>{esc(item["title"])}</h1>
      <div class="meta">{esc(authors)} · {esc(item.get("date", ""))}</div>
      {f'<h2>摘要</h2><p>{esc(abstract)}</p>' if abstract else ''}
      {render_links(latest_links)}
      <h2>版本记录</h2>
      <ol class="timeline detail-timeline">
{versions}
      </ol>
    </article>"""
    (PUB_DIR / f"{item['slug']}.html").write_text(
        page_shell(item["title"], detail_body, highwire_meta(item)),
        encoding="utf-8",
    )


def build():
    PUB_DIR.mkdir(exist_ok=True)
    items = [normalize_item(item) for item in json.loads(DATA.read_text(encoding="utf-8"))]
    slugs = {item["slug"] for item in items}

    for old_page in PUB_DIR.glob("*.html"):
        if old_page.stem not in slugs:
            old_page.unlink()

    grouped = {key: [] for key, _, _ in CATEGORIES}
    for item in items:
        grouped.setdefault(item.get("category", "research"), []).append(item)
        render_detail_page(item)

    sections = []
    for key, label, desc in CATEGORIES:
        projects = grouped.get(key, [])
        count = len(projects)
        entries = "\n".join(render_project_summary(item) for item in projects)
        empty = '<p class="empty">这个栏目还没有项目。</p>' if not projects else ""
        sections.append(
            f"""    <section class="category" id="{esc(key)}">
      <div class="category-head">
        <h2>{esc(label)}</h2>
        <span>{count} 项</span>
      </div>
      <p>{esc(desc)}</p>
{entries}
{empty}
    </section>"""
        )

    publications_body = """    <header class="site-header">
      <h1>项目</h1>
      <p>这里放研究笔记、工具和应用 Demo。每个项目都可以展开查看版本、PDF、代码，以及可选的 DOI、幻灯片或讨论链接。</p>
    </header>
    <nav><a href="index.html">首页</a><a href="#research">研究</a><a href="#tools">工具</a><a href="#applications">应用</a><a href="https://github.com/3099404236">GitHub</a></nav>
""" + "\n".join(sections)
    (ROOT / "publications.html").write_text(root_page_shell("项目", publications_body), encoding="utf-8")


if __name__ == "__main__":
    build()
