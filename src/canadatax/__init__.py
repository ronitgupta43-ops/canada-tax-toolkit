"""canadatax: simple, transparent Canadian income tax calculations."""

from .calculator import (
    bracket_tax,
    cpp_contributions,
    ei_premium,
    federal_bpa,
    federal_tax,
    ontario_health_premium,
    ontario_tax,
    take_home,
    total_tax,
)

__version__ = "0.2.0"
__all__ = [
    "bracket_tax", "cpp_contributions", "ei_premium", "federal_bpa", "federal_tax",
    "ontario_health_premium", "ontario_tax", "take_home", "total_tax",
]
