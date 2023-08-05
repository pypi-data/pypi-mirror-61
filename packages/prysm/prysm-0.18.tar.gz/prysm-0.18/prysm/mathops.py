"""A submodule which imports and exports math functions from different libraries.

The intend is to make the backend for prysm interoperable, allowing users to
utilize more high performance engines if they have them installed, or fall
back to more widely available options in the case that they do not.
"""
import numpy as np

from scipy.special import j1, j0  # NOQA

from prysm.conf import config


def jinc(r):
    """Jinc.

    Parameters
    ----------
    r : `number`
        radial distance

    Returns
    -------
    `float`
        the value of j1(x)/x for x != 0, 0.5 at 0

    """
    if r < 1e-8 and r > -1e-8:  # value of jinc for x < 1/2 machine precision  is 0.5
        return 0.5
    else:
        return j1(r) / r


def sign(x):
    """Sign of a number.  Note only works for single values, not arrays."""
    return -1 if x < 0 else 1


def kronecker(i, j):
    """Kronecker delta function, 1 if i = j, otherwise 0."""
    return 1 if i == j else 0


def gamma(n, m):
    """Gamma function."""
    if n == 1 and m == 2:
        return 3 / 8
    elif n == 1 and m > 2:
        mm1 = m - 1
        numerator = 2 * mm1 + 1
        denominator = 2 * (mm1 - 1)
        coef = numerator / denominator
        return coef * gamma(1, mm1)
    else:
        nm1 = n - 1
        num = (nm1 + 1) * (2 * m + 2 * nm1 - 1)
        den = (m + nm1 - 2) * (2 * nm1 + 1)
        coef = num / den
        return coef * gamma(nm1, m)


class MathEngine:
    """An engine allowing an interchangeable backend for mathematical functions."""
    def __init__(self, source=np):
        """Create a new math engine.

        Parameters
        ----------
        source : `module`
            a python module.

        """
        self.source = source

    def __getattr__(self, key):
        """Get attribute.

        Parameters
        ----------
        key : `str` attribute name

        """
        try:
            return getattr(self.source, key)
        except AttributeError:
            # function not found, fall back to numpy
            # this will actually work nicely for numpy 1.16+
            # due to the __array_function__ and __array_ufunc__ interfaces
            # that were implemented
            return getattr(self.source, key)  # this can raise, but we don't *need* to catch

    def change_backend(self, backend):
        """Run when changing the backend."""
        self.source = backend
        globals()['jinc'] = self.vectorize(jinc)


engine = MathEngine()
config.chbackend_observers.append(engine.change_backend)

jinc = engine.vectorize(jinc)
