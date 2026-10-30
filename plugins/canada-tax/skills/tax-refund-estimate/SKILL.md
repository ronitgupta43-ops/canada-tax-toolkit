---
name: tax-refund-estimate
description: Estimate an Ontario employee's tax refund or balance owing from pay stub or T4 numbers, including CPP/EI overpaid with two employers. Use for "will I get a refund", "did I overpay tax", "check my pay stub".
---

# Ontario tax refund estimate

## Setup (once per session)

```bash
pip install canada-tax-toolkit || pip install git+https://github.com/ronitgupta43-ops/canada-tax-toolkit
```

Add `--break-system-packages` if pip asks for it. Run the library; never work the brackets, credits, CPP or EI out by hand.

Inputs: total employment income for the year and **income tax only** deducted. Pay stubs often show one "Taxes" total that includes CPP and EI. Ask for the Fed Tax / Prov Tax lines, or subtract CPP and EI first. Mid-year: add expected remaining paycheques to both numbers.

```bash
python -c "from canadatax import refund_estimate; print(refund_estimate(47274.45, 6127.12, 2026))"
```

More than one employer: also pass the year's totals `cpp_deducted=` and `ei_deducted=` to catch overpayments.

Report `total_refund` (negative means owing), plus tax deducted vs tax owed. If the refund is above about 60% of `cpp_required + ei_required`, warn that CPP/EI were probably included in the tax figure. It's an estimate, not tax advice.
