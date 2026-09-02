#!/bin/sh
set -eu

script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd -P)
node_path=$(command -v node || true)

if [ -z "$node_path" ]; then
  printf '%s\n' 'Agent Usage requires Node.js.' >&2
  exit 127
fi
if [ -z "${HOME:-}" ]; then
  printf '%s\n' 'Agent Usage requires HOME to be set.' >&2
  exit 1
fi

node_dir=$(dirname -- "$node_path")
safe_path=$node_dir:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin

exec /usr/bin/env -i \
  HOME="$HOME" \
  PATH="$safe_path" \
  TERM="${TERM:-xterm-256color}" \
  TMPDIR="${TMPDIR:-/tmp}" \
  CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-}" \
  XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-}" \
  "$node_path" \
  --require "$script_dir/deny-network.cjs" \
  "$script_dir/../node_modules/ccusage/dist/index.js" "$@"
