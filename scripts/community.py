#!/usr/bin/env python3
"""Writes community.json: extensions on GitHub under the topic kelp-extension, which nobody here reviewed.

    GH_TOKEN=… python3 scripts/community.py

Each entry is pinned to the commit seen (Kelp shows what it runs before installing it, and marks the list as not
reviewed), with its stars and the stars it gained in the last seven days, which the list is sorted by. Repositories
already in index.json are left out. Uses the gh CLI; standard library otherwise.
"""
import base64
import datetime
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def gh(*args, accept=None):
    cmd = ["gh", "api", *args] + (["-H", f"Accept: {accept}"] if accept else [])
    return json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)


def weekly(repo, stars):
    """Stars given in the last seven days, read from the newest page of stargazers."""
    if not stars:
        return 0
    since = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)
    last = (stars - 1) // 100 + 1
    count = 0
    for page in (last, last - 1):
        if page < 1:
            break
        for s in gh(f"repos/{repo}/stargazers?per_page=100&page={page}", accept="application/vnd.github.star+json"):
            if datetime.datetime.fromisoformat(s["starred_at"].replace("Z", "+00:00")) >= since:
                count += 1
    return count


def main():
    with open(os.path.join(ROOT, "index.json"), encoding="utf-8") as f:
        reviewed = {e["id"] for e in json.load(f)}
    found = gh("search/repositories?q=topic:kelp-extension&per_page=100")["items"]
    out = []
    for r in found:
        repo = r["full_name"]
        if repo == os.environ.get("GITHUB_REPOSITORY", "nikiomori/kelp-extensions"):
            continue
        try:
            head = gh(f"repos/{repo}/commits/{r['default_branch']}")["sha"]
            m = json.loads(base64.b64decode(gh(f"repos/{repo}/contents/extension.json?ref={head}")["content"]))
        except (subprocess.CalledProcessError, KeyError, ValueError):
            continue  # not an extension at its top folder
        if not isinstance(m, dict) or m.get("id") in reviewed or not m.get("id") or not m.get("name"):
            continue
        out.append({k: m[k] for k in ("id", "name", "version", "description", "icon", "requires") if k in m}
                   | {"version": m.get("version", "0.0.0"), "source": f"https://github.com/{repo}/tree/{head}",
                      "reviewed": False, "stars": r["stargazers_count"], "weekly": weekly(repo, r["stargazers_count"])})
    out.sort(key=lambda e: (-e["weekly"], -e["stars"], e["id"]))
    with open(os.path.join(ROOT, "community.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"community.json: {len(out)} extensions")


if __name__ == "__main__":
    main()
