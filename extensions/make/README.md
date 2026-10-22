# Make

Makefile targets of the workspace — run them, dry-run them, or hand a failing one to an agent.

Needs `make` — Kelp keeps it off until that's installed.

Adds a **Make** panel to the right inspector with the targets of the workspace's Makefile (and the files it
`include`s), refreshed every 10 s. A `## comment` after a target (`test: build ## Run the tests`) shows as its subtitle.
Double-click a row for **Run** (`make <target>` in a terminal tab); its context menu also has Dry Run, Ask Agent to Fix.
Toolbar: Make (default target), Open Makefile.

In the command palette (⇧⌘P) and Run menu: Make: Run Default Target.

Targets are read with `make -pq`, which evaluates the Makefile: its `$(shell …)` calls run, its recipes don't.
