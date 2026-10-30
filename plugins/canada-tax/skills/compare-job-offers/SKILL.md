---
name: compare-job-offers
description: Compare two or more Ontario salaries or job offers by real take-home pay per year and per month after tax, CPP and EI. Use for "is $X vs $Y worth it", "what does a raise to $X really give me".
---

# Compare Ontario job offers

## Setup (once per session)

```bash
pip install canada-tax-toolkit || pip install git+https://github.com/ronitgupta43-ops/canada-tax-toolkit
```

Add `--break-system-packages` if pip asks for it. Run the library; never work the brackets, credits, CPP or EI out by hand.

```bash
python -c "
from canadatax import take_home
for s in (60000, 68000):
    r = take_home(s, 2026); print(s, r['take_home'], round(r['take_home']/12, 2))"
```

Report a small table: salary, take-home per year, per month, and the take-home difference. Also give the share of each extra dollar kept: take-home difference ÷ salary difference.

Salary only. Benefits, pension matching and commute costs aren't included, so mention them if the offers differ. It's an estimate, not tax advice.
