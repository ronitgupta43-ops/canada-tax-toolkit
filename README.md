# Canada Tax Toolkit 🇨🇦

Take-home pay and tax refund calculator for **Ontario, BC and Alberta**: federal and provincial tax, the Ontario Health Premium, CPP, CPP2 and EI. Every rate comes from CRA and lives in one readable file (`src/canadatax/rates.py`), and every calculation is checked against hand-worked examples.

**👉 Try it online: [ronitgupta43-ops.github.io/canada-tax-toolkit](https://ronitgupta43-ops.github.io/canada-tax-toolkit/)**

## Quick start

```bash
pip install canada-tax-toolkit
python -m canadatax 75000
```

```python
from canadatax import take_home, refund_estimate

take_home(75_000, 2026)                  # take-home pay with every deduction (Ontario)
take_home(75_000, 2026, "BC")            # or "AB" for Alberta
refund_estimate(47_274.45, 6_127.12)     # income for the year, income tax deducted
```

## Use it with Claude Code

```
/plugin marketplace add ronitgupta43-ops/canada-tax-toolkit
/plugin install canada-tax@canada-tax-toolkit
```

Adds three skills: take-home pay, tax refund estimate, and job offer comparison.

## What's included

- Federal tax for 2025 and 2026
- Ontario tax for 2025 and 2026, including the surtax and low-income tax reduction
- BC tax (2026), including the BC tax reduction
- Alberta tax (2026)
- Ontario Health Premium
- CPP, CPP2 and EI, with the tax credits and deduction they give you
- Canada employment amount
- Refund estimator, including CPP/EI overpaid with more than one employer
- Free web calculator that runs the same Python code in your browser

## Roadmap — contributions welcome!

- [x] BC and Alberta
- [ ] Other provinces (Quebec, Manitoba, Saskatchewan…)
- [ ] RRSP "what if" calculator

## Disclaimer

This is an educational tool, not tax advice. Always confirm with CRA or a tax professional.

## License

MIT
