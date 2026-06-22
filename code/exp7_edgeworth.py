"""Experiment 7 -- a DIFFERENT kind of series: the Edgeworth expansion of a
U-statistic, whose coefficients (cumulants) are connected-diagram einsums.

This is NOT a growth-rate problem.  We study the *asymptotic series* in n^{-1/2}
for the distribution of a standardized U-statistic,

   P(W_n <= x) = Phi(x) - phi(x)[ lambda_3/6 He2(x)
                  + lambda_4/24 He3(x) + lambda_3^2/72 He5(x) + ... ],

whose coefficients are the standardized cumulants lambda_r of W_n.  The point of
contact with the companion paper: the cumulants of a U-statistic are sums over
*connected diagrams*, each an einsum of the kernel's canonical components, and
the moment<->cumulant map is Moebius inversion on the partition lattice -- the
same inclusion-exclusion as the paper's U<->V relation.

Model (finite alphabet, so every coefficient is an exact contraction).
X_1..X_n i.i.d. on {1,2,3} with law p; symmetric kernel H (H_aa = 0);

   U_n = binom(n,2)^{-1} sum_{i<j} H[X_i,X_j]
       = (N^T H N)/(n(n-1)),   N ~ Multinomial(n,p).

Canonical (Hoeffding) components, all einsums of H and p:
   theta = p^T H p,   g1 = H p - theta,   g2[a,b] = H[a,b]-g1[a]-g1[b]-theta,
   zeta1 = sum_x p_x g1(x)^2,   gamma1 = sum_x p_x g1(x)^3,
   J = sum_{a,b} p_a p_b g1(a) g1(b) g2(a,b).

The leading skewness is the sum of TWO connected diagrams (this is the lesson --
a single diagram is wrong; they partially cancel):
   kappa_3(U_n) = 8(gamma1 + 3 J)/n^2 + O(n^{-3}),
   lambda_3 = kappa_3/sigma_n^3 -> c3 * n^{-1/2},   c3 = (gamma1 + 3 J)/zeta1^{3/2}.

We (i) verify the einsum coefficient c3 against the exact cumulants (computed via
multinomial factorial moments) and Monte Carlo; (ii) show the asymptotic-series
structure: successive terms shrink as n^{-1/2}, n^{-1}, and the Edgeworth CDF
beats the normal at exactly those rates.
"""
import numpy as np
from itertools import product
from scipy.stats import norm
from common import savefig, banner, C, plt

# ---- model: a symmetric kernel (zero diagonal) on a 5-letter alphabet, with a
# right-skewed law.  A 5-letter alphabet with incommensurate entries keeps U_n
# off any lattice, so its distribution is smooth even at moderate n.
H = np.array([[0.0000, 2.3422, 0.7603, 0.6514, 0.8908],
              [2.3422, 0.0000, 1.2930, 1.3777, 1.6366],
              [0.7603, 1.2930, 0.0000, 3.5483, 3.7831],
              [0.6514, 1.3777, 3.5483, 0.0000, 3.3073],
              [0.8908, 1.6366, 3.7831, 3.3073, 0.0000]])
P = np.array([0.2757, 0.2163, 0.1898, 0.1866, 0.1317])
Q = len(P)

# ---- probabilists' Hermite polynomials ----
def He(k, x):
    return {2: x**2 - 1, 3: x**3 - 3*x, 4: x**4 - 6*x**2 + 3,
            5: x**5 - 10*x**3 + 15*x,
            6: x**6 - 15*x**4 + 45*x**2 - 15}[k]

# ---- Stirling numbers of the 2nd kind (for exact multinomial moments) ----
def _stirling(nmax):
    S = [[0]*(nmax+1) for _ in range(nmax+1)]
    S[0][0] = 1
    for i in range(1, nmax+1):
        for k in range(1, i+1):
            S[i][k] = k*S[i-1][k] + S[i-1][k-1]
    return S
_S = _stirling(8)


def EQ_power(r, n):
    """Exact E[(N^T H N)^r] for N ~ Multinomial(n, p), via factorial moments."""
    mono = {(0,)*Q: 1.0}                       # expand Q^r into monomials in N
    for _ in range(r):
        new = {}
        for e, c in mono.items():
            for a in range(Q):
                for b in range(Q):
                    if H[a, b] == 0:
                        continue
                    e2 = list(e); e2[a] += 1; e2[b] += 1
                    e2 = tuple(e2)
                    new[e2] = new.get(e2, 0.0) + c*H[a, b]
        mono = new
    total = 0.0
    for e, c in mono.items():                   # E[prod_a N_a^{e_a}] via Stirling
        rng = [range(1, ea+1) if ea > 0 else range(1) for ea in e]
        s = 0.0
        for ks in product(*rng):
            K = sum(ks)
            ff = 1.0
            for t in range(K):
                ff *= (n - t)                   # falling factorial (n)_K
            term = ff
            for a in range(Q):
                if e[a] > 0:
                    term *= _S[e[a]][ks[a]] * P[a]**ks[a]
            s += term
        total += c*s
    return total


def exact_cumulants(n):
    """Standardized cumulants lambda_3, lambda_4 and variance of U_n, exactly."""
    den = n*(n-1.0)
    m = [EQ_power(r, n)/den**r for r in range(1, 5)]   # raw moments E[U^r]
    mu = m[0]
    k2 = m[1] - mu**2
    k3 = m[2] - 3*mu*m[1] + 2*mu**3
    k4 = m[3] - 4*mu*m[2] + 6*mu**2*m[1] - 3*mu**4 - 3*k2**2
    return k3/k2**1.5, k4/k2**2, k2, mu


def diagram_coefficients():
    theta = np.einsum("a,ab,b->", P, H, P)
    g1 = H @ P - theta
    zeta1 = np.einsum("x,x->", P, g1**2)
    gamma1 = np.einsum("x,x->", P, g1**3)
    g2 = H - g1[:, None] - g1[None, :] - theta
    Jdiag = np.einsum("a,b,a,b,ab->", P, P, g1, g1, g2)
    c3 = (gamma1 + 3*Jdiag) / zeta1**1.5
    return dict(theta=theta, zeta1=zeta1, gamma1=gamma1, J=Jdiag, c3=c3)


def edgeworth_cdf(x, n, terms):
    l3, l4, _, _ = exact_cumulants(n)
    F = norm.cdf(x)
    if terms >= 1:
        F = F - norm.pdf(x)*(l3/6*He(2, x))
    if terms >= 2:
        F = F - norm.pdf(x)*(l4/24*He(3, x) + l3**2/72*He(5, x))
    return F


def edgeworth_pdf(x, n, terms):
    l3, l4, _, _ = exact_cumulants(n)
    f = norm.pdf(x)
    corr = np.ones_like(x)
    if terms >= 1:
        corr = corr + l3/6*He(3, x)
    if terms >= 2:
        corr = corr + l4/24*He(4, x) + l3**2/72*He(6, x)
    return f*corr


def mc_W(n, M, rng):
    _, _, k2, mu = exact_cumulants(n)
    N = rng.multinomial(n, P, size=M).astype(float)
    U = np.einsum("ma,ab,mb->m", N, H, N) / (n*(n-1))
    return (U - mu) / np.sqrt(k2)


def main():
    banner("Experiment 7: Edgeworth expansion of a U-statistic (cumulants = einsums)")
    d = diagram_coefficients()
    print(f"  diagram pieces (einsums of H,p):  gamma1 = {d['gamma1']:.5f}  "
          f"(g1^3 diagram),   J = {d['J']:.5f}  (g1-g1-g2 cross diagram)")
    print(f"  leading skewness coefficient  c3 = (gamma1+3J)/zeta1^(3/2) = {d['c3']:.5f}")
    print(f"  (a single diagram gamma1/zeta1^1.5 = {d['gamma1']/d['zeta1']**1.5:.4f} "
          f"would be WRONG; the cross-diagram J cancels most of it)")

    print("\n  (i) verify c3 against exact cumulants (lambda_3 * sqrt(n) -> c3):")
    for n in [16, 32, 64, 128, 256]:
        l3, l4, _, _ = exact_cumulants(n)
        print(f"      n={n:4d}:  exact lambda_3*sqrt(n) = {l3*np.sqrt(n):.4f}    "
              f"lambda_4*n = {l4*n:.3f}")

    rng = np.random.default_rng(0)
    n_chk = 64
    W = mc_W(n_chk, 8_000_000, rng)
    l3c, _, _, _ = exact_cumulants(n_chk)
    print(f"\n  (ii) Monte-Carlo check at n={n_chk}:  MC skew = {np.mean(W**3):.4f}   "
          f"exact lambda_3 = {l3c:.4f}")

    # (iii) the payoff: each Edgeworth term lowers the approximation error
    print("\n  (iii) CDF sup-error vs Monte-Carlo truth (more terms -> smaller error):")
    nrate = np.array([12, 16, 24, 32, 48, 64, 96, 128])
    xg = np.linspace(-3.5, 3.8, 361)
    e0, e1, e2 = [], [], []
    for n in nrate:
        W = mc_W(n, 16_000_000, np.random.default_rng(100+n))
        Femp = np.searchsorted(np.sort(W), xg, side="right")/len(W)
        e0.append(np.max(np.abs(Femp - edgeworth_cdf(xg, n, 0))))
        e1.append(np.max(np.abs(Femp - edgeworth_cdf(xg, n, 1))))
        e2.append(np.max(np.abs(Femp - edgeworth_cdf(xg, n, 2))))
        print(f"      n={n:4d}:  normal {e0[-1]:.2e}   1-term {e1[-1]:.2e}   "
              f"2-term {e2[-1]:.2e}")
    e0, e1, e2 = map(np.array, (e0, e1, e2))

    # ---- figures ----
    fig, ax = plt.subplots(1, 2, figsize=(9.4, 3.6))

    # (a) density at moderate n: MC vs normal vs Edgeworth
    n0 = 20
    W = mc_W(n0, 10_000_000, np.random.default_rng(7))
    bins = np.linspace(-3.0, 4.2, 70)
    ax[0].hist(W, bins=bins, density=True, color="0.86", edgecolor="0.72",
               label=fr"true law of $W_n$ (MC, $n={n0}$)")
    xs = np.linspace(-3.0, 4.4, 400)
    ax[0].plot(xs, norm.pdf(xs), "--", color=C[0], label="normal")
    ax[0].plot(xs, edgeworth_pdf(xs, n0, 1), "-", color=C[1],
               label="Edgeworth, 1 term")
    ax[0].plot(xs, edgeworth_pdf(xs, n0, 2), "-", color=C[2],
               label="Edgeworth, 2 terms")
    ax[0].set_xlabel(r"standardized $W_n$")
    ax[0].set_ylabel("density")
    ax[0].set_title(r"(a) Edgeworth captures the skew, $n=20$")
    ax[0].legend(loc="upper right", fontsize=8)

    # (b) the payoff: successive Edgeworth terms lower the error
    ax[1].loglog(nrate, e0, "o-", color=C[0], ms=4, label="normal")
    ax[1].loglog(nrate, e1, "s-", color=C[1], ms=4, label="+ skewness (1 term)")
    ax[1].loglog(nrate, e2, "^-", color=C[2], ms=4, label="+ kurtosis (2 terms)")
    ax[1].loglog(nrate, e0[0]*(nrate/nrate[0])**-0.5, ":", color="0.5", lw=1,
                 label=r"slopes $-1/2,\ -1$")
    ax[1].loglog(nrate, e1[0]*(nrate/nrate[0])**-1.0, ":", color="0.5", lw=1)
    ax[1].set_xlabel(r"sample size $n$")
    ax[1].set_ylabel(r"$\sup_x|F_n(x)-\widehat F(x)|$")
    ax[1].set_title(r"(b) each Edgeworth term lowers the error")
    ax[1].legend(loc="lower left", fontsize=8)

    fig.tight_layout()
    savefig(fig, "edgeworth.pdf")


if __name__ == "__main__":
    main()
