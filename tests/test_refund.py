"""Refund estimate tests."""

from canadatax import refund_estimate, take_home


def test_refund_is_deducted_minus_owed():
    owed = take_home(50_000)["income_tax"]
    r = refund_estimate(50_000, owed + 1_000)
    assert r["tax_refund"] == 1000.00


def test_balance_owing_is_negative():
    owed = take_home(50_000)["income_tax"]
    r = refund_estimate(50_000, owed - 300)
    assert r["tax_refund"] == -300.00


def test_part_year_worker_gets_refund():
    # Paid $2,500 every two weeks, so payroll withholds as if earning $65,000,
    # but only worked 20 of 26 pay periods: $50,000 for the year.
    per_pay = round(take_home(65_000)["income_tax"] / 26, 2)
    r = refund_estimate(50_000, per_pay * 20)
    assert r["tax_refund"] > 1_000


def test_cpp_ei_overpayment_two_employers():
    # Two employers each deducted the full CPP maximum: one maximum comes back
    r = refund_estimate(100_000, 20_000, cpp_deducted=2 * (4230.45 + 416.00), ei_deducted=2 * 1123.07)
    assert r["cpp_refund"] == 4646.45
    assert r["ei_refund"] == 1123.07


def test_no_cpp_refund_when_not_entered():
    r = refund_estimate(50_000, 6_000)
    assert r["cpp_refund"] == 0 and r["ei_refund"] == 0
