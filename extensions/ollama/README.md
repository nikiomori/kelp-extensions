# Ollama

Models in Ollama: what is on disk and in memory; start Claude Code or Codex on one, chat, unload, pull, remove.

Needs `ollama` — Kelp keeps it off until that's installed. If Ollama isn't running, the panel starts it, as the
`ollama` command does. Starting an agent on a model needs a Kelp with the `session` action.

Adds an **Ollama** panel to the right inspector, refreshed every 5 s. Models in memory come first, with a mark and
how much memory they hold; each line says the model's size and what it can do (tools, vision, thinking, fill-in).
The model Kelp's code suggestions use says so. The panel's icon counts the models in memory.

Double-click a model that can call tools to start **Claude Code** on it (Ollama's Anthropic API at
127.0.0.1:11434), any other to chat with it in a terminal. Its context menu also has Start Codex, Chat in Terminal,
Unload from Memory (while it's in memory), Show Details, Remove….
Toolbar: Pull Model… (asks the name in a terminal tab), and a search of ollama.com.
