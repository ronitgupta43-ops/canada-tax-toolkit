"""Canada employment amount tests. Expected values calculated by hand."""

from canadatax import canada_employment_amount, take_home, total_tax


def test_amount_is_capped():
    assert canada_employment_amount(75_000) == 1_501   # maximum
    assert canada_employment_amount(1_000) == 1_000    # all of a small income


def test_federal_tax_drops_by_14_percent():
    # Same income tax inputs, with and without the credit: $1,501 x 14% = $210.14
    without = total_tax(70_000)["federal"]
    with_credit = total_tax(70_000, federal_only_credits=1_501)["federal"]
    assert abs((without - with_credit) - 210.14) < 0.02


def test_ontario_tax_unchanged():
    # Federal-only credit: Ontario tax must not change
    assert total_tax(70_000)["ontario"] == total_tax(70_000, federal_only_credits=1_501)["ontario"]


def test_low_income_saves_nothing():
    # Non-refundable: tax can't go below $0
    assert take_home(10_000)["federal"] == 0
