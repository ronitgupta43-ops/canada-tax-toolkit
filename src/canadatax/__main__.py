"""Command line: python -m canadatax 75000 [year]"""

import sys
from .calculator import take_home


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m canadatax <employment_income> [year]")
        sys.exit(1)
    income = float(sys.argv[1].replace(",", ""))
    year = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    r = take_home(income, year)
    print(f"Ontario employee, {r['year']} tax year")
    print(f"Employment income: ${r['employment_income']:>12,.2f}")
    print(f"Federal tax:       ${r['federal']:>12,.2f}")
    print(f"Ontario tax:       ${r['ontario']:>12,.2f}")
    print(f"Health premium:    ${r['ontario_health_premium']:>12,.2f}")
    print(f"CPP:               ${r['cpp']:>12,.2f}")
    print(f"CPP2:              ${r['cpp2']:>12,.2f}")
    print(f"EI:                ${r['ei']:>12,.2f}")
    print(f"Total deductions:  ${r['total_deductions']:>12,.2f}")
    print(f"Take-home pay:     ${r['take_home']:>12,.2f}")
    print(f"Per month:         ${r['monthly_take_home']:>12,.2f}")


if __name__ == "__main__":
    main()
