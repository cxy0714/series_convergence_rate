"""Experiment 1 -- the decomposable, treewidth-1 prototype.

Golden-mean shift / 1-D hard-core gas: Z_L = number of binary words of length
L with no two adjacent 1s.  This is the cleanest instance of

      Z_L = <u, T^L v>,    P = log lambda_1(T),

where T = [[1,1],[1,0]] is the 2x2 transfer matrix.  We verify, by direct
enumeration via the transfer matrix, that
   (i)  Z_{L+1}/Z_L -> phi              (the conjectured rate);
   (ii) the *speed* of that convergence equals the spectral gap |lambda_2/lambda_1|
        = phi^{-2}, i.e. dividing out the rate exposes the gap.
"""
import numpy as np
from common import savefig, banner, C, plt

PHI = (1 + np.sqrt(5)) / 2          # 1.6180339887...
GAP = 1 / PHI**2                    # |lambda_2/lambda_1| = 0.3819660...


def Z_golden(Lmax):
    """Z_L for L=0..Lmax via the transfer matrix (exact integer arithmetic)."""
    T = np.array([[1, 1], [1, 0]], dtype=object)   # object dtype -> big ints
    u = np.array([1, 1], dtype=object)             # boundary vectors
    Z = []
    M = np.array([[1, 0], [0, 1]], dtype=object)
    for L in range(Lmax + 1):
        Z.append(int(u @ M @ u))
        M = M @ T
    return np.array(Z, dtype=object)


def main():
    banner("Experiment 1: golden-mean shift (decomposable, treewidth 1)")
    Lmax = 40
    Z = Z_golden(Lmax)
    L = np.arange(Lmax + 1)
    ratio = np.array([Z[i + 1] / Z[i] for i in range(Lmax)], dtype=float)
    Ls = L[:Lmax]

    print(f"  phi                         = {PHI:.15f}")
    print(f"  spectral gap |l2/l1| = 1/phi^2 = {GAP:.15f}")
    print(f"  Z_1..Z_8                    = {[int(z) for z in Z[1:9]]}  (Fibonacci F_{{L+2}})")
    print(f"  ratio Z_L+1/Z_L at L=10,20,30 = "
          f"{ratio[10]:.12f}, {ratio[20]:.12f}, {ratio[30]:.12f}")

    err = np.abs(ratio - PHI)
    # empirical decay rate of the error per step
    emp = (err[25] / err[15]) ** (1 / 10)
    print(f"  empirical per-step error decay = {emp:.6f}  (theory: {GAP:.6f})")

    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.5))

    ax[0].axhline(PHI, color="0.5", ls="--", lw=1, label=r"$\varphi=(1+\sqrt{5})/2$")
    ax[0].plot(Ls, ratio, "o-", color=C[0], ms=3)
    ax[0].set_xlabel(r"word length $L$")
    ax[0].set_ylabel(r"ratio $Z_{L+1}/Z_L$")
    ax[0].set_title(r"(a) ratio $\to$ conjectured rate $\varphi$")
    ax[0].set_xlim(0, Lmax)
    ax[0].legend(loc="lower right")

    sel = (Ls >= 2) & (Ls <= 35)
    ax[1].semilogy(Ls[sel], err[sel], "o", color=C[1], ms=3,
                   label=r"$|Z_{L+1}/Z_L-\varphi|$")
    ax[1].semilogy(Ls[sel], err[2] * GAP ** (Ls[sel] - 2), "-", color="0.4",
                   label=r"slope $=\log(\varphi^{-2})$ (spectral gap)")
    ax[1].set_xlabel(r"word length $L$")
    ax[1].set_ylabel("ratio error")
    ax[1].set_title("(b) convergence speed $=$ spectral gap")
    ax[1].legend(loc="upper right")

    fig.tight_layout()
    savefig(fig, "exp1_golden_mean.pdf")


if __name__ == "__main__":
    main()
