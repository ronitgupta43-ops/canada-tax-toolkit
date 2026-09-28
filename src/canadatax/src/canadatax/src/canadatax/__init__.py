"""canadatax: simple, transparent Canadian income tax calculations."""

from .calculator import (
    bracket_tax,
    federal_bpa,
    federal_tax,
    ontario_tax,
    total_tax,
)

__version__ = "0.1.0"
__all__ = ["bracket_tax", "federal_bpa", "federal_tax", "ontario_tax", "total_tax"]
