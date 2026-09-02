#!/bin/sh
set -eu

script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd -P)
node_path=$(command -v node || true)
npm_path=$(command -v npm || true)

if [ -z "$node_path" ] || [ -z "$npm_path" ]; then
  printf '%s\n' 'Agent Usage requires Node.js and npm.' >&2
  exit 127
fi
if [ -z "${HOME:-}" ]; then
  printf '%s\n' 'Agent Usage requires HOME to be set.' >&2
  exit 1
fi

node_dir=$(dirname -- "$node_path")
npm_dir=$(dirname -- "$npm_path")
safe_path=$node_dir:$npm_dir:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin

exec /usr/bin/env -i \
  HOME="$HOME" \
  PATH="$safe_path" \
  NPM_CONFIG_USERCONFIG="$script_dir/../.npmrc" \
  NPM_CONFIG_GLOBALCONFIG=/dev/null \
  "$npm_path" ci --ignore-scripts --no-audit --no-fund --omit=dev
