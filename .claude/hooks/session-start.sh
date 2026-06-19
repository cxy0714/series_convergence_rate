#!/bin/bash
# SessionStart hook: provision the toolchain needed to build the paper and
# regenerate the figures (Python scientific stack + a LaTeX distribution).
#
# Synchronous, idempotent, web-only. Safe to run repeatedly: it skips anything
# already present, so on a warm container it returns almost immediately.
set -euo pipefail

# Only provision in the remote (Claude Code on the web) environment.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "[session-start] provisioning LaTeX + Python toolchain..."

# --- Python scientific stack ------------------------------------------------
if ! python3 -c "import numpy, scipy, matplotlib" >/dev/null 2>&1; then
  echo "[session-start] installing numpy/scipy/matplotlib..."
  python3 -m pip install --quiet numpy scipy matplotlib
else
  echo "[session-start] python deps already present."
fi

# --- LaTeX toolchain --------------------------------------------------------
if ! command -v pdflatex >/dev/null 2>&1 || ! command -v latexmk >/dev/null 2>&1; then
  echo "[session-start] installing TeX Live (this is the slow step)..."
  export DEBIAN_FRONTEND=noninteractive
  apt-get install -y --no-install-recommends \
      texlive-latex-base \
      texlive-latex-extra \
      texlive-pictures \
      texlive-science \
      texlive-fonts-recommended \
      latexmk >/dev/null
else
  echo "[session-start] LaTeX already present."
fi

echo "[session-start] done."
