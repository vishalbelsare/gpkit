# -*- coding: utf-8 -*-
"""Lightweight GP Modeling Package

    For examples please see the examples folder.

    Requirements
    ------------
    numpy
    MOSEK or CVXOPT
    scipy(optional): for full sparse matrix support
    sympy(optional): for latex printing in iPython Notebook

    Attributes
    ----------
    settings : dict
        Contains settings loaded from ``./env/settings``
"""

try:
    from pint import UnitRegistry
    units = UnitRegistry()

except ImportError:
    print "Unable to load pint; unit support disabled."

    class Quantity(object):
        "Dummy class for missing pint"
        pass

    class Units(object):
        "Dummy class to replace missing pint"
        Quantity = Quantity

        def __nonzero__(self):
            return 0

    units = Units()

from .nomials import Monomial, Posynomial, Variable
from .nomial_interfaces import mon, vecmon
from .posyarray import PosyArray
from .geometric_program import GP

if units:
    # regain control of Quantities' interactions with Posynomials
    Posynomial = Posynomial
    import operator

    def Qmul(self, other):
        if isinstance(other, Posynomial):
            return NotImplemented
        else:
            return self._mul_div(other, operator.mul)

    def Qtruediv(self, other):
        if isinstance(other, Posynomial):
            return NotImplemented
        else:
            return self._mul_div(other, operator.truediv)

    def Qfloordiv(self, other):
        if isinstance(other, Posynomial):
            return NotImplemented
        else:
            return self._mul_div(other, operator.floordiv, units_op=operator.truediv)

    units.Quantity.__mul__ = Qmul
    units.Quantity.__div__ = Qtruediv
    units.Quantity.__truediv__ = Qtruediv
    units.Quantity.__floordiv__ = Qfloordiv

# Load settings
from os import sep as os_sep
from os.path import dirname as os_path_dirname
settings_path = os_sep.join([os_path_dirname(__file__), "env", "settings"])
with open(settings_path) as settingsfile:
    lines = [line[:-1].split(" : ") for line in settingsfile
             if len(line.split(" : ")) == 2]
    settings = {name: value.split(", ") for (name, value) in lines}
