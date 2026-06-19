# Einsum, treewidth, and the convergence rates of multiplicative series

An exploration companion to *"On computing and the complexity of computing
higher-order U-statistics, exactly"* (Chen, Zhang, Liu). It asks how far the
einsum / treewidth machinery of that paper carries into the numerical study of
**series convergence rates** — pressures, free energies, growth rates, critical
exponents — and catalogues where it does and does not apply.

## The idea in one paragraph

A huge family of problems asks for the exponential growth rate of a partition
function `Z_L = sum_{words I of length L} w(I)` with a (sub)multiplicative
weight `w`. A `V`-statistic is exactly an `einsum`, and its exact cost is
`Theta(n^{tw+1})` (companion paper). The same calculus governs the
transfer-matrix engines that compute `Z_L`: the practitioner's "decomposable
vs. entangled" feeling is precisely *bounded vs. growing treewidth* of the
weight's dependency graph. In the decomposable regime the "divide out the
conjectured rate and check the ratio → 1" heuristic is rigorous and the spectral
gap is read off from the speed of convergence; in the entangled regime it is the
standard (heuristic) ratio method, whose cost the treewidth bound quantifies.

## Layout

```
main.tex            # the paper (build target)
references.bib      # bibliography
Makefile            # `make all` = figures + paper
code/               # numerical experiments (reproduce the figures + constants)
  common.py             shared plotting helpers
  exp1_golden_mean.py   golden-mean shift: ratio -> phi, error decay = spectral gap
  exp2_hard_squares.py  hard squares on a strip: treewidth = strip width = cost dial
  exp3_continued_fraction.py   dim_H(E_2) via the transfer operator + ratio test
  exp4_matrix_products.py      affinity dimension: entangled case and its collapse
  run_all.py            run everything
figures/            # generated PDF figures embedded by main.tex
```

## Build

```bash
make all        # regenerate figures, then compile main.pdf
# or, separately:
cd code && python3 run_all.py     # -> figures/*.pdf  (prints each reproduced constant)
latexmk -pdf main.tex             # -> main.pdf
```

### Toolchain

- **Python**: `numpy`, `scipy`, `matplotlib`.
- **LaTeX**: a TeX Live install with `latexmk` (packages: amsmath, tikz,
  natbib, cleveref, booktabs, hyperref, pgfplots).

A ready-made, idempotent provisioning script lives at
`.claude/hooks/session-start.sh` (it installs both stacks and is safe to re-run).
Run it directly, or set it up by hand:

```bash
# one-shot provisioning (same as the script does):
pip install numpy scipy matplotlib
apt-get install -y --no-install-recommends \
    texlive-latex-base texlive-latex-extra texlive-pictures texlive-science latexmk
```

To make a fresh **Claude-Code-on-the-web** container provision itself
automatically at session start, add this to `.claude/settings.json` (you must
add it yourself — the agent is intentionally not allowed to register its own
hooks):

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh" } ] }
    ]
  }
}
```

## Reproduced constants (self-checks)

Each experiment prints the known constant it reproduces:

| experiment | reproduces | value |
|---|---|---|
| golden-mean shift | golden ratio, spectral gap | `phi = 1.6180339887`, gap `= phi^-2` |
| hard squares | hard-square entropy constant | `kappa = 1.5030480824753` |
| continued fractions | `dim_H(E_2)` (Jenkinson–Pollicott) | `0.5312805062772` (15 digits) |
| matrix products | `log rho(T1+T2)`, affinity dim | trace surrogate matches to 12 digits |
