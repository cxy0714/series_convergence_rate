"""Experiment 6 -- verifying a conjectured *order* (sub-exponential exponent).

This is the payoff in the ENTANGLED regime: when no finite transfer matrix
exists you cannot get the rate in closed form, but you can still compute Z_L to
large L and *extract* the conjectured asymptotic order

        Z_L ~ A * lambda^L * L^theta .

The standard tool is the ratio method.  From r_L = Z_{L+1}/Z_L,

        r_L = lambda ( 1 + theta/L + O(1/L^2) )   ==>   theta_L := L ( r_L/lambda - 1 ) -> theta,

and one Richardson step  theta_L^(1) = L*theta_L - (L-1)*theta_{L-1}  kills the
1/L term and converges like O(1/L^2).

We validate the procedure on two sequences whose exponent is *known exactly*, so
we can see it recover the right number:

    central binomial  Z_L = C(2L,L)        ~ 4^L  L^{-1/2}     (theta = -1/2)
    Catalan numbers   Z_L = C(2L,L)/(L+1)  ~ 4^L  L^{-3/2}     (theta = -3/2)

The point: the same extrapolation, applied to self-avoiding-walk counts on a
strip (where lambda and theta are NOT known in closed form), is exactly how the
conjectured 2D exponent  theta = gamma-1 = 11/32 = 0.34375  is corroborated.
"""
import numpy as np
from math import comb
from common import savefig, banner, C, plt


def ratio_exponent(Z, lam):
    """theta_L = L (r_L/lam - 1) and one Richardson acceleration."""
    Z = [float(z) for z in Z]
    r = np.array([Z[i + 1] / Z[i] for i in range(len(Z) - 1)])
    Lr = np.arange(1, len(r) + 1)
    theta = Lr * (r / lam - 1.0)
    # Richardson: theta_L^(1) = L theta_L - (L-1) theta_{L-1}
    rich = np.full_like(theta, np.nan)
    rich[1:] = Lr[1:] * theta[1:] - (Lr[1:] - 1) * theta[:-1]
    return Lr, theta, rich


def main():
    banner("Experiment 6: extracting a conjectured sub-exponential order theta")
    Lmax = 140

    binom = [comb(2 * l, l) for l in range(1, Lmax + 1)]            # theta = -1/2
    catalan = [comb(2 * l, l) // (l + 1) for l in range(1, Lmax + 1)]  # theta = -3/2

    Lb, tb, rb = ratio_exponent(binom, 4.0)
    Lc, tc, rc = ratio_exponent(catalan, 4.0)

    print("  central binomial (true theta = -1/2):")
    print(f"     raw   theta_L at L=20,70,139 = {tb[19]:.5f}, {tb[69]:.5f}, {tb[138]:.5f}")
    print(f"     Rich. theta_L at L=20,70,139 = {rb[19]:.6f}, {rb[69]:.6f}, {rb[138]:.6f}  (-> -0.5)")
    print("  Catalan (true theta = -3/2):")
    print(f"     raw   theta_L at L=20,70,139 = {tc[19]:.5f}, {tc[69]:.5f}, {tc[138]:.5f}")
    print(f"     Rich. theta_L at L=20,70,139 = {rc[19]:.6f}, {rc[69]:.6f}, {rc[138]:.6f}  (-> -1.5)")

    fig, ax = plt.subplots(1, 2, figsize=(9.4, 3.6))

    for (L, th, ri, true, name, col) in [
        (Lb, tb, rb, -0.5, r"central binomial", C[1]),
        (Lc, tc, rc, -1.5, r"Catalan", C[0]),
    ]:
        ax[0].plot(L, th, "-", color=col, lw=1.4, label=fr"{name}: raw $\theta_L$")
        ax[0].axhline(true, color=col, ls=":", lw=1)
    ax[0].set_xlabel(r"word length $L$")
    ax[0].set_ylabel(r"exponent estimate $\theta_L$")
    ax[0].set_title(r"(a) raw ratio method $\theta_L=L(r_L/\lambda-1)$")
    ax[0].legend(loc="center right", fontsize=8)
    ax[0].set_ylim(-1.75, -0.25)

    for (L, ri, true, name, col) in [
        (Lb, rb, -0.5, r"central binomial $\to -1/2$", C[1]),
        (Lc, rc, -1.5, r"Catalan $\to -3/2$", C[0]),
    ]:
        m = ~np.isnan(ri)
        ax[1].plot(L[m], ri[m], "-", color=col, lw=1.4, label=name)
        ax[1].axhline(true, color=col, ls=":", lw=1)
    ax[1].set_xlabel(r"word length $L$")
    ax[1].set_ylabel(r"accelerated estimate $\theta_L^{(1)}$")
    ax[1].set_title(r"(b) one Richardson step pins the exponent")
    ax[1].legend(loc="center right", fontsize=8)
    ax[1].set_ylim(-1.75, -0.25)

    fig.tight_layout()
    savefig(fig, "exponent_fit.pdf")


if __name__ == "__main__":
    main()
