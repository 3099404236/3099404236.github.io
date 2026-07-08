# 3099404236 Research Notes

This repository hosts a lightweight academic homepage for research notes.

## Local build

```powershell
python scripts/build_publications.py
```

Then open `index.html` or `publications.html`.

## Add a new note

1. Copy the note PDF into `papers/`.
2. Add one item to `data/publications.json`.
3. Run `python scripts/build_publications.py`.
4. Commit and push.

Each generated publication detail page includes Highwire-style citation metadata for Google Scholar compatibility. Indexing is not guaranteed.

