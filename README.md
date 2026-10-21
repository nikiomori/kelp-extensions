# Kelp extensions

Extensions for Kelp, the native macOS IDE for coding agents, shared by the people who use it. Each one is a folder in
[`extensions/`](extensions) and is reviewed before it is merged; Kelp installs exactly the commit that was reviewed.

## Install one

- **In Kelp:** Settings › Extensions › Library › Install.
- **From a terminal or an agent:** `kelp ext search` lists them, `kelp ext install docker` installs one,
  `kelp ext update` brings them up to date.

Before installing, Kelp shows which commands the extension can run on your Mac.

## Add yours

An extension is a folder with an `extension.json` — no build step. Kelp's extension guide describes the format:
it is at `~/.kelp/extensions/EXTENSIONS.md` on your Mac, `kelp ext new <id>` makes a working starter, and an agent in
Kelp (Claude Code) writes one when you ask for it.

1. Fork this repo and add `extensions/<id>/`:
   - `extension.json` — its `id` is the folder's name; `name`, `version` (`1.0.0`) and `description` are required.
     List the commands it needs in `requires` (e.g. `["docker"]`).
   - `README.md` — what it adds and what it needs.
   - Any HTML or scripts it uses. No binaries, symlinks or files over 1 MB.
2. Try it: `kelp ext install ./extensions/<id>`.
3. Open a pull request. A check runs `python3 scripts/index.py --check`; run it yourself first.

To change an extension, bump its `version` in the same pull request.

With the GitHub CLI, from the folder of an extension you made:

```sh
id=my-thing
gh repo fork nikiomori/kelp-extensions --clone && cd kelp-extensions
git switch -c "$id" && cp -R ~/.kelp/extensions/$id extensions/ && rm -f extensions/$id/.kelp-source.json
python3 scripts/index.py --check && git add extensions/$id && git commit -m "Add $id" && gh pr create --fill
```

## How it works

On every merge to `main`, [a workflow](.github/workflows/index.yml) checks the extensions and writes
[`index.json`](index.json): each extension's name, version and folder at the commit that last changed it. Kelp reads
that file and downloads that folder from GitHub. A Kelp extension from anywhere else on GitHub installs the same way
(`kelp ext install https://github.com/you/repo/tree/main/folder`), without the review.

## Reviewing

Extensions run commands on the user's Mac, so read every command in a pull request: list commands, actions, toolbar
buttons, and the `kelp.exec` calls of web pages. They should do what the README says and nothing else.

## License

[MIT](LICENSE). By contributing you agree your extension is shared under it.
