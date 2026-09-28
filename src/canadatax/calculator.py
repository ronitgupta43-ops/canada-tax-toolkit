"""Federal and Ontario personal income tax calculator."""

from .rates import FEDERAL, ONTARIO


def _rates(table, year):
    if year not in table:
        raise ValueError(f"No rates for {year}. Available: {sorted(table)}")
    return table[year]


def bracket_tax(income, brackets):
    """Apply progressive brackets to an income amount."""
    tax, lower = 0.0, 0.0
    for upper, rate in brackets:
        if upper is None or income <= upper:
            return tax + (income - lower) * rate
        tax += (upper - lower) * rate
        lower = upper
    return tax


def federal_bpa(net_income, year=2026):
    """Federal basic personal amount, phased down for high incomes."""
    r = _rates(FEDERAL, year)
    start, end = r["bpa_phaseout_start"], r["bpa_phaseout_end"]
    extra = r["bpa_max"] - r["bpa_min"]
    if net_income <= start:
        return r["bpa_max"]
    if net_income >= end:
        return r["bpa_min"]
    return r["bpa_min"] + extra * (end - net_income) / (end - start)


def federal_tax(taxable_income, year=2026):
    """Basic federal tax after the basic personal amount credit."""
    r = _rates(FEDERAL, year)
    gross = bracket_tax(taxable_income, r["brackets"])
    credit = federal_bpa(taxable_income, year) * r["credit_rate"]
    return round(max(0.0, gross - credit), 2)


def ontario_basic_tax(taxable_income, year=2026):
    """Ontario tax after the basic personal amount credit, before surtax."""
    r = _rates(ONTARIO, year)
    gross = bracket_tax(taxable_income, r["brackets"])
    credit = r["bpa"] * r["credit_rate"]
    return max(0.0, gross - credit)


def ontario_surtax(basic_tax, year=2026):
    r = _rates(ONTARIO, year)
    return sum(max(0.0, basic_tax - t) * rate for t, rate in r["surtax"])


def ontario_tax(taxable_income, year=2026):
    """Ontario tax including surtax.

    Not yet included: Ontario tax reduction (low income) and
    Ontario Health Premium. See README roadmap.
    """
    basic = ontario_basic_tax(taxable_income, year)
    return round(basic + ontario_surtax(basic, year), 2)


def total_tax(taxable_income, year=2026):
    """Summary of federal + Ontario tax for one income."""
    fed = federal_tax(taxable_income, year)
    on = ontario_tax(taxable_income, year)
    total = round(fed + on, 2)
    next_dollar = federal_tax(taxable_income + 100, year) + ontario_tax(taxable_income + 100, year)
    return {
        "year": year,
        "income": taxable_income,
        "federal": fed,
        "ontario": on,
        "total": total,
        "after_tax_income": round(taxable_income - total, 2),
        "average_rate": round(total / taxable_income, 4) if taxable_income else 0.0,
        "marginal_rate": round((next_dollar - total) / 100, 4),
    }
