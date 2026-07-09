# 3099404236 的项目主页

这个仓库托管一个轻量的个人项目主页，用来展示研究笔记、代码工具和应用 Demo。

## 本地生成

```powershell
python scripts/build_publications.py
```

然后打开 `index.html` 或 `publications.html`。

## 添加新项目

1. 如果项目有 PDF 报告，把它复制到 `papers/`。
2. 在 `data/publications.json` 里添加一条项目记录。
3. 运行 `python scripts/build_publications.py`。
4. 提交并推送。

用 `category: "research"`、`category: "tools"` 或
`category: "applications"` 控制项目出现在哪个折叠栏目里。研究类项目如果有
PDF，会生成 Highwire 风格的 citation metadata，方便以后被 Google Scholar
识别；工具和应用类项目不需要 DOI，也不需要论文式元数据。
