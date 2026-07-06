# Agent Usage — cmux Dock extension

Live coding-agent token usage and cost dashboard, running as a TUI pane in the
[cmux](https://github.com/manaflow-ai/cmux) Dock. Wraps
[ccusage](https://github.com/ryoppippi/ccusage), which reads your local Claude
Code usage logs — nothing leaves your machine.

## Install

```
cmux extension install manaflow-ai/cmux-agent-usage
```

or Settings → Extensions → Install from GitHub, or the Extensions menu at the
bottom of the Dock. cmux shows you the exact commands below before anything
runs, pins the install to a commit, and asks again if they ever change.

## Panes

- **Live usage** — `npx --yes ccusage@latest blocks --live` (live 5-hour block dashboard)
- **Daily report** — `npx --yes ccusage@latest daily` (prints the report, then drops to a shell)

Requires Node.js (for `npx`).

## Publishing your own

Any public GitHub repo with a `cmux-extension.json` manifest and the
`cmux-extension` topic appears in the cmux marketplace automatically.
