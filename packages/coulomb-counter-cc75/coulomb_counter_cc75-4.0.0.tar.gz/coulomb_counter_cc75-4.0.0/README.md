# coulomb_counter_cc75_py
Python library for the coulomb counter cc75
========================================================

The Coulomb_counter class allows to read and manage data from a USB
connection with a coulomb counter cc75.

You can install it with pip:

    pip install coulomb_counter_cc75

Exemple d'usage:

    >>> from coulomb_counter_cc75 import Coulomb_counter
    >>> Coulomb_counter.onUpdate = lambda self: print(self)
    >>> coulomb_counter = Coulomb_counter("/dev/ttyUSB0")
    >>> coulomb_counter.launch()
