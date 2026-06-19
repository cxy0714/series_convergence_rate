"""Experiment 5 -- the structural diagnostic behind the easy/hard classification.

The whole "treewidth classifies the convergence rate" story rests on one fact:

    a FINITE transfer matrix (bounded carrier) forces a PURE geometric correction
        Z_L = c * lambda^L * (1 + O(delta^L)),     Z_L / lambda^L -> c > 0,
    so it can NEVER produce a genuine power-law factor L^theta.

Hence the *shape* of the correction to lambda^L reads off the structural class.
We contrast the two extremes with elementary, exactly-known sequences:

  * golden-mean shift  Z_L = F_{L+2}  (no two adjacent 1s):
        LOCAL constraint -> finite carrier (2 states) -> Z_L/phi^L -> const,
        ratio error |Z_{L+1}/Z_L - phi| decays GEOMETRICALLY (rate phi^-2).

  * central binomial   Z_L = C(2L,L)  (#(+1)=#(-1), Dyck-type):
        GLOBAL constraint (sum = 0) -> the carrier must track an unbounded
        height -> NO finite transfer matrix -> Z_L/4^L ~ 1/sqrt(pi L)  (a power
        law!), and the ratio error |Z_{L+1}/Z_L - 4| = 2/(L+1) decays only
        ALGEBRAICALLY (~ 1/L).

Same template (a rate from a sum over constrained words); the only difference is
local vs global coupling, i.e. bounded vs growing carrier -- and it is legible in
the asymptotics.
"""
import numpy as np
from math import comb
from common import savefig, banner, C, plt

PHI = (1 + np.sqrt(5)) / 2


def fib_seq(n):
    """F_1..F_n as Python big ints."""
    F = [0, 1]
    while len(F) < n + 1:
        F.append(F[-1] + F[-2])
    return F


def main():
    banner("Experiment 5: structural diagnostic -- geometric vs power-law correction")

    Lmax = 120
    L = np.arange(1, Lmax + 1)

    # --- golden mean: Z_L = F_{L+2}, lambda = phi (finite carrier) ---
    F = fib_seq(Lmax + 3)
    Zg = [F[i + 2] for i in range(1, Lmax + 1)]          # F_{L+2}, big ints
    norm_g = np.array([float(Zg[i] / PHI ** int(L[i])) for i in range(Lmax)])
    ratio_g = np.array([float(Zg[i + 1] / Zg[i]) for i in range(Lmax - 1)])
    errg = np.abs(ratio_g - PHI)

    # --- central binomial: Z_L = C(2L,L), lambda = 4 (unbounded carrier) ---
    Zb = [comb(2 * l, l) for l in range(1, Lmax + 1)]    # big ints
    norm_b = np.array([float(Zb[i] / 4 ** int(L[i])) for i in range(Lmax)])
    ratio_b = np.array([float(Zb[i + 1] / Zb[i]) for i in range(Lmax - 1)])
    errb = np.abs(ratio_b - 4.0)

    print(f"  golden mean (finite carrier):  Z_L/phi^L at L=20,60,120 = "
          f"{norm_g[19]:.6f}, {norm_g[59]:.6f}, {norm_g[119]:.6f}   (-> const)")
    print(f"  central binom (no carrier):    Z_L/4^L  at L=20,60,120 = "
          f"{norm_b[19]:.6f}, {norm_b[59]:.6f}, {norm_b[119]:.6f}   (~1/sqrt(pi L))")
    print(f"     check 1/sqrt(pi L)         at L=20,60,120 = "
          f"{1/np.sqrt(np.pi*20):.6f}, {1/np.sqrt(np.pi*60):.6f}, {1/np.sqrt(np.pi*120):.6f}")
    print(f"  ratio error |r_L - lambda| at L=20: golden {errg[19]:.2e} (geometric),  "
          f"binom {errb[19]:.2e} (= 2/(L+1) = {2/21:.2e})")

    fig, ax = plt.subplots(1, 2, figsize=(9.4, 3.6))

    # (a) the correction to lambda^L:  flat (finite) vs power law (infinite)
    ax[0].loglog(L, norm_g, "o-", color=C[2], ms=3,
                 label=r"golden mean $Z_L/\varphi^L\to$ const (finite carrier)")
    ax[0].loglog(L, norm_b, "s-", color=C[1], ms=3,
                 label=r"central binomial $Z_L/4^L\sim(\pi L)^{-1/2}$")
    ax[0].loglog(L, 1 / np.sqrt(np.pi * L), "--", color="0.4", lw=1,
                 label=r"slope $-1/2$ (power law)")
    ax[0].set_xlabel(r"word length $L$")
    ax[0].set_ylabel(r"$Z_L/\lambda^L$")
    ax[0].set_title(r"(a) correction to $\lambda^L$: flat $=$ gap, slope $=$ power law")
    ax[0].legend(loc="lower left", fontsize=7.5)

    # (b) how fast the naive ratio settles: geometric vs algebraic
    Lr = L[:-1]
    sel_g = errg > 1e-15
    ax[1].semilogy(Lr[sel_g], errg[sel_g], "o-", color=C[2], ms=3,
                   label=r"golden mean: $\sim\varphi^{-2L}$ (geometric $=$ gap)")
    ax[1].semilogy(Lr, errb, "s-", color=C[1], ms=3,
                   label=r"central binomial: $=2/(L{+}1)$ (algebraic, no gap)")
    ax[1].set_xlabel(r"word length $L$")
    ax[1].set_ylabel(r"ratio error $|Z_{L+1}/Z_L-\lambda|$")
    ax[1].set_title(r"(b) ratio settles geometrically (gap) vs $\sim 1/L$ (no gap)")
    ax[1].legend(loc="lower left", fontsize=7.5)

    fig.tight_layout()
    savefig(fig, "classification.pdf")


if __name__ == "__main__":
    main()
