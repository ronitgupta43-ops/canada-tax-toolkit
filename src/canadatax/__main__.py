"""Command line: python -m canadatax 75000 [year]"""

import sys
from .calculator import total_tax


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m canadatax <taxable_income> [year]")
        sys.exit(1)
    income = float(sys.argv[1].replace(",", ""))
    year = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    r = total_tax(income, year)
    print(f"Ontario resident, {r['year']} tax year")
    print(f"Taxable income:    ${r['income']:>12,.2f}")
    print(f"Federal tax:       ${r['federal']:>12,.2f}")
    print(f"Ontario tax:       ${r['ontario']:>12,.2f}")
    print(f"Total tax:         ${r['total']:>12,.2f}")
    print(f"After-tax income:  ${r['after_tax_income']:>12,.2f}")
    print(f"Average rate:      {r['average_rate']:>12.2%}")
    print(f"Marginal rate:     {r['marginal_rate']:>12.2%}")


if __name__ == "__main__":
    main()
