"""Tax rates and thresholds by year.

Sources (2026): CRA federal rates, CRA T4127 payroll formulas, Ontario TD1ON.
When adding a new year, copy the latest block, update every number,
and add a test that checks a known example from an official source.
"""

FEDERAL = {
    2025: {
        # Lowest rate cut from 15% to 14% on July 1, 2025: full-year rate is 14.5%
        # Source: CRA T4032ON payroll tables, July 2025
        "brackets": [
            (57_375, 0.145),
            (114_750, 0.205),
            (177_882, 0.26),
            (253_414, 0.29),
            (None, 0.33),
        ],
        "bpa_max": 16_129,
        "bpa_min": 14_538,
        "bpa_phaseout_start": 177_882,
        "bpa_phaseout_end": 253_414,
        "credit_rate": 0.145,
        "employment_amount": 1_471,
    },
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
        # Canada employment amount (federal only), Schedule 1 line 31260
        "employment_amount": 1_501,
    },
}

ONTARIO = {
    2025: {
        # Source: TaxTips.ca Ontario 2025 rates; EY Ontario Budget 2025 summary
        "brackets": [
            (52_886, 0.0505),
            (105_775, 0.0915),
            (150_000, 0.1116),
            (220_000, 0.1216),
            (None, 0.1316),
        ],
        "bpa": 12_747,
        "credit_rate": 0.0505,
        "surtax": [(5_710, 0.20), (7_307, 0.36)],
        "tax_reduction": 294,
        "health_premium": [   # unchanged since 2005
            (20_000, 0.06, 0, 300),
            (36_000, 0.06, 300, 450),
            (48_000, 0.25, 450, 600),
            (72_000, 0.25, 600, 750),
            (200_000, 0.25, 750, 900),
        ],
    },
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
        # Ontario tax reduction (low income), basic amount for an individual
        # Source: CRA form ON428, Part C; EY Ontario Budget 2026 summary
        "tax_reduction": 300,
        # Ontario Health Premium: (threshold, rate, base, cap)
        # Source: Ontario Taxation Act, 2007; CRA form ON428
        "health_premium": [
            (20_000, 0.06, 0, 300),
            (36_000, 0.06, 300, 450),
            (48_000, 0.25, 450, 600),
            (72_000, 0.25, 600, 750),
            (200_000, 0.25, 750, 900),
        ],
    },
}

# Employee payroll contributions: CPP and EI
# Source: CRA 2026 CPP and EI rates and maximums
PAYROLL = {
    2025: {
        # Source: CRA T4032ON payroll tables, 2025
        "cpp_exemption": 3_500,
        "ympe": 71_300,
        "cpp_rate": 0.0595,
        "cpp_base_rate": 0.0495,
        "yampe": 81_200,
        "cpp2_rate": 0.04,
        "ei_max_insurable": 65_700,
        "ei_rate": 0.0164,
    },
    2026: {
        "cpp_exemption": 3_500,
        "ympe": 74_600,           # CPP ceiling
        "cpp_rate": 0.0595,       # employee rate, $3,500 to YMPE
        "cpp_base_rate": 0.0495,  # part of cpp_rate that earns a tax credit;
                                  # the other 1% is a deduction from income
        "yampe": 85_000,          # CPP2 ceiling
        "cpp2_rate": 0.04,        # employee rate, YMPE to YAMPE (a deduction)
        "ei_max_insurable": 68_900,
        "ei_rate": 0.0163,        # EI premiums earn a tax credit
    },
}
