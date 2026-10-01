"""Ontario low-income tax reduction tests. Expected values calculated by hand.

Hand calculations round each step to the cent (like the ON428 form),
so results may differ from the code by a cent.
"""

from canadatax import ontario_tax


def close(a, b):
    return abs(a - b) < 0.02


def test_reduction_examples():
    assert ontario_tax(15_000) == 0                # reduction bigger than tax
    assert close(ontario_tax(20_000), 108.12)      # partial reduction
    assert close(ontario_tax(22_000), 310.12)      # partial reduction
    assert close(ontario_tax(30_000), 859.06)      # no reduction


def test_no_ontario_tax_up_to_18930():
    assert ontario_tax(18_900) == 0


def test_no_reduction_above_24870():
    assert close(ontario_tax(25_000), 606.56)
