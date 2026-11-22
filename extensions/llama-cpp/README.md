# llama.cpp

llama-server: the servers running on this Mac and the GGUF models downloaded for them; start a server, open its
page, start Claude Code on it.

Adds a **llama.cpp** panel to the right inspector, refreshed every 5 s: the running `llama-server`s (port, context,
"Answering" while one works), then the GGUF files in the Hugging Face cache (`~/.cache/huggingface/hub`, where
`llama-server -hf` downloads), with their size. Servers Ollama and Kelp run for themselves aren't counted on the
panel's icon; Kelp's own next-edit server can't be stopped from here.

Double-click a server to open its page in a browser tab, a file to start a server on it in a terminal tab (`--jinja
-c 32768`, the first free port from 8080; close the tab to stop it). The context menu also has Start Claude Code
(on a server, through its Anthropic API; needs a Kelp with the `session` action), Stop Server…, Show in Finder, Move
to Trash….
Toolbar: Download Model… (asks `user/repo:quant`, then downloads it and starts a server), and a search of GGUF models
on Hugging Face.

Settings › Extensions › llama.cpp › llama-server: its name on PATH (`brew install llama.cpp`), or its full path if
you built llama.cpp yourself.
