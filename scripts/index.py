#!/usr/bin/env python3
"""Checks every extension in extensions/ and writes index.json, the list Kelp's library shows.

    python3 scripts/index.py                         check, then write index.json (commit it with the extension)
    python3 scripts/index.py --check [--base REF]    check only, index.json included; with --base, an extension
                                                     changed since REF must have a new version (what pull requests run)
    python3 scripts/index.py --tag                   check, then tag each extension <id>-<version> (what main runs)

Each index entry points at the tag <id>-<version>: the last commit that changed the extension's folder, so Kelp
installs exactly what was reviewed. The index can then go in the same commit as the extension. Standard library only.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.environ.get("GITHUB_REPOSITORY", "nikiomori/kelp-extensions")
ID = re.compile(r"[a-z0-9][a-z0-9.-]*")
VERSION = re.compile(r"\d+\.\d+\.\d+")
CONTRIBUTES = {"panels", "editors", "commands", "settings", "themes", "iconThemes", "agents", "languages"}
MAX_FILE = 1_000_000


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def problems(folder, m):
    """What's wrong with extensions/<folder>, whose extension.json is `m`."""
    out = []
    if m.get("id") != folder or not ID.fullmatch(folder):
        out.append(f'"id" must be the folder\'s name, "{folder}" (lowercase letters, digits, dots and dashes)')
    for key in ("name", "description"):
        if not isinstance(m.get(key), str) or not m[key].strip():
            out.append(f'"{key}" is missing')
    if not isinstance(m.get("version"), str) or not VERSION.fullmatch(m["version"]):
        out.append('"version" must look like 1.0.0')
    if "icon" in m and not isinstance(m["icon"], str):
        out.append('"icon" is an SF Symbol name')
    if "requires" in m and not (isinstance(m["requires"], list) and all(isinstance(r, str) for r in m["requires"])):
        out.append('"requires" is a list of commands')
    c = m.get("contributes")
    if not isinstance(c, dict) or not c:
        out.append('"contributes" adds nothing')
    else:
        out += [f'unknown contribution "{k}"' for k in sorted(set(c) - CONTRIBUTES)]
        for view in (c.get("panels") or []) + (c.get("editors") or []):
            page = isinstance(view, dict) and view.get("web")
            if page and not os.path.isfile(os.path.join(ROOT, "extensions", folder, page)):
                out.append(f"web page {page} isn't in the folder")
    if not os.path.isfile(os.path.join(ROOT, "extensions", folder, "README.md")):
        out.append("README.md is missing")
    for dirpath, dirs, files in os.walk(os.path.join(ROOT, "extensions", folder)):
        for name in dirs + files:
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, os.path.join(ROOT, "extensions", folder))
            if os.path.islink(path):
                out.append(f"{rel} is a symlink")
            elif name.startswith("."):
                out.append(f"{rel} is hidden")
            elif os.path.isfile(path) and os.path.getsize(path) > MAX_FILE:
                out.append(f"{rel} is over 1 MB")
    return out


def version_problems(base, folder, m):
    """An extension changed since `base` needs a version it didn't have there."""
    if not git("diff", "--name-only", f"{base}...HEAD", "--", f"extensions/{folder}"):
        return []
    try:
        before = json.loads(git("show", f"{base}:extensions/{folder}/extension.json"))
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return []  # new here
    return [f'changed, so "version" must change too (it is {m.get("version")})'] if before.get("version") == m.get("version") else []


def tag(folder, version):
    """Tags the last commit that changed extensions/<folder> as <folder>-<version>, unless that tag holds it already."""
    name, path = f"{folder}-{version}", f"extensions/{folder}"
    if subprocess.run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{name}"], cwd=ROOT, capture_output=True).returncode == 0:
        if git("diff", "--name-only", name, "HEAD", "--", path):
            sys.exit(f'{path}: changed since the tag {name}, so "version" must change too')
        return
    commit = git("log", "-1", "--format=%H", "--", path)
    if not commit:
        sys.exit(f"{path}: commit it first (the index points at its tag)")
    git("tag", name, commit)
    print(f"tagged {name}")


def main():
    args = sys.argv[1:]
    base = args[args.index("--base") + 1] if "--base" in args else None
    entries, failed = [], False
    for folder in sorted(os.listdir(os.path.join(ROOT, "extensions"))):
        if not os.path.isdir(os.path.join(ROOT, "extensions", folder)):
            continue
        try:
            with open(os.path.join(ROOT, "extensions", folder, "extension.json"), encoding="utf-8") as f:
                m = json.load(f)
            found = problems(folder, m) if isinstance(m, dict) else ["extension.json isn't an object"]
        except (OSError, json.JSONDecodeError) as e:
            m, found = {}, [f"extension.json: {e}"]
        if base and not found:
            found = version_problems(base, folder, m)
        for p in found:
            print(f"extensions/{folder}: {p}")
        failed = failed or bool(found)
        if not found:
            entries.append({k: m[k] for k in ("id", "name", "version", "description", "icon", "requires") if k in m}
                           | {"source": f"https://github.com/{REPO}/tree/{folder}-{m['version']}/extensions/{folder}"})
    if failed:
        sys.exit(1)
    index = json.dumps(entries, indent=2, ensure_ascii=False) + "\n"
    path = os.path.join(ROOT, "index.json")
    if "--check" in args or "--tag" in args:
        with open(path, encoding="utf-8") as f:
            if f.read() != index:
                sys.exit("index.json is out of date: run python3 scripts/index.py and commit it")
        if "--tag" in args:
            for e in entries:
                tag(e["id"], e["version"])
        print("all extensions are fine")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(index)
    print(f"index.json: {len(entries)} extensions")


if __name__ == "__main__":
    main()
