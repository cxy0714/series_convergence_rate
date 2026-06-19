"""Experiment 2 -- treewidth = strip width.

Hard squares (2-D hard-core lattice gas): place 0/1 on a W x L grid so that no
two 1s are horizontally or vertically adjacent.  On a strip of width W the count
Z_{W,L} is computed by a transfer matrix M_W indexed by the admissible *column
states* = independent sets of the path P_W.  Its dimension is

      dim M_W = (# independent sets of P_W) = F_{W+2}  ~  phi^W,

which is exactly the cost predicted by the einsum/treewidth calculus: the
decomposition graph of the strip has treewidth W, so evaluating Z_{W,L} costs
Theta(q^{W+1} L) with q = 2.  The per-site growth rate

      lambda_1(M_W)^{1/W}  ->  kappa = 1.5030480824753...   (hard-square constant)

as W grows: wider strips give a better estimate of kappa but at exponentially
larger cost -- the treewidth IS the accuracy/cost dial.
"""
import numpy as np
from common import savefig, banner, C, plt

PHI = (1 + np.sqrt(5)) / 2
KAPPA = 1.5030480824753322   # hard-square entropy constant (Baxter); reference value


def column_states(W):
    """All independent sets of the path P_W, as bitmasks (no two adjacent bits)."""
    return [s for s in range(1 << W) if (s & (s << 1)) == 0]


def transfer_matrix(W):
    states = column_states(W)
    idx = {s: i for i, s in enumerate(states)}
    d = len(states)
    M = np.zeros((d, d))
    for s in states:
        for t in states:
            if (s & t) == 0:          # no horizontal adjacency between columns
                M[idx[s], idx[t]] = 1.0
    return M, d


def main():
    banner("Experiment 2: hard squares on a strip (treewidth = strip width)")
    print(f"  reference hard-square constant kappa = {KAPPA:.13f}")
    Ws = list(range(1, 17))
    rows = []
    lam_prev = None
    for W in Ws:
        M, d = transfer_matrix(W)
        lam = np.max(np.abs(np.linalg.eigvals(M))).real
        per_site = lam ** (1.0 / W)
        incr = (lam / lam_prev) if lam_prev is not None else np.nan  # ratio estimator
        fib = round(PHI ** (W + 2) / np.sqrt(5))   # F_{W+2}
        rows.append((W, d, fib, lam, per_site, incr))
        print(f"  W={W:2d}  dim(M_W)={d:5d} (=F_{{W+2}}={fib:5d})  "
              f"lambda_1={lam:12.6f}  l^(1/W)={per_site:.9f} (err {abs(per_site-KAPPA):.1e})  "
              f"l_W/l_(W-1)={incr:.9f}" +
              ("" if W == 1 else f" (err {abs(incr-KAPPA):.1e})"))
        lam_prev = lam

    Wn = np.array([r[0] for r in rows])
    dim = np.array([r[1] for r in rows])
    ps = np.array([r[4] for r in rows])
    incr = np.array([r[5] for r in rows])

    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.5))

    ax[0].axhline(KAPPA, color="0.5", ls="--", lw=1,
                  label=r"$\kappa=1.50304808\ldots$")
    ax[0].plot(Wn, ps, "o-", color=C[2], ms=4,
               label=r"per-site $\lambda_1(M_W)^{1/W}$")
    ax[0].plot(Wn[1:], incr[1:], "s-", color=C[4], ms=4,
               label=r"ratio $\lambda_1(M_W)/\lambda_1(M_{W-1})$")
    ax[0].set_xlabel(r"strip width $W$ ($=$ treewidth)")
    ax[0].set_ylabel(r"estimate of $\kappa$")
    ax[0].set_title(r"(a) two estimators $\to$ hard-square constant")
    ax[0].legend(loc="upper right")

    ax[1].semilogy(Wn, dim, "s-", color=C[3], ms=4,
                   label=r"$\dim M_W=F_{W+2}\sim\varphi^{\,W}$")
    ax[1].set_xlabel(r"strip width $W$ ($=$ treewidth)")
    ax[1].set_ylabel(r"transfer-matrix dimension")
    ax[1].set_title(r"(b) cost $=\Theta(q^{\mathrm{tw}+1}L)$ grows with width")
    ax[1].legend(loc="upper left")

    fig.tight_layout()
    savefig(fig, "exp2_hard_squares.pdf")


if __name__ == "__main__":
    main()
