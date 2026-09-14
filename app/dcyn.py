
from enum import Enum


class DCYNValidationError(ValueError):
    """Raised when a Yes/No value is outside the DCYN contract."""


class DCYNValue(Enum):
    YES = True
    NO = False


def parse_dcyn(value: object) -> bool:
    """Convert an exact Yes/No value to a Boolean.

    Surrounding whitespace is ignored and matching is case-insensitive.
    Every other value is rejected to keep the rule deterministic.
    """
    if not isinstance(value, str):
        raise DCYNValidationError("Value must be the string Yes or No.")

    normalized = value.strip().casefold()

    if normalized == "yes":
        return DCYNValue.YES.value

    if normalized == "no":
        return DCYNValue.NO.value

    raise DCYNValidationError("Value must be exactly Yes or No.")
