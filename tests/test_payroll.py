"""CPP, CPP2 and EI tests. Expected values calculated by hand from 2026 CRA rates."""

from canadatax import cpp_contributions, ei_premium, take_home, total_tax


def test_cpp_50k():
    c = cpp_contributions(50_000)
    assert c["cpp"] == 2766.75      # (50,000 - 3,500) x 5.95%
    assert c["cpp2"] == 0           # below the YMPE
    assert c["base"] == 2301.75     # (50,000 - 3,500) x 4.95%
    assert c["enhanced"] == 465.00  # (50,000 - 3,500) x 1%


def test_cpp_80k():
    c = cpp_contributions(80_000)
    assert c["cpp"] == 4230.45      # maximum
    assert c["cpp2"] == 216.00      # (80,000 - 74,600) x 4%


def test_cpp_maximums():
    c = cpp_contributions(150_000)
    assert c["cpp"] == 4230.45
    assert c["cpp2"] == 416.00


def test_cpp_below_exemption():
    assert cpp_contributions(3_000)["cpp"] == 0


def test_ei():
    assert ei_premium(50_000) == 815.00     # 50,000 x 1.63%
    assert ei_premium(80_000) == 1123.07    # maximum


def test_take_home_adds_up():
    r = take_home(75_000)
    parts = r["income_tax"] + r["cpp"] + r["cpp2"] + r["ei"]
    assert abs(r["total_deductions"] - parts) < 0.02
    assert abs(r["take_home"] - (75_000 - r["total_deductions"])) < 0.02


def test_cpp_and_ei_lower_income_tax():
    # credits and the CPP deduction mean less income tax than ignoring them
    assert take_home(75_000)["income_tax"] < total_tax(75_000)["total"]
