# 3099404236 Projects

This repository hosts a lightweight academic/project homepage. It supports
research notes, code-first tools, and applied demos.

## Local build

```powershell
python scripts/build_publications.py
```

Then open `index.html` or `publications.html`.

## Add a new project

1. Copy the PDF report into `papers/` if the project has one.
2. Add one item to `data/publications.json`.
3. Run `python scripts/build_publications.py`.
4. Commit and push.

Use `category: "research"`, `category: "tools"`, or
`category: "applications"` to control which collapsible section the project
appears in. Research projects with a PDF get Highwire-style citation metadata
for Google Scholar compatibility. Tool and application projects do not need DOI
or paper-style metadata.
