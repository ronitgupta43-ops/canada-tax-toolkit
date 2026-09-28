"""Tests use worked examples published by tax reference sites / CRA formulas."""

from canadatax import bracket_tax, federal_bpa, federal_tax, ontario_tax
from canadatax.calculator import ontario_basic_tax, ontario_surtax
from canadatax.rates import FEDERAL


def test_first_federal_bracket():
    # 14% of the first $58,523 = $8,193.22
    assert round(bracket_tax(58_523, FEDERAL[2026]["brackets"]), 2) == 8193.22


def test_federal_bpa_phaseout():
    assert federal_bpa(100_000) == 16_452
    assert federal_bpa(300_000) == 14_829
    assert 14_829 < federal_bpa(220_000) < 16_452


def test_ontario_150k_basic_and_surtax():
    basic = ontario_basic_tax(150_000)
    assert round(basic, 2) == 11708.05
    assert round(ontario_surtax(basic), 2) == round(1178.01 + 1534.34, 2)


def test_ontario_75k_no_surtax():
    basic = ontario_basic_tax(75_000)
    assert abs(basic - 3997.03) < 0.01  # source rounds each bracket


def test_low_income_pays_no_tax():
    assert federal_tax(10_000) == 0
    assert ontario_tax(10_000) == 0


def test_unknown_year_raises():
    try:
        federal_tax(50_000, year=1999)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
