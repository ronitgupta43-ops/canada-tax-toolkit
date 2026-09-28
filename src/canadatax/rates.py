"""Tax rates and thresholds by year.

Sources (2026): CRA federal rates, CRA T4127 payroll formulas, Ontario TD1ON.
When adding a new year, copy the latest block, update every number,
and add a test that checks a known example from an official source.
"""

FEDERAL = {
    2026: {
        # (upper limit of bracket, rate); None = no upper limit
        "brackets": [
            (58_523, 0.14),
            (117_045, 0.205),
            (181_440, 0.26),
            (258_482, 0.29),
            (None, 0.33),
        ],
        "bpa_max": 16_452,   # basic personal amount, full
        "bpa_min": 14_829,   # BPA once income reaches top bracket
        "bpa_phaseout_start": 181_440,
        "bpa_phaseout_end": 258_482,
        "credit_rate": 0.14,
    },
}

ONTARIO = {
    2026: {
        "brackets": [
            (53_891, 0.0505),
            (107_785, 0.0915),
            (150_000, 0.1116),   # not indexed for inflation
            (220_000, 0.1216),   # not indexed for inflation
            (None, 0.1316),
        ],
        "bpa": 12_989,
        "credit_rate": 0.0505,
        # surtax is charged on basic Ontario tax, not on income
        "surtax": [(5_818, 0.20), (7_446, 0.36)],
    },
}
