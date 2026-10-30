"""BC and Alberta tests. Expected values calculated by hand from 2026 rates."""

from canadatax import provincial_tax, take_home, ontario_tax


def close(a, b):
    return abs(a - b) < 0.02


def test_bc_60k():
    # 50,363 x 5.6% + 9,637 x 7.7% - 13,216 x 5.6%
    assert close(provincial_tax(60_000, 2026, "BC"), 2822.28)


def test_bc_tax_reduction():
    # $690 reduction, less 3.56% of income over $25,570
    assert close(provincial_tax(30_000, 2026, "BC"), 1680 - 740.10 - (690 - 0.0356 * 4_430))
    assert provincial_tax(20_000, 2026, "BC") == 0   # full $690 wipes out the tax


def test_alberta():
    assert close(provincial_tax(60_000, 2026, "AB"), 4_800 - 22_769 * 0.08)
    assert close(provincial_tax(100_000, 2026, "AB"), 4_896 + 3_880 - 1_821.52)


def test_ontario_unchanged():
    assert provincial_tax(75_000, 2026, "ON") == ontario_tax(75_000, 2026)
    assert take_home(75_000)["take_home"] == 56925.82


def test_no_health_premium_outside_ontario():
    assert take_home(75_000, 2026, "BC")["ontario_health_premium"] == 0
    assert take_home(75_000, 2026, "AB")["ontario_health_premium"] == 0


def test_unknown_province():
    try:
        provincial_tax(50_000, 2026, "QC")
    except ValueError:
        return
    raise AssertionError("expected ValueError")
