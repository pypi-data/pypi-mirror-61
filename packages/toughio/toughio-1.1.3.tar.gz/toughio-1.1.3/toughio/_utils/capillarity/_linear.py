from ._base import BaseCapillarity

__all__ = [
    "Linear",
]


class Linear(BaseCapillarity):
    """Linear function.

    Parameters
    ----------
    pmax : scalar
        Maximum pressure (CP(1)).
    smin : scalar
        Lower liquid saturation threshold (CP(2)).
    smax : scalar
        Upper liquid saturation threshold (CP(3)).

    """

    _id = 1
    _name = "Linear"

    def __init__(self, pmax, smin, smax):
        assert smax > smin
        self.parameters = [pmax, smin, smax]

    def _eval(self, sl, pmax, smin, smax):
        """Linear function."""
        return (
            -pmax
            if sl <= smin
            else 0.0
            if sl >= smax
            else -pmax * (smax - sl) / (smax - smin)
        )

    @property
    def parameters(self):
        """Return model parameters."""
        return [self._pmax, self._smin, self._smax]

    @parameters.setter
    def parameters(self, value):
        assert len(value) == 3
        self._pmax = value[0]
        self._smin = value[1]
        self._smax = value[2]
