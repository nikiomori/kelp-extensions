#!/usr/bin/env python3
"""Writes icons/*.svg and theme.json, the Tidepool file icon theme: a sheet with a colored tag for files, a tinted
folder for folders. Change the tables below and run it again (python3 generate.py). Standard library only.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GRAY = "#8e949c"   # the sheet: about 3:1 on white and on a dark sidebar, so one set works in light and dark
DARK = "#1f2328"   # tag text on pale tags

# Tags: icon → (text, color, what it's for): extensions, and whole file names (those with a dot or a capital),
# which win over extensions.
TAGS = {
    "ts":     ("TS",  "#3178c6", ["ts", "mts", "cts", "tsconfig.json"]),
    "tsx":    ("TSX", "#3178c6", ["tsx"]),
    "js":     ("JS",  "#f0db4f", ["js", "mjs", "cjs", "jsconfig.json"]),
    "jsx":    ("JSX", "#f0db4f", ["jsx"]),
    "py":     ("PY",  "#3776ab", ["py", "pyi", "pyw", "requirements.txt", "pyproject.toml", "Pipfile"]),
    "go":     ("GO",  "#00add8", ["go", "go.mod", "go.sum"]),
    "rs":     ("RS",  "#ce422b", ["rs", "Cargo.toml", "Cargo.lock"]),
    "swift":  ("SW",  "#f05138", ["swift", "Package.swift", "Package.resolved"]),
    "rb":     ("RB",  "#cc342d", ["rb", "erb", "Gemfile", "Gemfile.lock", "Rakefile"]),
    "java":   ("J",   "#e76f00", ["java", "jar"]),
    "kt":     ("KT",  "#7f52ff", ["kt", "kts"]),
    "c":      ("C",   "#5c6bc0", ["c"]),
    "h":      ("H",   "#8e6cc0", ["h"]),
    "cpp":    ("C++", "#00599c", ["cpp", "cc", "cxx", "mm"]),
    "hpp":    ("H++", "#6d4fb3", ["hpp", "hh", "hxx"]),
    "cs":     ("C#",  "#239120", ["cs"]),
    "m":      ("M",   "#438eff", ["m"]),
    "php":    ("PHP", "#777bb4", ["php"]),
    "lua":    ("LUA", "#4054b2", ["lua"]),
    "zig":    ("ZIG", "#f7a41d", ["zig", "zon"]),
    "sh":     (">_",  "#3c9a3c", ["sh", "bash", "zsh", "fish", ".zshrc", ".bashrc", ".profile", ".zprofile"]),
    "ps":     ("PS",  "#2671be", ["ps1", "psm1"]),
    "html":   ("<>",  "#e34f26", ["html", "htm"]),
    "css":    ("CSS", "#1572b6", ["css"]),
    "scss":   ("SC",  "#cd6799", ["scss", "sass"]),
    "vue":    ("VUE", "#41b883", ["vue"]),
    "svelte": ("SV",  "#ff3e00", ["svelte"]),
    "json":   ("{}",  "#f5a623", ["json", "jsonc", "json5", "jsonl"]),
    "yaml":   ("YML", "#cb171e", ["yaml", "yml"]),
    "toml":   ("TML", "#9c4221", ["toml"]),
    "xml":    ("XML", "#e37933", ["xml", "plist", "xib", "storyboard"]),
    "cfg":    ("CFG", "#6d8086", ["ini", "cfg", "conf", "properties", ".editorconfig", ".kelp.yaml"]),
    "env":    ("ENV", "#ecd53f", ["env", ".env", ".env.local", ".env.example", ".env.development", ".env.production"]),
    "md":     ("MD",  "#519aba", ["md", "markdown", "mdx"]),
    "pdf":    ("PDF", "#d93025", ["pdf"]),
    "csv":    ("CSV", "#1d8348", ["csv", "tsv"]),
    "sql":    ("SQL", "#dd8a00", ["sql"]),
    "db":     ("DB",  "#0f80cc", ["db", "sqlite", "sqlite3"]),
    "img":    ("IMG", "#a065cb", ["png", "jpg", "jpeg", "gif", "webp", "ico", "icns", "bmp", "tiff", "heic"]),
    "svg":    ("SVG", "#ffb13b", ["svg"]),
    "log":    ("LOG", "#7f8c8d", ["log"]),
    "gql":    ("GQL", "#e10098", ["graphql", "gql"]),
    "docker": ("DKR", "#2496ed", ["Dockerfile", "Containerfile", ".dockerignore", "compose.yml", "compose.yaml",
                                  "docker-compose.yml", "docker-compose.yaml"]),
    "make":   ("MK",  "#427819", ["mk", "Makefile", "GNUmakefile", "Justfile"]),
    "npm":    ("NPM", "#cb3837", ["package.json", "package-lock.json", ".npmrc"]),
    "git":    ("GIT", "#f05032", [".gitignore", ".gitattributes", ".gitmodules", ".gitkeep"]),
    "license": ("LIC", "#b8860b", ["LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "COPYING"]),
}
PALE = {"js", "jsx", "json", "env", "svg", "zig"}   # dark text on these

# Folders: icon → (color, the folder names it's for). Any other folder is "folder".
FOLDERS = {
    "folder":         ("#6c9bd2", []),
    "folder-src":     ("#4caf7a", ["src", "source", "sources", "lib", "app"]),
    "folder-test":    ("#e8964a", ["test", "tests", "__tests__", "spec", "specs", "e2e"]),
    "folder-docs":    ("#3fa7b5", ["docs", "doc", "documentation"]),
    "folder-scripts": ("#d4a72c", ["scripts", "bin", "tools"]),
    "folder-assets":  ("#b07cd8", ["assets", "images", "img", "icons", "fonts", "media", "public", "static", "resources"]),
    "folder-git":     ("#f05032", [".git", ".github", ".gitlab"]),
    "folder-deps":    ("#8a8f98", ["node_modules", "vendor", "pods", ".build", "build", "dist", "out", "target",
                                   "coverage", ".next", "__pycache__", ".venv", "venv", "deriveddata"]),
}

# A stroke font for the tags: char → (width, polylines), in a box 1 wide (times width) and 1 tall, y down.
GLYPHS = {
    "A": (1, [[(0, 1), (0, 0.25), (0.25, 0), (0.75, 0), (1, 0.25), (1, 1)], [(0, 0.6), (1, 0.6)]]),
    "B": (1, [[(0, 0), (0, 1), (0.75, 1), (1, 0.8), (1, 0.7), (0.75, 0.5), (0, 0.5)], [(0, 0), (0.7, 0), (0.95, 0.2), (0.95, 0.3), (0.7, 0.5)]]),
    "C": (1, [[(1, 0), (0, 0), (0, 1), (1, 1)]]),
    "D": (1, [[(0, 0), (0, 1), (0.6, 1), (1, 0.7), (1, 0.3), (0.6, 0), (0, 0)]]),
    "E": (1, [[(1, 0), (0, 0), (0, 1), (1, 1)], [(0, 0.5), (0.8, 0.5)]]),
    "F": (1, [[(1, 0), (0, 0), (0, 1)], [(0, 0.5), (0.8, 0.5)]]),
    "G": (1, [[(1, 0), (0, 0), (0, 1), (1, 1), (1, 0.55), (0.5, 0.55)]]),
    "H": (1, [[(0, 0), (0, 1)], [(1, 0), (1, 1)], [(0, 0.5), (1, 0.5)]]),
    "I": (0, [[(0, 0), (0, 1)]]),
    "J": (1, [[(1, 0), (1, 1), (0, 1), (0, 0.65)]]),
    "K": (1, [[(0, 0), (0, 1)], [(1, 0), (0, 0.6)], [(0.4, 0.4), (1, 1)]]),
    "L": (1, [[(0, 0), (0, 1), (1, 1)]]),
    "M": (1.2, [[(0, 1), (0, 0), (0.6, 0.55), (1.2, 0), (1.2, 1)]]),
    "N": (1, [[(0, 1), (0, 0), (1, 1), (1, 0)]]),
    "O": (1, [[(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]]),
    "P": (1, [[(0, 1), (0, 0), (1, 0), (1, 0.55), (0, 0.55)]]),
    "Q": (1, [[(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], [(0.55, 0.65), (1, 1.1)]]),
    "R": (1, [[(0, 1), (0, 0), (1, 0), (1, 0.55), (0, 0.55)], [(0.45, 0.55), (1, 1)]]),
    "S": (1, [[(1, 0), (0, 0), (0, 0.5), (1, 0.5), (1, 1), (0, 1)]]),
    "T": (1, [[(0, 0), (1, 0)], [(0.5, 0), (0.5, 1)]]),
    "U": (1, [[(0, 0), (0, 1), (1, 1), (1, 0)]]),
    "V": (1, [[(0, 0), (0.5, 1), (1, 0)]]),
    "W": (1.3, [[(0, 0), (0.3, 1), (0.65, 0.4), (1, 1), (1.3, 0)]]),
    "X": (1, [[(0, 0), (1, 1)], [(1, 0), (0, 1)]]),
    "Y": (1, [[(0, 0), (0.5, 0.5), (1, 0)], [(0.5, 0.5), (0.5, 1)]]),
    "Z": (1, [[(0, 0), (1, 0), (0, 1), (1, 1)]]),
    "+": (1, [[(0.5, 0.2), (0.5, 0.8)], [(0.1, 0.5), (0.9, 0.5)]]),
    "#": (1.2, [[(0.35, 0.05), (0.35, 0.95)], [(0.85, 0.05), (0.85, 0.95)], [(0, 0.35), (1.2, 0.35)], [(0, 0.7), (1.2, 0.7)]]),
    "{": (0.9, [[(0.9, 0), (0.45, 0), (0.45, 0.4), (0, 0.5), (0.45, 0.6), (0.45, 1), (0.9, 1)]]),
    "}": (0.9, [[(0, 0), (0.45, 0), (0.45, 0.4), (0.9, 0.5), (0.45, 0.6), (0.45, 1), (0, 1)]]),
    "<": (0.9, [[(0.9, 0.1), (0, 0.5), (0.9, 0.9)]]),
    ">": (0.9, [[(0, 0.1), (0.9, 0.5), (0, 0.9)]]),
    "_": (1, [[(0, 1), (1, 1)]]),
}
W, H, GAP, PAD, STROKE = 2.4, 5, 1.8, 1.35, 1.1   # tag text, in px of the 16 × 16 icon, stroke centre to centre
TAG_X, TAG_Y, TAG_H = 0.5, 7, 8.5


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">{body}</svg>\n'


def n(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def sheet(lines=False):
    s = (f'<path d="M3.5 1.5H10L13.5 5V14.5H3.5Z" fill="{GRAY}" fill-opacity=".15" stroke="{GRAY}" stroke-linejoin="round"/>'
         f'<path d="M10 1.5V5H13.5" fill="none" stroke="{GRAY}" stroke-linejoin="round"/>')
    if lines:
        s += f'<path d="M5.5 7.5H11.5M5.5 9.5H11.5M5.5 11.5H9.5" stroke="{GRAY}" stroke-linecap="round"/>'
    return s


def tag(text, color, ink):
    width = PAD * 2 + sum(GLYPHS[c][0] * W for c in text) + GAP * (len(text) - 1)
    paths, x, y = [], TAG_X + PAD, TAG_Y + (TAG_H - H) / 2
    for c in text:
        w, lines = GLYPHS[c]
        for line in lines:
            paths.append("M" + "L".join(f"{n(x + px * W)} {n(y + py * H)}" for px, py in line))
        x += w * W + GAP
    return (f'<rect x="{TAG_X}" y="{TAG_Y}" width="{n(width)}" height="{TAG_H}" rx="1.5" fill="{color}"/>'
            f'<path d="{"".join(paths)}" fill="none" stroke="{ink}" stroke-width="{STROKE}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def shade(color, k=0.7):
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{int(v * k):02x}" for v in (r, g, b))


def folder(color, open_):
    back = f'<path d="M1.5 3.5Q1.5 2.5 2.5 2.5H6L7.5 4H13.5Q14.5 4 14.5 5V12.5Q14.5 13.5 13.5 13.5H2.5Q1.5 13.5 1.5 12.5Z" fill="{shade(color)}"/>'
    if open_:
        return back + f'<path d="M1.5 13.5L3.4 7.6Q3.6 7 4.2 7H14.8Q15.6 7 15.4 7.7L13.8 13Q13.6 13.5 13 13.5Z" fill="{color}"/>'
    return back + f'<rect x="1.5" y="5.5" width="13" height="8" rx="1" fill="{color}"/>'


def main():
    out = os.path.join(HERE, "icons")
    os.makedirs(out, exist_ok=True)
    icons = {"file": svg(sheet(lines=True))}
    theme = {"file": "file", "folder": "folder", "folderExpanded": "folder-open",
             "fileExtensions": {}, "fileNames": {}, "folderNames": {}, "folderNamesExpanded": {}}
    for icon, (text, color, names) in TAGS.items():
        icons[icon] = svg(sheet() + tag(text, color, DARK if icon in PALE else "#fff"))
        for name in names:
            theme["fileNames" if "." in name or name != name.lower() else "fileExtensions"][name.lower()] = icon
    for icon, (color, names) in FOLDERS.items():
        icons[icon] = svg(folder(color, False))
        icons[icon + "-open"] = svg(folder(color, True))
        for name in names:
            theme["folderNames"][name] = icon
            theme["folderNamesExpanded"][name] = icon + "-open"
    for old in os.listdir(out):
        os.remove(os.path.join(out, old))
    for icon, text in icons.items():
        with open(os.path.join(out, icon + ".svg"), "w", encoding="utf-8") as f:
            f.write(text)
    theme = {"iconDefinitions": {i: {"iconPath": f"./icons/{i}.svg"} for i in icons}} | theme
    with open(os.path.join(HERE, "theme.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(theme, indent=2) + "\n")
    print(f"{len(icons)} icons")


if __name__ == "__main__":
    main()
