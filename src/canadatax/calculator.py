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
    """Ontario tax including surtax, after the low-income tax reduction.

    The Ontario Health Premium is calculated separately.
    """
    r = _rates(ONTARIO, year)
    basic = ontario_basic_tax(taxable_income, year)
    tax = basic + ontario_surtax(basic, year)
    reduction = max(0, 2 * r["tax_reduction"] - tax)
    reduction = min(reduction, tax)
    return round(tax - reduction, 2)


def ontario_health_premium(taxable_income, year=2026):
    """Ontario Health Premium: $0 up to $900, based on taxable income.

    Each level ramps up at a rate above its threshold, then flattens at a cap.
    """
    r = _rates(ONTARIO, year)
    premium = 0.0
    for threshold, rate, base, cap in r["health_premium"]:
        if taxable_income > threshold:
            premium = min(cap, base + rate * (taxable_income - threshold))
    return round(premium, 2)


def total_tax(taxable_income, year=2026):
    """Summary of federal + Ontario tax for one income."""
    fed = federal_tax(taxable_income, year)
    on = ontario_tax(taxable_income, year)
    ohp = ontario_health_premium(taxable_income, year)
    total = round(fed + on + ohp, 2)
    nxt = taxable_income + 100
    next_dollar = federal_tax(nxt, year) + ontario_tax(nxt, year) + ontario_health_premium(nxt, year)
    return {
        "year": year,
        "income": taxable_income,
        "federal": fed,
        "ontario": on,
        "ontario_health_premium": ohp,
        "total": total,
        "after_tax_income": round(taxable_income - total, 2),
        "average_rate": round(total / taxable_income, 4) if taxable_income else 0.0,
        "marginal_rate": round((next_dollar - total) / 100, 4),
    }
