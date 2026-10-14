"""Federal and Ontario personal income tax calculator."""

from .rates import FEDERAL, ONTARIO, PAYROLL


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


def federal_tax(taxable_income, year=2026, other_credits=0):
    """Basic federal tax after the basic personal amount credit.

    other_credits: extra credit amounts (like base CPP and EI) that earn
    a credit at the same rate as the basic personal amount.
    """
    r = _rates(FEDERAL, year)
    gross = bracket_tax(taxable_income, r["brackets"])
    credit = (federal_bpa(taxable_income, year) + other_credits) * r["credit_rate"]
    return round(max(0.0, gross - credit), 2)


def ontario_basic_tax(taxable_income, year=2026, other_credits=0):
    """Ontario tax after non-refundable credits, before surtax."""
    r = _rates(ONTARIO, year)
    gross = bracket_tax(taxable_income, r["brackets"])
    credit = (r["bpa"] + other_credits) * r["credit_rate"]
    return max(0.0, gross - credit)


def ontario_surtax(basic_tax, year=2026):
    r = _rates(ONTARIO, year)
    return sum(max(0.0, basic_tax - t) * rate for t, rate in r["surtax"])


def ontario_tax(taxable_income, year=2026, other_credits=0):
    """Ontario tax including surtax, after the low-income tax reduction.

    The Ontario Health Premium is calculated separately.
    """
    r = _rates(ONTARIO, year)
    basic = ontario_basic_tax(taxable_income, year, other_credits)
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


def cpp_contributions(employment_income, year=2026):
    """Employee CPP and CPP2 contributions on employment income.

    Returns a dict:
      cpp       - CPP on earnings between the exemption and the YMPE
      cpp2      - CPP2 on earnings between the YMPE and the YAMPE
      base      - part of cpp that earns a tax credit
      enhanced  - part of cpp that is a deduction from income
    """
    r = _rates(PAYROLL, year)
    pensionable = min(employment_income, r["ympe"]) - r["cpp_exemption"]
    pensionable = max(0.0, pensionable)
    cpp = round(pensionable * r["cpp_rate"], 2)
    base = round(pensionable * r["cpp_base_rate"], 2)
    cpp2_earnings = max(0.0, min(employment_income, r["yampe"]) - r["ympe"])
    cpp2 = round(cpp2_earnings * r["cpp2_rate"], 2)
    return {"cpp": cpp, "cpp2": cpp2, "base": base, "enhanced": round(cpp - base, 2)}


def ei_premium(employment_income, year=2026):
    """Employee EI premium on employment income."""
    r = _rates(PAYROLL, year)
    return round(min(employment_income, r["ei_max_insurable"]) * r["ei_rate"], 2)


def total_tax(taxable_income, year=2026, other_credits=0, federal_only_credits=0):
    """Summary of federal + Ontario tax for one taxable income.

    other_credits: credit amounts claimed both federally and in Ontario
    federal_only_credits: credit amounts claimed only federally
    """
    fed_credits = other_credits + federal_only_credits

    def tax_at(income):
        return (federal_tax(income, year, fed_credits)
                + ontario_tax(income, year, other_credits)
                + ontario_health_premium(income, year))

    fed = federal_tax(taxable_income, year, fed_credits)
    on = ontario_tax(taxable_income, year, other_credits)
    ohp = ontario_health_premium(taxable_income, year)
    total = round(fed + on + ohp, 2)
    return {
        "year": year,
        "income": taxable_income,
        "federal": fed,
        "ontario": on,
        "ontario_health_premium": ohp,
        "total": total,
        "after_tax_income": round(taxable_income - total, 2),
        "average_rate": round(total / taxable_income, 4) if taxable_income else 0.0,
        "marginal_rate": round((tax_at(taxable_income + 100) - total) / 100, 4),
    }


def canada_employment_amount(employment_income, year=2026):
    """Federal Canada employment amount: employment income, up to a yearly maximum."""
    r = _rates(FEDERAL, year)
    return min(employment_income, r["employment_amount"])


def take_home(employment_income, year=2026):
    """Take-home pay for an Ontario employee: income tax, CPP and EI.

    How CPP and EI affect income tax:
      - the enhanced part of CPP and all of CPP2 are deducted from income
      - base CPP and EI premiums earn non-refundable tax credits
    Employees also get the federal Canada employment amount credit.
    """
    c = cpp_contributions(employment_income, year)
    ei = ei_premium(employment_income, year)
    taxable = round(employment_income - c["enhanced"] - c["cpp2"], 2)
    credits = c["base"] + ei
    employment = canada_employment_amount(employment_income, year)
    t = total_tax(taxable, year, other_credits=credits, federal_only_credits=employment)
    deductions = round(t["total"] + c["cpp"] + c["cpp2"] + ei, 2)
    return {
        "year": year,
        "employment_income": employment_income,
        "taxable_income": taxable,
        "federal": t["federal"],
        "ontario": t["ontario"],
        "ontario_health_premium": t["ontario_health_premium"],
        "income_tax": t["total"],
        "cpp": c["cpp"],
        "cpp2": c["cpp2"],
        "ei": ei,
        "total_deductions": deductions,
        "take_home": round(employment_income - deductions, 2),
        "monthly_take_home": round((employment_income - deductions) / 12, 2),
        "average_rate": round(deductions / employment_income, 4) if employment_income else 0.0,
    }
