# Agent Usage — cmux Dock extension

Live Claude Code token usage and cost dashboard, running as a TUI pane in the
[cmux](https://github.com/manaflow-ai/cmux) Dock. It uses a checked-in
[ccusage](https://github.com/ryoppippi/ccusage) dependency.

## Install

```
cmux extension install manaflow-ai/cmux-agent-usage
```

or Settings → Extensions → Install from GitHub, or the Extensions menu at the
bottom of the Dock. cmux shows the build and pane commands before they run and
asks again if those commands change.

The first install downloads the pinned package from npm. The build uses
`npm ci` with the checked-in lockfile and integrity hash, and disables package
install scripts, audits, and funding requests. The panes execute the installed
package locally. They pass `--offline`, and the launcher blocks outbound
`fetch` calls, so ccusage reads local Claude Code JSONL logs and its embedded
pricing data without sending usage data or fetching pricing at runtime.
The live pane may show a pricing fallback warning. The pinned ccusage live
path probes its pricing source before falling back; the launcher rejects that
probe locally.

## Panes

- **Live usage** — `./scripts/run-ccusage.sh blocks --live --offline` (live 5-hour block dashboard)
- **Daily report** — `./scripts/run-ccusage.sh daily --offline` (prints the report, then drops to a shell)

Requires Node.js 20.19.4 or newer and npm. Dependency updates must change
`package.json`, `package-lock.json`, and the reviewed integrity hash together.
The `17.2.1` pin is intentional: it is the newest ccusage release that still
supports the live `blocks --live` command. Newer releases removed that option
and need a separate pane design.

## Publishing your own

Any public GitHub repo with a `cmux-extension.json` manifest and the
`cmux-extension` topic appears in the cmux marketplace automatically.
