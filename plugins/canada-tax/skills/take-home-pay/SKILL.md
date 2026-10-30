---
name: take-home-pay
description: Ontario take-home pay for a salary in 2025 or 2026 - federal and Ontario tax, Health Premium, CPP, EI, per year, month and paycheque. Use for "what's my take-home on $X", "how much tax on $X in Ontario".
---

# Ontario take-home pay

## Setup (once per session)

```bash
pip install canada-tax-toolkit || pip install git+https://github.com/ronitgupta43-ops/canada-tax-toolkit
```

Add `--break-system-packages` if pip asks for it. Run the library; never work the brackets, credits, CPP or EI out by hand.

```bash
python -c "from canadatax import take_home; print(take_home(75000, 2026))"
```

Report: take-home per year and per month, then federal tax, Ontario tax, Health Premium, CPP + CPP2 and EI. For every two weeks, divide take-home by 26.

Covers single Ontario employees only. Not covered: other provinces, RRSP and other deductions, self-employment. Say so instead of guessing. It's an estimate, not tax advice.
