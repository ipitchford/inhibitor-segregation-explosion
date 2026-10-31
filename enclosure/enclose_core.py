"""Two-sided enclosure of the explosion probability in the conversion-inhibition model.

The exact identity P(T<inf) = E[P(K_inf < z | marked environment)] is evaluated through the backward
equation of the operational-time chain (I, k), where k counts auxiliary Bernoulli(e^{-b u}) successes
attached to inhibitor conversion (birth) events.  Two-sided bounds come from monotone comparisons:
  * on each time step the success probability is frozen at an upper bound of its largest value
    (lower bound) or a lower bound of its smallest value (upper bound);
  * truncation at I = N + 1 with payoff 1 - E[remaining successes]/(z-k) (lower) or 1 (upper);
  * the same payoffs at the horizon U;
  * on each step the frozen generator is applied by uniformisation; the Poisson tail is dropped
    (lower) or its mass added (upper).
Rounding.  Time steps are dyadic, so step lengths and Poisson means are exact binary64 numbers.
Every transcendental or cancelling quantity (exponentials, Poisson weights and tail, payoffs) is
computed in decimal arithmetic at 50 significant digits (correctly rounded exp) and converted to
binary64 with a one-ulp nudge in the conservative direction.  Every remaining floating-point
operation forms sums of products of nonnegative numbers.  In the standard model each binary64
operation returns (exact)(1 + e) + f with |e| <= 2^-53 and |f| < 2^-1074 (f = 0 for sums), so each
operator application and each Poisson-weighted sum (at most 80 terms; at most about ninety successive
operations) has relative error below 1e-14 plus an absolute error far below 1e-300.  An outward
relative factor EPS_OUT = 1e-13 and an absolute allowance ABS_OUT = 1e-300 are applied after every
such operation, so underflow and subnormal values are covered.  Decimal quantities are correctly
rounded at 50 digits; each conversion to binary64 is nearest-then-one-ulp in the safe direction
(never below 0), which is valid because the Decimal error is far below half an ulp; payoffs below
1e-20 are set to 0 (when positive, a payoff is computed with absolute Decimal error below 1e-47).
The argument is made for complete export (p = 0), rates in [1/16, 16] (so that the binary64 divisor Lam is at
least 1/16 and underflow errors stay far below 1e-300 after division), 1 <= z <= 10, N <= 2000,
U <= 64, steps of at most 1/64, exact binary64 grid points, rates and Poisson means, and at most 80
Poisson terms; Delta = b + lam - d is computed exactly as a rational number.  Other inputs are refused.
Assumes IEEE-754 binary64 arithmetic with correctly rounded
+,-,*,/ (as provided by NumPy on IEEE hardware).  Standard library + NumPy.  No assert statements.
"""
import math
from decimal import Decimal, Context, getcontext, setcontext, ROUND_HALF_EVEN
from fractions import Fraction
import numpy as np

DEC_CONTEXT = Context(prec=50, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999)
setcontext(DEC_CONTEXT.copy())
EPS_OUT = 1e-13
ABS_OUT = 1e-300    # absolute allowance per operation for underflow (IEEE products and quotients err by < 2^-1074 absolutely)
INF = float("inf")

def fail(msg):
    raise RuntimeError(msg)

def down(x):
    """binary64 number <= the Decimal x >= 0 (nearest conversion, one ulp down, never below 0)."""
    return max(0.0, math.nextafter(float(x), -INF))

def up(x):
    return math.nextafter(float(x), INF)

def dexp_neg(x):
    """Decimal e^{-x} for a binary64 x >= 0 (Decimal(x) is exact)."""
    return (-Decimal(x)).exp()

def mean_tail_up(u, i, b, c, d, lam, p):
    """Upper bound on E[sum_{tau_j>u} e^{-b tau_j} | I(u)=i] = d e^{-bu} (i + c/b) / Delta, Delta = b + lam(1-p) - d > 0."""
    B, C, Dd = (Decimal(v) for v in (b, c, d))
    DF = Fraction(b) + Fraction(lam) * (1 - Fraction(p)) - Fraction(d)       # exact
    Delta = Decimal(DF.numerator) / Decimal(DF.denominator)                  # one correctly rounded division
    if DF <= 0:
        fail("first-moment bound needs Delta > 0")
    return Dd * (-(B * Decimal(u))).exp() * (Decimal(i) + C / B) / Delta

def poisson_weights(mu, tol=Decimal("1e-17")):
    """Lower/upper binary64 weights for Poisson(mu) terms 0..M-1 and an upper bound on the omitted tail."""
    M = Decimal(mu)
    t = (-M).exp()
    w = []
    n = 0
    while True:
        w.append(t)
        n += 1
        t = t * M / n
        if n > mu + 1:
            tail = t / (1 - M / (n + 1))       # geometric bound on P(N >= n)
            if tail < tol:
                break
        if n > 100000:
            fail("Poisson series did not converge")
    lo = np.array([down(x) for x in w])
    hi = np.array([up(x) for x in w])
    return lo, hi, up(tail)

def dyadic_floor(x):
    """Largest power of two <= x (x > 0)."""
    return 2.0 ** math.floor(math.log2(x))

def enclose(b, c, d, lam, p, z, i0, N, U, h0, hmax):
    """Run with a private 50-digit decimal context, restoring the caller's context afterwards."""
    saved = getcontext()
    setcontext(DEC_CONTEXT.copy())
    try:
        return _enclose(b, c, d, lam, p, z, i0, N, U, h0, hmax)
    finally:
        setcontext(saved)

def _enclose(b, c, d, lam, p, z, i0, N, U, h0, hmax):
    if not all(isinstance(v, float) for v in (U, h0, hmax)):
        fail("U, h0 and hmax must be binary64 floats")
    for v in (b, c, d, lam):
        if not (isinstance(v, float) and 1 / 16 <= v <= 16):
            fail("rates must be binary64 numbers in [1/16, 16]")
    if p != 0 or not (1 <= z <= 10) or not (1 <= N <= 2000) or not (0 <= i0 <= N) or not (0 < hmax <= 2 ** -6) or not (0 < U <= 64):
        fail("the rounding argument covers only p = 0, 1 <= z <= 10, 1 <= N <= 2000, 0 <= i0 <= N, steps <= 1/64, U <= 64")
    i = np.arange(N + 1, dtype=float)
    Lam = c + d * N + lam
    if Fraction(Lam) != Fraction(c) + Fraction(d) * N + Fraction(lam):
        fail("uniformisation rate not exact in binary64")
    stay_w = d * (N - i)                            # = Lam - c - d i - lam, computed without cancellation

    def payoff_lower(u, ii, k):
        # When v > 0 we have E[H]/(z-k) < 1, so about ten correctly rounded Decimal operations at
        # relative precision 1e-49 give |error of v| < 1e-47; values below 1e-20 are replaced by 0, and
        # one binary64 ulp of any value above 1e-20 exceeds 1e-36.
        v = 1 - mean_tail_up(u, ii, b, c, d, lam, p) / (z - k)
        return down(v) if v > Decimal("1e-20") else 0.0

    lo = np.array([[payoff_lower(U, ii, k) for ii in range(N + 1)] for k in range(z)])
    hi = np.ones((z, N + 1))
    def T(g, q, exitv, lower):
        out = np.empty_like(g)
        for k in range(z):
            nxt = np.append(g[k, 1:], exitv[k])
            nxtk = np.append(g[k + 1, 1:], exitv[k + 1]) if k + 1 < z else np.zeros(N + 1)
            cat = np.full(N + 1, g[k, 0])                 # p = 0: a division resets I to 0
            out[k] = (c * nxt + d * i * ((1.0 - q) * nxt + q * nxtk) + lam * cat + stay_w * g[k]) / Lam
        if lower:
            return np.maximum(out * (1 - EPS_OUT) - ABS_OUT, 0.0)
        return np.minimum(out * (1 + EPS_OUT) + ABS_OUT, 1.0)

    u = float(U)
    steps = 0
    while u > 0:
        h = min(dyadic_floor(min(hmax, h0 * math.exp(b * u / 2))), u)
        if h < u:
            h = dyadic_floor(h)
        ua, ub = u - h, u
        if Fraction(ua) != Fraction(ub) - Fraction(h):
            fail("time grid not exact")
        q_hi = min(1.0, up(dexp_neg(b * ua)) if b * ua == Fraction(b) * Fraction(ua) else 1.0)
        q_lo = max(0.0, down(dexp_neg(b * ub))) if b * ub == Fraction(b) * Fraction(ub) else 0.0
        mu = Lam * h
        if Fraction(mu) != Fraction(Lam) * Fraction(h):
            fail("Poisson mean not exact")
        if mu > 32:
            fail("Poisson mean above the range covered by the rounding argument")
        wl, wu, tail = poisson_weights(mu)
        if len(wl) > 80:
            fail("too many Poisson terms for the rounding argument")
        exit_lo = [payoff_lower(ua, N + 1, k) for k in range(z)]
        acc = wl[0] * lo; g = lo
        for n in range(1, len(wl)):
            g = T(g, q_hi, exit_lo, True); acc = acc + wl[n] * g
        lo = np.maximum(acc * (1 - EPS_OUT) - ABS_OUT, 0.0)
        acc = wu[0] * hi; g = hi
        for n in range(1, len(wu)):
            g = T(g, q_lo, [1.0] * z, False); acc = acc + wu[n] * g
        hi = np.minimum((acc + tail) * (1 + EPS_OUT) + ABS_OUT, 1.0)
        u = ua; steps += 1
    return float(lo[0, i0]), float(hi[0, i0]), steps
