"""Experiment 4 -- the motivating NON-decomposable family, and when it collapses.

For matrices T_1, T_2 and a word I = (i_1,...,i_L), set T_I = T_{i_1} ... T_{i_L}.
The self-affine / joint-spectral-radius / affinity-dimension partition functions

      Z_L(s) = sum_{|I|=L} phi^s(T_I),      phi^s = singular-value function,

couple all L indices through a *spectral* function of the whole product: the
decomposition graph is the complete graph K_L (treewidth L-1), so brute force
costs q^L -- this is the friend's "everything in one lump" obstruction.

We demonstrate two things with explicit 2x2 matrices.

(A) Dictionary / dichotomy.  Replacing the operator norm by the *linear* functional
    trace turns the weight multiplicative: sum_I tr(T_I) = tr(S^L), S = T_1+T_2,
    whose decomposition graph is the path P_L (treewidth 1), computable in O(L).
    For NON-NEGATIVE matrices, Perron-Frobenius forces the two pressures to
    coincide,  lim (1/L) log sum_I ||T_I|| = log rho(S),  so the cheap decomposable
    surrogate *proves* the exponential rate that brute force only estimates.
    For SIGNED matrices the rate genuinely differs (cancellation) -- the honest
    boundary of the method.

(B) Affinity dimension.  Z_L(s) with phi^s(A)=sigma_1^s (0<=s<=1) and
    sigma_1 sigma_2^{s-1} (1<=s<=2); the affinity dimension is the root of the
    pressure P(s)=0.  Since sigma_1 sigma_2 = |det| is multiplicative, the s=2
    endpoint is fully decomposable (closed form), which we use to validate the
    brute-force enumeration.
"""
import numpy as np
from scipy.optimize import brentq
from common import savefig, banner, C, plt


# --- non-negative running pair (contractions): used in (A) and (B) ---
T1 = np.array([[0.50, 0.20], [0.10, 0.40]])
T2 = np.array([[0.30, 0.05], [0.25, 0.45]])
# --- a signed pair, used only for the "surrogate fails" remark in (A) ---
S1 = np.array([[0.6, 0.0], [0.0, -0.5]])
S2 = np.array([[0.0, 0.7], [0.5, 0.0]])


def sv_2x2(A):
    """Vectorised singular values of a stack A of 2x2 matrices, shape (m,2,2)."""
    a, b = A[:, 0, 0], A[:, 0, 1]
    c, d = A[:, 1, 0], A[:, 1, 1]
    F = a * a + b * b + c * c + d * d        # ||A||_F^2 = s1^2 + s2^2
    det = a * d - b * c
    disc = np.sqrt(np.maximum(F * F - 4 * det * det, 0.0))
    s1 = np.sqrt((F + disc) / 2)
    s2 = np.abs(det) / np.maximum(s1, 1e-300)
    return s1, s2, np.abs(det)


def enumerate_products(A1, A2, Lmax, checkpoints):
    """Return {L: (s1,s2,absdet, opnorm_sum, trace_sum)} at checkpoint lengths."""
    prods = np.stack([A1, A2])            # (2,2,2): length-1 words
    out = {}
    for L in range(1, Lmax + 1):
        if L > 1:
            prods = np.concatenate([prods @ A1, prods @ A2], axis=0)
        if L in checkpoints:
            s1, s2, ad = sv_2x2(prods)
            tr = prods[:, 0, 0] + prods[:, 1, 1]
            out[L] = dict(s1=s1, s2=s2, absdet=ad,
                          opnorm_sum=float(np.sum(s1)),
                          trace_sum=float(np.sum(tr)))
    return out


def pressure_of_s(data_L, L, s):
    s1, s2, ad = data_L["s1"], data_L["s2"], data_L["absdet"]
    if s <= 1.0:
        phi = s1 ** s
    else:
        phi = s1 * s2 ** (s - 1.0)
    return np.log(np.sum(phi)) / L


def main():
    banner("Experiment 4: matrix products -- non-decomposable, and its collapse")
    S = T1 + T2
    rhoS = np.max(np.abs(np.linalg.eigvals(S)))
    print(f"  non-negative pair: rho(T1+T2) = {rhoS:.12f},  log rho = {np.log(rhoS):.12f}")

    Lmax = 18
    cps = [2, 4, 6, 8, 10, 12, 14, 16, 18]
    data = enumerate_products(T1, T2, Lmax, set(cps))

    # ---- (A) norm-sum pressure (brute force) vs decomposable trace surrogate ----
    print("\n  (A) brute-force ||.||-sum rate vs decomposable trace surrogate "
          "(should both -> log rho(S)):")
    P_norm, P_trace = [], []
    for L in cps:
        pn = np.log(data[L]["opnorm_sum"]) / L
        pt = np.log(data[L]["trace_sum"]) / L
        P_norm.append(pn)
        P_trace.append(pt)
        print(f"      L={L:2d}  (1/L)log sum||T_I|| = {pn:.9f}   "
              f"(1/L)log tr(S^L) = {pt:.9f}   log rho(S) = {np.log(rhoS):.9f}")

    # closed-form trace surrogate for arbitrary L (decomposable, O(L)):
    bigL = 2000
    tr_big = np.log(np.trace(np.linalg.matrix_power(S, bigL))) / bigL
    print(f"      decomposable closed form at L={bigL}: (1/L)log tr(S^L) = {tr_big:.12f}")

    # signed pair: surrogate fails
    Ss = S1 + S2
    rhoSs = np.max(np.abs(np.linalg.eigvals(Ss)))
    dsign = enumerate_products(S1, S2, Lmax, {Lmax})
    pn_sign = np.log(dsign[Lmax]["opnorm_sum"]) / Lmax
    pt_sign = np.log(abs(dsign[Lmax]["trace_sum"])) / Lmax
    print(f"  signed pair: (1/L)log sum||T_I|| = {pn_sign:.6f}  vs  log rho(S1+S2) = "
          f"{np.log(rhoSs):.6f}   (they differ: trace surrogate invalid)")

    # ---- (B) affinity dimension: pressure curve and its root ----
    print("\n  (B) affinity-dimension pressure P(s) and root P(s*)=0:")
    # validation at s=2 (fully decomposable closed form)
    detsum = abs(np.linalg.det(T1)) + abs(np.linalg.det(T2))
    print(f"      validation at s=2: brute (1/L)log Z_L(2)={pressure_of_s(data[Lmax],Lmax,2.0):.9f}"
          f"  closed form log(|det T1|+|det T2|)={np.log(detsum):.9f}")
    sgrid = np.linspace(0.01, 2.0, 60)
    Pbig = np.array([pressure_of_s(data[Lmax], Lmax, s) for s in sgrid])
    roots = {}
    for L in [6, 10, 14, 18]:
        try:
            r = brentq(lambda s: pressure_of_s(data[L], L, s), 0.05, 1.999)
            roots[L] = r
        except ValueError:
            roots[L] = np.nan
    for L in [6, 10, 14, 18]:
        print(f"      L={L:2d}:  affinity-dimension estimate s* = {roots[L]:.6f}")

    # ---- figures ----
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.5))

    ax[0].axhline(np.log(rhoS), color="0.5", ls="--", lw=1,
                  label=r"$\log\rho(T_1+T_2)$ (closed form)")
    ax[0].plot(cps, P_norm, "o-", color=C[1], ms=4,
               label=r"brute force $\frac{1}{L}\log\sum_I\|T_I\|$ ($K_L$, cost $q^L$)")
    ax[0].plot(cps, P_trace, "s-", color=C[0], ms=4,
               label=r"surrogate $\frac{1}{L}\log\mathrm{tr}(S^L)$ ($P_L$, cost $O(L)$)")
    ax[0].set_xlabel(r"word length $L$")
    ax[0].set_ylabel(r"pressure estimate")
    ax[0].set_title(r"(a) non-decomposable rate $=$ decomposable rate")
    ax[0].legend(loc="upper right", fontsize=8)

    ax[1].axhline(0.0, color="0.5", ls="--", lw=1)
    ax[1].plot(sgrid, Pbig, "-", color=C[3], label=r"$P_L(s)$, $L=18$")
    if not np.isnan(roots[18]):
        ax[1].plot([roots[18]], [0.0], "o", color=C[1], ms=7,
                   label=fr"affinity dim $s^*\approx{roots[18]:.3f}$")
    ax[1].set_xlabel(r"exponent $s$")
    ax[1].set_ylabel(r"pressure $P_L(s)$")
    ax[1].set_title(r"(b) affinity dimension $=$ root of $P(s)=0$")
    ax[1].legend(loc="upper right")

    fig.tight_layout()
    savefig(fig, "exp4_matrix_products.pdf")


if __name__ == "__main__":
    main()
