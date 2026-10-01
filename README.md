# Canada Tax Toolkit 🇨🇦

Simple, transparent Python tools for Canadian personal income tax — starting with **federal + Ontario** for the **2026** tax year.

Every rate lives in one readable file (`src/canadatax/rates.py`), and every calculation is tested against published worked examples.
**👉 Try it online: [ronitgupta43-ops.github.io/canada-tax-toolkit](https://ronitgupta43-ops.github.io/canada-tax-toolkit/)**

## Quick start

```bash
git clone https://github.com/ronitgupta43-ops/canada-tax-toolkit.git
cd canada-tax-toolkit
pip install -e .
python -m canadatax 75000
```

```python
from canadatax import total_tax
print(total_tax(75_000))
```

## What's included (v0.1)

- 2026 federal brackets (14% lowest rate) and basic personal amount, including the high-income phase-out
- 2026 Ontario brackets, basic personal amount and two-tier surtax
- Average and marginal tax rates
- Command-line tool
- Ontario low-income tax reduction and Ontario Health Premium
- Free web calculator that runs in your browser

## Roadmap — contributions welcome!

- [x] Ontario tax reduction (low-income)
- [x] Ontario Health Premium
- [ ] CPP / EI contributions and credits
- [ ] 2025 rates (with the blended 14.5% federal rate)
- [ ] Other provinces (BC, Alberta, Quebec…)
- [ ] RRSP deduction "what if" calculator

## Disclaimer

This is an educational tool, not tax advice. Always confirm with CRA or a tax professional.

## License

MIT
