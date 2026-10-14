"""2025 tax year tests. Expected values calculated by hand from CRA 2025 rates."""

from canadatax import bracket_tax, cpp_contributions, ei_premium, take_home, total_tax
from canadatax.rates import FEDERAL


def close(a, b):
    return abs(a - b) < 0.02


def test_first_federal_bracket_2025():
    # 14.5% of the first $57,375 = $8,319.38
    assert close(bracket_tax(57_375, FEDERAL[2025]["brackets"]), 8319.38)


def test_federal_bpa_credit_2025():
    # $16,129 x 14.5% = $2,338.71
    assert close(FEDERAL[2025]["bpa_max"] * FEDERAL[2025]["credit_rate"], 2338.71)


def test_cpp_and_ei_2025():
    assert cpp_contributions(100_000, 2025)["cpp"] == 4034.10   # maximum
    assert cpp_contributions(100_000, 2025)["cpp2"] == 396.00   # maximum
    assert ei_premium(50_000, 2025) == 820.00                   # 50,000 x 1.64%
    assert ei_premium(100_000, 2025) == 1077.48                 # maximum


def test_ontario_no_tax_up_to_18569_in_2025():
    assert total_tax(18_500, 2025)["ontario"] == 0


def test_2025_and_2026_both_work():
    assert take_home(75_000, 2025)["take_home"] > 0
    assert take_home(75_000, 2026)["take_home"] > 0
