# Tidepool Icons

A file icon theme: each file is a sheet with a colored tag that names its language — **TS**, **PY**, **GO**, **RS**,
**SW**, **{}**, **>_** — and folders are tinted by what they hold. One set of icons for light and dark.

Pick it in Settings › Appearance › File Icon Theme › **Tidepool**. It runs nothing.

- **Languages:** TypeScript, JavaScript (and their JSX), Python, Go, Rust, Swift, Ruby, Java, Kotlin, C, C++, C#,
  Objective-C, PHP, Lua, Zig, shell, PowerShell, HTML, CSS, SCSS, Vue, Svelte, SQL, GraphQL.
- **Data and config:** JSON, YAML, TOML, XML and plists, INI, `.env`, Markdown, CSV, SQLite, PDF, images, SVG, logs.
- **Known files:** `package.json`, `Dockerfile` and compose files, `Makefile`, `.gitignore`, `LICENSE`, `go.mod`,
  `Cargo.toml`, `Package.swift`, `Gemfile`, `pyproject.toml`, `tsconfig.json`.
- **Folders:** sources (`src`, `lib`, `Sources`) green, tests orange, docs teal, `scripts` and `bin` mustard, assets
  purple, `.git` and `.github` red, dependencies and build output (`node_modules`, `dist`, `.build`, `target`…) gray.
  Any other file is a plain sheet, any other folder blue.

The icons are SVGs written by `generate.py` from its tables: add a row there, run `python3 generate.py`, and commit
`icons/` and `theme.json` with it. The theme is in VS Code's format, so it works there too.
