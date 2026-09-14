#!/usr/bin/env bash
set -euo pipefail

NODE_VERSION=22.22.0
RIPGREP_VERSION=15.1.0
TOOLS_DIR="${HOME}/.local/praxis-tools"
BIN_DIR="${HOME}/.local/bin"

mkdir -p "${TOOLS_DIR}" "${BIN_DIR}"

python3 -m ensurepip --user >/dev/null 2>&1 || true
python3 -m pip install --user -e '.[dev]'

if ! command -v node >/dev/null 2>&1; then
  curl --fail --location --silent --show-error \
    "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz" \
    --output /tmp/praxis-node.tar.gz
  tar -xzf /tmp/praxis-node.tar.gz -C "${TOOLS_DIR}"
  ln -sfn "${TOOLS_DIR}/node-v${NODE_VERSION}-linux-x64/bin/node" "${BIN_DIR}/node"
  ln -sfn "${TOOLS_DIR}/node-v${NODE_VERSION}-linux-x64/bin/npm" "${BIN_DIR}/npm"
  ln -sfn "${TOOLS_DIR}/node-v${NODE_VERSION}-linux-x64/bin/npx" "${BIN_DIR}/npx"
fi

if ! command -v rg >/dev/null 2>&1; then
  curl --fail --location --silent --show-error \
    "https://github.com/BurntSushi/ripgrep/releases/download/${RIPGREP_VERSION}/ripgrep-${RIPGREP_VERSION}-x86_64-unknown-linux-musl.tar.gz" \
    --output /tmp/praxis-ripgrep.tar.gz
  tar -xzf /tmp/praxis-ripgrep.tar.gz -C "${TOOLS_DIR}"
  ln -sfn "${TOOLS_DIR}/ripgrep-${RIPGREP_VERSION}-x86_64-unknown-linux-musl/rg" "${BIN_DIR}/rg"
fi

export PATH="${BIN_DIR}:${PATH}"
python3 --version
java -version
node --version
npm --version
rg --version | head -1
