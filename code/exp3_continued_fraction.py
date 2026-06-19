"""Experiment 3 -- a transfer operator with an INFINITE alphabet collapsed onto a
fixed finite state space; the flagship "computation assists a convergence proof".

Set E_2 = continued fractions [0; a_1, a_2, ...] with all digits a_i in {1,2}.
Its Hausdorff dimension s* is the Bowen root of the pressure: s* is the unique s
with leading eigenvalue lambda(s) = 1 of the Ruelle transfer operator

      (L_s f)(x) = sum_{a in {1,2}} (a+x)^{-2s} f(1/(a+x)),     x in [0,1].

The weight phi_I(x) = |D(psi_{a_1} o ... o psi_{a_n})(x)|^s is multiplicative along
the word (chain rule), so the n-th partition function Z_n(s) = sum_{|I|=n} sup|phi_I|^s
has growth rate lambda(s).  Two computations, cross-checked against the published
value s* = 0.5312805062772... (Jenkinson-Pollicott):

  (A) Chebyshev collocation of L_s on a FIXED grid of N+1 nodes (independent of
      word length) -> leading eigenvalue lambda(s) -> root-find lambda(s*)=1.
      This is the decomposable / finite-transfer-operator route: fast, accurate.

  (B) the elementary "divide out the conjectured rate and watch the ratio" route:
      enumerate all 2^n words, form Z_n(s), and show Z_{n+1}(s)/Z_n(s) -> 1
      exactly at s = s* (and -> != 1 otherwise).
"""
import numpy as np
from scipy.optimize import brentq
from common import savefig, banner, C, plt

S_STAR_REF = 0.5312805062772      # Jenkinson-Pollicott reference value


# --------------------------------------------------------------------------
# (A) Chebyshev collocation of the transfer operator on [0,1].
# --------------------------------------------------------------------------
def cheb_nodes_weights(N):
    """Chebyshev-Lobatto nodes on [0,1] and barycentric weights."""
    k = np.arange(N + 1)
    x = np.cos(np.pi * k / N)              # in [-1,1]
    t = (x + 1) / 2                        # mapped to [0,1]
    w = np.ones(N + 1)
    w[0] = 0.5
    w[-1] = 0.5
    w *= (-1.0) ** k
    return t, w


def bary_basis(t, w, y):
    """Row vector of barycentric Lagrange basis values b_k(y) at a scalar y."""
    diff = y - t
    hit = np.isclose(diff, 0.0)
    if hit.any():
        b = np.zeros_like(t)
        b[np.argmax(hit)] = 1.0
        return b
    c = w / diff
    return c / c.sum()


def operator_matrix(s, t, w):
    N1 = len(t)
    M = np.zeros((N1, N1))
    for i, ti in enumerate(t):
        for a in (1, 2):
            y = 1.0 / (a + ti)
            M[i, :] += (a + ti) ** (-2.0 * s) * bary_basis(t, w, y)
    return M


def leading_eig(s, t, w):
    M = operator_matrix(s, t, w)
    ev = np.linalg.eigvals(M)
    return ev


def lambda_of_s(s, t, w):
    ev = leading_eig(s, t, w)
    return np.max(ev.real)


def dimension_via_operator(N):
    t, w = cheb_nodes_weights(N)
    s_star = brentq(lambda s: lambda_of_s(s, t, w) - 1.0, 0.3, 0.8, xtol=1e-13)
    # spectral gap at s*
    ev = np.sort_complex(leading_eig(s_star, t, w))
    mags = np.sort(np.abs(ev))[::-1]
    gap = mags[1] / mags[0]
    return s_star, gap


# --------------------------------------------------------------------------
# (B) elementary word enumeration: divide out the rate, watch the ratio.
# --------------------------------------------------------------------------
def Z_words(s, nmax, x0=0.5):
    """Z_n(s) = sum over 2^n words of |derivative|^s, for n=1..nmax."""
    pts = np.array([x0])
    ld = np.array([0.0])             # accumulated log|derivative|
    Z = []
    for _ in range(nmax):
        new_pts = []
        new_ld = []
        for a in (1, 2):
            new_pts.append(1.0 / (a + pts))
            new_ld.append(ld - 2.0 * np.log(a + pts))
        pts = np.concatenate(new_pts)
        ld = np.concatenate(new_ld)
        Z.append(np.sum(np.exp(s * ld)))
    return np.array(Z)


def main():
    banner("Experiment 3: Hausdorff dimension of the E_2 continued-fraction set")
    print(f"  reference s* = dim_H(E_2) = {S_STAR_REF:.13f}  (Jenkinson-Pollicott)")

    # (A) operator route: convergence in grid size N
    print("\n  (A) transfer-operator collocation (fixed grid, any word length):")
    rows = []
    for N in [4, 6, 8, 10, 12, 16, 20, 24]:
        s_star, gap = dimension_via_operator(N)
        rows.append((N, s_star, gap))
        print(f"      N={N:3d}  s*_N = {s_star:.13f}  err={abs(s_star-S_STAR_REF):.2e}  "
              f"spectral gap |l2/l1|={gap:.4f}")
    s_best = rows[-1][1]
    gap_best = rows[-1][2]

    # (B) word route: ratio Z_{n+1}/Z_n at s*, s*-0.03, s*+0.03
    print("\n  (B) word-enumeration ratio test (divide out the rate):")
    nmax = 18
    svals = [s_best - 0.03, s_best, s_best + 0.03]
    labels = [r"$s=s^*-0.03$", r"$s=s^*$", r"$s=s^*+0.03$"]
    ratios = []
    for s in svals:
        Z = Z_words(s, nmax)
        r = Z[1:] / Z[:-1]
        ratios.append(r)
        print(f"      s={s:.5f}:  Z_n+1/Z_n at n=8,12,17 = "
              f"{r[7]:.6f}, {r[11]:.6f}, {r[16]:.6f}")

    # ---- figures ----
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.5))

    Ns = np.array([r[0] for r in rows])
    errs = np.array([abs(r[1] - S_STAR_REF) for r in rows])
    ax[0].semilogy(Ns, errs, "o-", color=C[0], ms=4)
    ax[0].set_xlabel(r"collocation grid size $N$")
    ax[0].set_ylabel(r"$|s^*_N - s^*|$")
    ax[0].set_title(r"(a) operator route: spectral convergence to $\dim_H E_2$")

    nn = np.arange(1, nmax)
    for r, lab, col in zip(ratios, labels, [C[1], C[2], C[3]]):
        ax[1].plot(nn, r, "o-", color=col, ms=3, label=lab)
    ax[1].axhline(1.0, color="0.5", ls="--", lw=1)
    ax[1].set_xlabel(r"word length $n$")
    ax[1].set_ylabel(r"ratio $Z_{n+1}(s)/Z_n(s)$")
    ax[1].set_title(r"(b) word route: ratio $\to 1$ iff $s=s^*$")
    ax[1].legend(loc="center right")

    fig.tight_layout()
    savefig(fig, "exp3_continued_fraction.pdf")
    print(f"\n  best estimate s* (N=24) = {s_best:.10f}, gap = {gap_best:.4f}")


if __name__ == "__main__":
    main()
