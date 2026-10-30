"""canadatax: simple, transparent Canadian income tax calculations."""

from .calculator import (
    bracket_tax,
    canada_employment_amount,
    cpp_contributions,
    ei_premium,
    federal_bpa,
    federal_tax,
    ontario_health_premium,
    ontario_tax,
    provincial_tax,
    refund_estimate,
    take_home,
    total_tax,
)

__version__ = "0.5.0"
__all__ = [
    "bracket_tax", "canada_employment_amount", "cpp_contributions", "ei_premium", "federal_bpa", "federal_tax",
    "ontario_health_premium", "ontario_tax", "provincial_tax", "refund_estimate", "take_home", "total_tax",
]
