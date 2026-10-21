# Reprise

Calls recorded with [Reprise](https://github.com/nikiomori/reprise), the open-source call recorder for macOS:
read the transcript, play the call, have an agent sum it up.

Needs `jq`, which macOS 15 and later have in /usr/bin.

Adds a **Calls** panel to the right inspector: the last 100 calls, newest first, with when, how long and in which app;
"transcript" when Reprise has transcribed it (Settings › Transcription in Reprise). Refreshed every 30 s.
Double-click a call to **Open Transcript**; its context menu also has Sum It Up With Agent (decisions, action items,
open questions, and what concerns the project you have open), Play, Copy Transcript, Show in Finder.
Toolbar: Open Reprise.

Settings › Extensions › Reprise › **Calls folder**: set it if you moved Reprise's library (Reprise › Settings › General ›
Saved in). Empty: Movies › Reprise.
