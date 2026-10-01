"""Ontario Health Premium tests. Expected values calculated by hand from the ON428 table."""

from canadatax import ontario_health_premium, total_tax


def test_ohp_examples():
    cases = {
        18_000: 0,      # below $20,000
        22_000: 120,    # 6% of $2,000
        30_000: 300,    # flat $300 band
        37_000: 360,    # $300 + 6% of $1,000
        48_200: 500,    # $450 + 25% of $200
        100_000: 750,   # flat $750 band
        250_000: 900,   # maximum
    }
    for income, expected in cases.items():
        assert ontario_health_premium(income) == expected, income


def test_ohp_boundaries():
    assert ontario_health_premium(20_000) == 0
    assert ontario_health_premium(25_000) == 300
    assert ontario_health_premium(38_500) == 450
    assert ontario_health_premium(48_600) == 600
    assert ontario_health_premium(72_600) == 750
    assert ontario_health_premium(200_600) == 900


def test_total_includes_ohp():
    r = total_tax(75_000)
    assert r["ontario_health_premium"] == 750
    assert r["total"] == round(r["federal"] + r["ontario"] + 750, 2)
